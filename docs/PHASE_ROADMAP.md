# CrapsSim-Evo — Active Phase Plan

## Current Phase: 1 — Infrastructure & Tooling

### Objective
Initialize repo hygiene, packaging, and base scaffolding. No runtime behavior.

### Checkpoints
| Phase | Checkpoint | Title | Outcome |
|------:|------------|-------|---------|
| 1 | P1·C1 | Git hygiene | Add .gitattributes, .editorconfig, full MIT LICENSE, refreshed .gitignore. |
| 1 | P1·C2 | Packaging skeleton | pyproject (0.0.1), console script, optional deps, requirements. |
| 1 | P1·C3 | Lint & format setup | Ruff config, Black settings, CI lint job. |

### Exit Criteria
- `pip install -e .` succeeds.
- `pytest -q` passes existing tests.
- `ruff check .` passes locally and in CI.
- `black --check .` passes locally and in CI.
- Repo structure matches planned layout.
