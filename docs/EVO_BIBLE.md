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

