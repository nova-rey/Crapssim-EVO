# CrapsSim-Evo Bible (Append-Only)

## Entry — 2025-10-23 · Pre-Spec Planning
- Decision: base evolution library will be **LEAP** for reproducibility and manifest-based pipelines.
- CrapsSim-Evo remains a **silo**; it only exchanges `.zip` bundles with CSC.
- Bundles chosen as `.zip` (not `.tar.zst`) for simplicity since file sizes are small.
- Each bundle carries a `meta/bundle.json` shipping label and SHA256 checksums.
- DNA stored as a **separate file** alongside `spec.json`, not embedded inside.
- Evolver exports generation directories with:
  - `spec.json`
  - `dna.json`
  - optional `fitness.json`
  - `population_manifest.json`
- CSC consumes the same bundle format, adds journals/reports/manifests, and returns another zip.
- The conveyor loop:  

[Evolver] → bundle_in.zip → [CSC] → bundle_out.zip → [Evolver]

- Development will begin with infrastructure, config, deterministic RNG, and bundle I/O; all independent of CSC internals.
- Phases 1–8 define “safe” groundwork that will not require rework once the spec locks.

---

*(All future major decisions append below; never overwrite prior entries.)*


## Entry — Phase 1 Kickoff (Infrastructure & Tooling)
- Added repo hygiene files, packaging skeleton, and empty module scaffolding.
- Established Python 3.11 baseline, editable install, and CLI entry point stub.
- No runtime behavior added; this phase is foundational only.

## Entry — P1·C1 Git Hygiene
- Added `.gitattributes` to enforce LF line endings and mark binary types.
- Added `.editorconfig` for consistent indentation, encoding, and whitespace rules.
- Replaced placeholder `LICENSE` with full MIT text.
- Overwrote `.gitignore` with a comprehensive Python/project superset.
- No runtime behavior changed.

## Entry — P1·C3 Lint & Format Setup
- Added `ruff.toml` with Python 3.11 target, 100 line length, and import-order checks.
- Created CI workflow to run `ruff check` and `black --check` on pushes and PRs.
- Formatting standardized with Black (line length 100). No runtime behavior changed.

## Entry — P2·C0 Config & Logging Phase Kickoff
- Began Phase 2 focused on configuration and logging infrastructure.
- Established plan for YAML-based config loader with default merging and environment variable expansion.
- Planned structured UTC logging setup (console-only, idempotent).
- Added `docs/CONFIG_GUIDE.md` outlining design and usage examples.

## Entry — P2·C1 Config Loader
- Implemented `load_config()` in `evo/config.py` to load YAML, merge defaults, and expand environment variables.
- Added recursive env-var substitution for `${VAR}` patterns.
- Ensured defaults always applied: `run_id`, `logging.level`, `seed`.
- Updated `configs/example.yml` with a realistic testable configuration.
- Added unit tests for defaults, env expansion, and normalization.

## Entry — P2·C2 Logger Implementation
- Implemented idempotent console logger with UTC timestamps and consistent format.
- Default level INFO; supports DEBUG, WARNING, ERROR, CRITICAL.
- Prevents duplicate handlers when re-initialized.
- Added unit tests confirming format, idempotency, and level filtering.

## Entry — P2·C3 Docs & Tests Wrap-Up
- Phase 2 complete: Config loader and logger confirmed stable.
- Added verified behavior section to `CONFIG_GUIDE.md`.
- All unit tests green and CI lint clean (Ruff + Black).
- Ready for Phase 3 (deterministic RNG utilities).
- Tagged baseline `v0.0.2-phase2-baseline`.

## Entry — Phase 3 Deterministic RNG Utilities
- Introduced reproducible RNG framework with `seed_global`, `make_subseed`, and `rng_context`.
- Added SHA256-based `hash_bytes` and `hash_dict` utilities.
- All functions deterministic across runs and platforms.
- Tests confirm RNG isolation, repeatability, and hash stability.
- Repo verified lint- and format-clean (Ruff + Black).
- Baseline tagged `v0.0.3-phase3-baseline`.

## Entry — Phase 4 Bundle I/O & Manifest
- Implemented safe `.zip` extraction and repacking with integrity checks.
- Added checksum and contents index generation.
- Introduced `meta/bundle.json` manifest (bundle_schema_version 1.0).
- Enforced zip-slip guard and pass-through of unknown files.
- Tests verify round-trip preservation, validation, and checksum accuracy.
- Repo verified Ruff + Black clean.
- Tagged baseline `v0.0.4-phase4-baseline`.

## Entry — Phase 4 Wrap-Up
- Completed Bundle I/O & Manifest phase.
- All bundle utilities verified via unit tests and round-trip integrity.
- Updated roadmap to mark Phase 4 complete.
- Repo ready for Phase 5 (Fitness & Metrics Framework).
- Lint and format confirmed clean (Ruff + Black).

## Entry — Phase 5 Fitness & Metrics Framework
- Added report and journal parsers for CSC bundle outputs.
- Introduced metrics registry (`roi`, `drawdown`, `pso_rate`) with decorator pattern.
- Implemented `compute_fitness()` producing deterministic `fitness.json` per seed.
- Added tests covering ROI, drawdown, PSO, and fallback logic.
- Documented scoring formula in `FITNESS_GUIDE.md`.
- Verified Ruff + Black clean; tagged baseline `v0.0.5-phase5-baseline`.
