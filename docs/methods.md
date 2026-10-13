# The 18 methods

Each method lists the problem, what changed, and the measured effect where one was measured. A dash means the method contributed to a combined result rather than being measured alone.

## A · Heartbeat diet

| # | Method | What changed | Measured effect |
|---|---|---|---|
| 1 | **Per-agent heartbeat intervals** | One default interval replaced by intervals per agent: 2 h for the live intake agent, 4–24 h for others, and 11 agents moved to scheduled jobs only | Part of the −91% |
| 2 | **0-token gate sentinel** | Nine LLM heartbeats replaced by a deterministic check that wakes a model only when state has changed | Part of the −91% |
| 3 | **Before/after accounting** | Token use logged per agent, per run and per day from the moment of the change | 12.0 M → 1.0 M tokens a day (−91%); largest agent 7.2 M → 0.47 M (−93%); several agents −97% to −100% |

## B · Right-sized agents and models

| # | Method | What changed | Measured effect |
|---|---|---|---|
| 4 | **Dedicated minimal agent for single-purpose calls** | WhatsApp extraction moved out of a full agent (tools and memory loaded) into a tool-less, memory-less extractor with stateless calls | ~38 k → ~4 k tokens per message (1,177 turns, 0 errors) |
| 5 | **Three-tier model ladder** | Top tier only for live intake, a middle tier for reasoning agents, a light tier for scouts, extraction and Q&A | 7 models tracked by share of tokens |
| 6 | **Two-tier extraction** | Free rule-based parsing first; the LLM only fills gaps. Trivial lines are skipped, and extraction waits for 20 minutes of quiet and handles changes only | ~7.3 k tokens per lead with the second prompt version |
| 7 | **Bilingual glossary in the prompt** | A Telugu/Hindi-in-English glossary so extraction succeeds on the first pass | Fewer retries (A/B test on 5 leads) |
| 8 | **Local models for bulk or private work** | Photo descriptions (296) and embeddings run on a local model; the summary model moved local | 0 cloud tokens for media and memory |
| 9 | **Free-first routing with tracked fallbacks** | Free and local providers first, paid as fallback; dead fallbacks counted (2 of 10); a noisy auto-router (168 errors) identified | ₹0 marginal API cost per lead |

## C · Zero-token engineering

| # | Method | What changed | Measured effect |
|---|---|---|---|
| 10 | **Deterministic engines** | Knowledge capture, an architecture scanner (983 components), telemetry collectors, runbook sync and watchdogs are plain code | Monitoring and knowledge at 0 AI tokens |
| 11 | **Rate-limited LLM curators** | The one LLM curator runs at most every 6 hours and is skipped on small-context fallback models | 10.0 M tokens over 444 runs at ₹0 notional cost |
| 12 | **Read the dashboard, not the model** | Backfill reads the messaging provider's dashboard at 0 tokens, then makes one combined extraction per contact | — |
| 13 | **Cache-friendly design** | Stable prompt prefixes for provider caching; slow API endpoints cached for 60 s | 76% of tokens served from cache |

## D · Budgets, caps and windows

| # | Method | What changed | Measured effect |
|---|---|---|---|
| 14 | **Daily budget** | 15 M tokens a day, enforced and shown as a gauge | 1.5 M on the day measured (10% of budget) |
| 15 | **Per-feature caps** | Hard daily limits on question-answering and on backfill (≈2.5% of budget) | — |
| 16 | **Idle-aware windows** | Heavy jobs run only in quiet windows, and only when 7 pre-checks pass (gateway, load, no recent 429, budget, enabled, and more) | No 429 errors in 24 h |
| 17 | **Learned rate-limit forecasting** | Provider limits are unpublished, so capacity is learned from tokens used before past 429 errors | ~16.8 M per 5 h and ~341 M per 7 days learned; 3% used |

## E · Economics and governance

| # | Method | What changed | Measured effect |
|---|---|---|---|
| 18 | **Unit economics** | Cost per lead and per deal tracked; a what-if prices a new agent before it is built | Cost known before code is written |
