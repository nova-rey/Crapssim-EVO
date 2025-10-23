# Contributing

Thanks for helping build CrapsSim-Evo.

## Commit & PR Etiquette
- **One checkpoint = one reversible commit.**
- Keep commits focused; avoid mixing refactors and new features.
- Ensure `pytest -q` is green before opening a PR.

## Style & Hygiene
- Line endings are **LF** (enforced via `.gitattributes`).
- Use UTF-8, trim trailing whitespace, and final newline (see `.editorconfig`).
- Prefer Python 3.11+ features where reasonable.

## CI & Tests
- Add or update tests alongside code changes.
- Determinism matters: seed RNGs in tests when applicable.

## Roadmaps
- `docs/PHASE_ROADMAP.md` may be overwritten at each Phase C0.
- `docs/EVO_BIBLE.md` is **append-only**; add a short factual entry for major decisions.
