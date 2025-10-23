# CrapsSim-Evo — Pre-Spec Development Roadmap

## Phase 0 — Documentation Seed ✅
- Created baseline docs and project structure.

---

## Phase 1 — Infrastructure & Tooling
**Goal:** establish base environment and repo hygiene.

| Checkpoint | Title | Summary |
|-------------|--------|----------|
| P1·C1 | Git hygiene | Add `.gitignore`, LICENSE placeholder. |
| P1·C2 | Packaging skeleton | `pyproject.toml`, `requirements.txt`, metadata. |
| P1·C3 | Lint/format setup | Ruff / Black config optional. |

**Exit:** repo installs locally; deps resolve.

---

## Phase 2 — Config & Logging
**Goal:** load YAML configs and structured logs.

| Checkpoint | Title | Summary |
|-------------|--------|----------|
| P2·C1 | Config loader | Load/merge YAML, defaults, env overrides. |
| P2·C2 | Logger | UTC timestamps, file/stdout, verbosity levels. |
| P2·C3 | Docs | `CONFIG_GUIDE.md` for key structure. |

**Exit:** `load_config()` + logging verified by tests.

---

## Phase 3 — Deterministic RNG Utilities
**Goal:** reproducible seeding framework.

| Checkpoint | Title | Summary |
|-------------|--------|----------|
| P3·C1 | RNG module | `seed_global`, `subseed`, `hash_dict`. |
| P3·C2 | Tests | Confirm repeatability & stable subseeds. |

---

## Phase 4 — Bundle I/O Skeleton
**Goal:** safe unzip/re-zip preserving unknown files.

| Checkpoint | Title | Summary |
|-------------|--------|----------|
| P4·C1 | Unbox | Safe extraction to staging dir. |
| P4·C2 | Rebox | Preserve all files; repack to zip. |
| P4·C3 | Checksums & index | Compute SHA256 + CONTENTS.json. |
| P4·C4 | Tests | Round-trip & zip-slip rejection. |

---

## Phase 5 — Data Models (Stubbed)
**Goal:** typed placeholders for future schemas.

| Checkpoint | Title | Summary |
|-------------|--------|----------|
| P5·C1 | Models | Dataclasses for Spec, DNA, Manifest, BundleMeta. |
| P5·C2 | (De)serializers | Load/dump JSON stable order. |
| P5·C3 | Tests | Round-trip equality, stable hashes. |

---

## Phase 6 — CLI Skeleton
**Goal:** minimal CLI and argument handling.

| Checkpoint | Title | Summary |
|-------------|--------|----------|
| P6·C1 | CLI entrypoint | argparse for `--config`, `--bundle-in/out`, `--verbose`. |
| P6·C2 | Wiring | Hook config + bundle round-trip no-op. |

---

## Phase 7 — Test Harness & CI
**Goal:** automated testing baseline.

| Checkpoint | Title | Summary |
|-------------|--------|----------|
| P7·C1 | Pytest scaffolding | tests for config, rng, bundles, models. |
| P7·C2 | CI workflow | GH Actions for tests + caching. |

---

## Phase 8 — Docs & Examples
**Goal:** polish developer UX.

| Checkpoint | Title | Summary |
|-------------|--------|----------|
| P8·C1 | Example bundle | Add tiny dummy + README. |
| P8·C2 | Update docs | Quickstart + contributing guide. |

---

### Guardrails
- One reversible commit per checkpoint.  
- No CSC schema assumptions.  
- Deterministic outputs only.  
- Minimal dependencies.  
- Phase tags: `v0.0.1` → `v0.0.8`.

