# CrapsSim-Evo — Active Phase Plan

## Current Phase: 7 — Lineage & DNA Tracking (Completed)

### Objective
Record deterministic ancestry data: parent spec hashes, structured op logs, and per-individual RNG subseeds.

### Checkpoints
| Phase | Checkpoint | Title | Status |
|:----:|:------------|:------|:--------|
| 7 | P7·C1 | DNA utilities & schema 0.2 | ✅ Merged |
| 7 | P7·C2 | Parent hashes & subseeds | ✅ Merged |
| 7 | P7·C3 | Structured ops logs | ✅ Merged |
| 7 | P7·C4 | Tests & docs | ✅ This commit |

### Exit Criteria
- `dna.json` contains parent hashes, ops logs, subseed, and `evo_schema_version: 0.2`.
- Tests pass; Ruff + Black clean.
- Tag: `v0.0.7-phase7-baseline`.

---

## Next Phase: 8 — Adaptive Stagnation Control
Integrate Level of Stagnation (LoS) metrics and automatic trigger rules to escape plateaus.
