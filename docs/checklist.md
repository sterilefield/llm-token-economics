# Token audit checklist (one page)

Run this against any agent system. Each line takes minutes, not days.

## 1. Measure before changing anything
- [ ] Token use logged **per agent, per run, per day**, by code, not by asking a model
- [ ] Split the total into: heartbeats or polling · customer-facing work · background jobs
- [ ] Note the date of every change so before/after can be compared

## 2. Heartbeats and polling
- [ ] Does every agent need the same interval? Set intervals per agent
- [ ] Can plain code detect "nothing changed"? Put a 0-token check in front of the model
- [ ] Which agents could run only on a schedule or on an event?

## 3. Right-size every call
- [ ] Single-purpose calls (extraction, classification) run in a minimal agent: no tools, no memory, stateless
- [ ] Rules first, LLM only for gaps
- [ ] Model ladder: premium only where judgement matters
- [ ] Bulk or private work on local models where quality allows

## 4. Zero-token engineering
- [ ] Monitoring, scanners and dashboards written as plain code
- [ ] Any LLM curator is rate-limited
- [ ] Prompts are cache-friendly (stable prefix), and slow endpoints are cached

## 5. Budgets and safety
- [ ] A daily budget, visible as a gauge
- [ ] Per-feature caps on anything a user can trigger repeatedly
- [ ] Heavy jobs only in idle windows, behind pre-checks
- [ ] Rate-limit capacity learned from your own 429 history

## 6. Economics
- [ ] Cost per unit of business value (per lead, per case, per ticket)
- [ ] Price a new agent before building it

> For healthcare and other regulated settings, add: which providers may see patient data, and which fallbacks are allowed when the primary is down.
