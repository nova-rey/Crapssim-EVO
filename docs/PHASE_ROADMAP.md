# CrapsSim-Evo — Active Phase Plan

## Current Phase: 6 — Population & Evolution Loop (Completed)

### Objective
Implement the deterministic selection→variation→replacement loop and export the next generation bundle.

### Checkpoints
| Phase | Checkpoint | Title | Status |
|:----:|:------------|:------|:--------|
| 6 | P6·C1 | Population Loading | ✅ Merged |
| 6 | P6·C2 | Selection + Elitism | ✅ Merged |
| 6 | P6·C3 | Variation (CX + Mut) | ✅ Merged |
| 6 | P6·C4 | Export + Determinism | ✅ This commit |

### Exit Criteria
- Next generation exported to folder and zip.
- Deterministic with fixed `root_seed`.
- Tests pass; Ruff + Black clean.
- Tag: `v0.0.6-phase6-baseline`.

---

## Next Phase: 7 — Lineage & DNA Tracking
Enhance DNA with parent hashes, op parameters, RNG sub-seeds, and strong replay manifests.
