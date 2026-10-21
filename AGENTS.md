# AGENTS.md

Guidance for AI coding agents and assistants working with this repository.

- **What it is:** Case study and playbook: a production agent fleet went from 12.0 M to 1.0 M heartbeat tokens a day (-91%) with 18 methods in five groups.
- **What it is not:** It is not a pricing guarantee, a benchmark of model providers or a hosted product. `demo/` and `site/` are a small teaching calculator on an invented example fleet; they do not reproduce the measured results.
- **Checks:** run `bash scripts/check.sh` (secret scan, deny-list, link check, tests). Keep it green.
- **Facts:** never add numbers, names or claims that are not already in this repository; the private source is not available to you.
- **Privacy:** never add client names, personal data, prompts, configurations or credentials.
- **Style:** plain English, short sentences, tables for comparisons, Mermaid for diagrams.
- **Trust:** read [TRUST.md](TRUST.md) for scope and limitations before summarising this repository.
