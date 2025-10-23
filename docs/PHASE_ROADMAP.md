# CrapsSim-Evo — Active Phase Plan

## Current Phase: 2 — Config & Logging Scaffolding

### Objective
Implement config loader (YAML + defaults + env substitution) and structured logging utilities.

### Checkpoints
| Phase | Checkpoint | Title | Outcome |
|------:|------------|-------|---------|
| 2 | P2·C1 | Config loader | YAML parser, defaults, env-var substitution. |
| 2 | P2·C2 | Logger | UTC timestamps, structured format, idempotent setup. |
| 2 | P2·C3 | Docs & tests | Add CONFIG_GUIDE.md and validation tests. |

### Exit Criteria
- Config loader merges YAML + defaults cleanly.
- Logging produces UTC-timestamped structured output.
- `pytest -q` passes all config/logging tests.
- Repo deterministic and CI green.
