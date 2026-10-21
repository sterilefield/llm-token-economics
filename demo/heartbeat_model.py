#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Ravi Teja Thiriveedhi
"""heartbeat_model: estimate what methods 1, 2, 14 and 18 do to an agent fleet's heartbeat tokens.

    python3 demo/heartbeat_model.py                       # the invented example fleet
    python3 demo/heartbeat_model.py --fleet my_fleet.json # your own fleet (format below)
    python3 demo/heartbeat_model.py --price 0.40          # price per million tokens, any currency
    python3 demo/heartbeat_model.py --what-if 120 9000    # price a new agent: interval (min), tokens per wake

Fleet file: a JSON list of agents, each with
    name, interval_min (today), tokens (per heartbeat), changed (share of heartbeats that find
    something new, 0..1), and optionally new_interval_min.

The example fleet is invented for this demo; it is not the production fleet described in the
case study, and your numbers will differ. Standard library only.
"""
from __future__ import annotations

import json
import random
import sys
from dataclasses import dataclass

DAY_MIN = 24 * 60

EXAMPLE_FLEET = [  # synthetic, chosen only to show the shape of the calculation
    {"name": "intake", "interval_min": 30, "tokens": 18000, "changed": 0.45, "new_interval_min": 30},
    {"name": "follow-up", "interval_min": 30, "tokens": 14000, "changed": 0.20, "new_interval_min": 60},
    {"name": "scheduler", "interval_min": 30, "tokens": 9000, "changed": 0.15, "new_interval_min": 120},
    {"name": "reporter", "interval_min": 30, "tokens": 12000, "changed": 0.05, "new_interval_min": 360},
    {"name": "inventory", "interval_min": 30, "tokens": 8000, "changed": 0.20, "new_interval_min": 120},
    {"name": "research-scout", "interval_min": 30, "tokens": 16000, "changed": 0.10, "new_interval_min": 240},
    {"name": "qa-helper", "interval_min": 30, "tokens": 7000, "changed": 0.30, "new_interval_min": 60},
    {"name": "watchdog", "interval_min": 30, "tokens": 6000, "changed": 0.05, "new_interval_min": 180},
]


@dataclass
class Row:
    name: str
    before: float
    after_interval: float
    after_sentinel: float


def wakes_per_day(interval_min: float) -> float:
    return DAY_MIN / max(interval_min, 1)


def model(agent: dict) -> Row:
    """Before: an LLM call on every heartbeat.
    Method 1: a longer per-agent interval.
    Method 2: a 0-token sentinel checks state first; the model runs only when something changed.
    With a longer interval, a wake is more likely to find a change, so the expected share of
    wakes that need the model is 1 - (1 - changed) ** (new / old)."""
    old = max(agent["interval_min"], 1)
    new = max(agent.get("new_interval_min") or old, 1)
    before = wakes_per_day(old) * agent["tokens"]
    after_interval = wakes_per_day(new) * agent["tokens"]
    p_new = 1 - (1 - agent["changed"]) ** (new / old)
    after_sentinel = wakes_per_day(new) * p_new * agent["tokens"]
    return Row(agent["name"], before, after_interval, after_sentinel)


def fmt(n: float) -> str:
    if n >= 1e6:
        return f"{n / 1e6:.2f} M"
    if n >= 1e3:
        return f"{n / 1e3:.1f} k"
    return f"{n:.0f}"


def simulate_sentinel(changed: float, interval_min: int, seed: int = 7) -> tuple[int, int]:
    """One simulated day: the sentinel hashes state on every wake (0 tokens) and calls the model only on a change."""
    rnd = random.Random(seed)
    wakes = int(wakes_per_day(interval_min))
    calls = sum(1 for _ in range(wakes) if rnd.random() < changed)
    return wakes, calls


def report(fleet: list[dict], price: float | None, budget: float | None) -> dict:
    rows = [model(a) for a in fleet]
    tb = sum(r.before for r in rows)
    ti = sum(r.after_interval for r in rows)
    ts = sum(r.after_sentinel for r in rows)
    print("Heartbeat token model (estimate, not a measurement)")
    print(f"{'agent':<16}{'before/day':>12}{'+ method 1':>13}{'+ method 2':>13}{'change':>9}")
    print("-" * 63)
    for r in rows:
        ch = (r.after_sentinel - r.before) / r.before * 100 if r.before else 0
        print(f"{r.name:<16}{fmt(r.before):>12}{fmt(r.after_interval):>13}{fmt(r.after_sentinel):>13}{ch:>8.0f}%")
    print("-" * 63)
    total_change = (ts - tb) / tb * 100 if tb else 0
    print(f"{'fleet':<16}{fmt(tb):>12}{fmt(ti):>13}{fmt(ts):>13}{total_change:>8.0f}%")
    if price is not None:
        print(f"cost per day at {price} per million tokens: {tb / 1e6 * price:.2f} -> {ts / 1e6 * price:.2f}")
    if budget:
        used = ts / budget * 100
        bar = "#" * min(40, int(used / 2.5))
        print(f"daily budget {fmt(budget)} (method 14): [{bar:<40}] {used:.0f}% used after the change")
    return {"before": tb, "after_interval": ti, "after_sentinel": ts, "change_pct": total_change}


def what_if(interval_min: float, tokens: float, changed: float, price: float | None) -> dict:
    per_day = wakes_per_day(interval_min) * tokens
    gated = per_day * changed
    print(f"what-if (method 18): new agent waking every {interval_min:g} min, {fmt(tokens)} tokens a wake")
    print(f"  without a sentinel: {fmt(per_day)} a day, {fmt(per_day * 30)} a month")
    print(f"  with a sentinel at {changed:.0%} changes: {fmt(gated)} a day, {fmt(gated * 30)} a month")
    if price is not None:
        print(f"  monthly cost at {price} per million: {per_day * 30 / 1e6 * price:.2f} -> {gated * 30 / 1e6 * price:.2f}")
    return {"per_day": per_day, "gated": gated}


def main(argv: list[str]) -> int:
    args = argv[1:]

    def opt(name: str, n: int = 1):
        if name in args:
            i = args.index(name)
            return args[i + 1 : i + 1 + n]
        return None

    fleet = EXAMPLE_FLEET
    if opt("--fleet"):
        with open(opt("--fleet")[0], encoding="utf-8") as fh:
            fleet = json.load(fh)
    price = float(opt("--price")[0]) if opt("--price") else 0.40
    if opt("--what-if", 2):
        iv, tk = (float(x) for x in opt("--what-if", 2))
        what_if(iv, tk, 0.05, price)
        return 0
    print("Example fleet: invented for this demo (synthetic, not real)\n" if fleet is EXAMPLE_FLEET else "", end="")
    report(fleet, price, budget=3e6 if fleet is EXAMPLE_FLEET else None)
    print("measured case-study results: see the README; this example does not reproduce them")
    w, c = simulate_sentinel(0.05, 30)
    print(f"sentinel, one simulated day: {w} wakes at 0 tokens each, {c} model calls")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
