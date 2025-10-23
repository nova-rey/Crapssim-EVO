# CrapsSim-Evo Roadmap

Development begins after CSC spec + bundle module finalize.

## Phase 0 — Preparation
- Create repo and baseline docs (this commit).
- Wait for CSC bundle I/O to stabilize.

## Phase 1 — Skeleton & Config Loader
- Build repo scaffolding, YAML config parser, logging setup.

## Phase 2 — Fitness Engine
- Parse CSC journals, compute EV, drawdown, PSO, etc.

## Phase 3 — LEAP Pipeline
- Implement normal + wildcard pipelines with mutation/crossover operators.

## Phase 4 — LoS Metric
- Compute Level of Stagnation; trigger Wildcard mode.

## Phase 5 — Manifests & Export
- Emit population manifests and per-candidate DNA updates.

## Phase 6 — Baseline & Integration
- Run seeded integration with CSC bundles.
- Tag release `v0.10.0-phase6-baseline`.

### Guardrails
- Deterministic RNG only.
- One reversible commit per checkpoint.
- Schema versions logged in all artifacts.
