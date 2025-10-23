# CrapsSim-Evo — Active Phase Plan

## Current Phase: 1 — Infrastructure & Tooling

### Objective
Initialize repo hygiene, packaging, and base scaffolding. No runtime behavior.

### Checkpoints
| Phase | Checkpoint | Title | Outcome |
|------:|------------|-------|---------|
| 1 | P1·C1 | Git hygiene | Add .gitignore and LICENSE placeholder. |
| 1 | P1·C2 | Packaging skeleton | pyproject + requirements for editable install. |
| 1 | P1·C3 | Lint/format setup (optional) | Ruff/Black configs in pyproject. |

### Exit Criteria
- `pip install -e .` succeeds.
- `pytest -q` runs with no import errors.
- Repo structure matches planned layout.
