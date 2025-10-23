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
