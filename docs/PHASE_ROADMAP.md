# CrapsSim-Evo — Active Phase Plan

## Current Phase: Pre-Spec Scaffolding

### Objective
Lay down infrastructure, config systems, deterministic utilities, and safe bundle I/O prior to CSC spec finalization.

### Checkpoints
| Phase | Checkpoint | Title | Outcome |
|--------|-------------|--------|----------|
| 1 | P1·C1 | Git hygiene | Repo ignores, license placeholder. |
| 1 | P1·C2 | Packaging skeleton | pyproject + requirements. |
| 2 | P2·C1 | Config loader | YAML + defaults. |
| 2 | P2·C2 | Logger | Structured UTC logs. |
| 3 | P3·C1 | RNG module | Reproducible seeds. |
| 4 | P4·C1 | Bundle IO | Safe unzip/rezip. |
| 5 | P5·C1 | Models | Dataclasses for core schemas. |
| 6 | P6·C1 | CLI skeleton | argparse and no-op round-trip. |
| 7 | P7·C1 | Pytest & CI | green baseline. |
| 8 | P8·C1 | Docs polish | example bundle and quickstart. |

### Exit Criteria
- All utilities tested and deterministic.  
- CI pipeline green.  
- No behavior tied to CSC internals.  
- Ready to integrate with final spec for Phase 9.

