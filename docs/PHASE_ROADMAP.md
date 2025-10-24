# CrapsSim-Evo — Active Phase Plan

## Current Phase: 3 — Deterministic RNG Utilities

### Objective
Create a unified RNG system enabling deterministic reproducibility and replayability.

### Checkpoints
| Phase | Checkpoint | Title | Outcome |
|:----:|:------------|:------|:---------|
| 3 | P3·C1 | Seed + Subseed Utilities | Root and derived seed helpers implemented |
| 3 | P3·C2 | RNG Context | Context manager ensures isolation and determinism |
| 3 | P3·C3 | Hash Helpers | Stable dict and byte hashing utilities |
| 3 | P3·C4 | Tests + Docs | Verified repeatability, docs updated, baseline tagged |

### Exit Criteria
- RNG behavior deterministic across runs.
- `pytest -q` green and consistent.
- Ruff + Black clean.
- Baseline tag: `v0.0.3-phase3-baseline`.
