# CrapsSim-Evo — Active Phase Plan

## Current Phase: 4 — Bundle I/O & Manifest (Completed)

### Objective
Implement deterministic `.zip` bundle handling for Evo: unpack, validate, repack, and generate manifests.

### Checkpoints
| Phase | Checkpoint | Title | Status |
|:----:|:------------|:------|:--------|
| 4 | P4·C1 | Unpack + Validation | ✅ Merged |
| 4 | P4·C2 | Repack + Pass-through | ✅ Merged |
| 4 | P4·C3 | Checksums + Index | ✅ Merged |
| 4 | P4·C4 | Docs & Bible Wrap-Up | ✅ This commit |

### Exit Criteria
- Bundle extraction and repack confirmed lossless.
- Zip-slip guard validated.
- Checksum + contents index verified by tests.
- Repo lint- and format-clean (Ruff + Black).
- Tag created: `v0.0.4-phase4-baseline`.

---

## Next Phase: 5 — Fitness & Metrics Framework
Lay the groundwork for evaluating CSC simulation results:
- Parse journals, compute bankroll-based metrics, and generate fitness scores.
- Prepare metrics interface for LEAP integration.
