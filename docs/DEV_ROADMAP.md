# CrapsSim-Evo — Development Roadmap (Data-Center Ready)

This document outlines the medium- to long-term roadmap for CrapsSim-Evo, focused on
making Evo a deterministic, lab-grade system suitable for long-running campaigns and
data-center deployment.

The roadmap assumes the current baseline includes:

- Deterministic DNA and lineage tracking
- Adaptive Level-of-Stagnation (LoS) metric and wildcard gens
- Convergence and operator statistics
- Deterministic bundling and interop manifests
- Dual-lane interop (file-drop + HTTP) for CSC integration

## Phase 12 — Spec & DNA Domain Split

**Goal:** Clean separation between structural and behavioral aspects of a strategy,
without changing runtime behavior.

- Introduce `spec.structural.*` for bets, amounts, odds, press/regress rules, and
  stop/goal thresholds.
- Introduce `spec.behavior.*` for future rule/DSL-based behavior.
- Split DNA into:
  - `ops_log_structural[]`
  - `ops_log_behavior[]`
  - `dna_schema_version: "0.3-split"`
- Add an export flattener that compiles `spec.structural` into the legacy flat spec
  that CSC understands today, ignoring behavior fields for now.
- Ensure exports remain backward-compatible and deterministic.

## Phase 13 — Structural Operator Pool v1

**Goal:** Make Evo very good at evolving the structural “shape” of a craps strategy.

- Define a `StructuralOps` registry for:
  - Numeric drift of units, odds, and thresholds with safe bounds
  - Categorical toggles for enabling/disabling bets
  - Adjustments to press/regress rules and stop/goal thresholds
- Enforce table legality by validating structural mutations against CSC’s rules
  (increments, max odds, etc.).
- Keep operator weights configurable in the main config.
- Maintain strict determinism: given the same parents and seeds, children are
  reproduced exactly.

## Phase 14 — Result Ingestion & Fitness Aggregator v2

**Goal:** Turn CSC outputs into a robust, multi-metric fitness score.

- Implement a results ingestion module that reads CSC outputs (e.g. `fitness.json`,
  `report.json`, and related artifacts).
- Compute generation-level metrics such as:
  - EF mean and EF top-k
  - ROI mean
  - Maximum and average drawdown
  - Optional PSO-related statistics
- Define a configurable `FitnessPolicy` that combines these metrics into a single
  fitness score.
- Feed the resulting fitness back into:
  - LoS computation
  - Operator statistics
  - Convergence and trend analysis

## Phase 15 — Evolution Orchestrator & Resilience

**Goal:** Evolve from “one-off runs” to a robust, resumable campaign engine.

- Introduce an evolution orchestrator that manages:
  - Populations and generations
  - Job submission to CSC
  - Per-individual status (pending/running/done/error)
- Add checkpointing of campaign state so Evo can recover from interruptions.
- Implement retry logic for transient errors (timeouts, HTTP 5xx), and clear
  classification of permanent failures (invalid spec, hash mismatch, etc.).
- Ensure a failed individual or CSC run does not wedge the entire campaign.

## Phase 16 — Behavior DNA & DSL Alignment (Evo-Side Only)

**Goal:** Prepare Evo to evolve behavioral rules once CSC’s DSL is ready, without
executing behavior locally.

- Define a `behavior.rules[]` schema that mirrors CSC’s DSL surface.
- Implement a `BehaviorOps` registry for:
  - Adjusting thresholds and conditions in rules
  - Swapping verbs within an allowed set
  - Adding/removing rules (with caps to avoid rule bloat)
- Add a strong validator so mutated behaviors are always syntactically valid.
- Keep behavioral evolution disabled by default; treat behavior DNA as inert
  metadata until CSC advertises DSL support.

## Phase 17 — Behavior Execution Bridge

**Goal:** Turn behavioral DNA into actual behavior via CSC’s internal DSL.

- Add configuration to choose domain:
  - `structural`
  - `behavior`
  - `hybrid`
- When behavioral evolution is enabled:
  - Export `behavior.rules[]` to the spec as-is.
  - Check CSC capabilities; only rely on behavior when `capabilities.dsl == true`.
- Optionally ingest CSC decision journals (`decisions.jsonl`) for additional
  diagnostics and secondary metrics.

## Phase 18 — Multi-Lineage & Island Model Evolution

**Goal:** Support multiple populations and evolutionary “islands” in parallel.

- Introduce an experiment abstraction (e.g. `experiments/EXP001/`).
- Support multiple populations that evolve independently, with optional migration
  of elites between islands.
- Coordinate CSC workers across experiments subject to global limits on
  concurrency and resource usage.

## Phase 19 — Observability & Operations

**Goal:** Make Evo operable like a long-running service.

- Standardize on structured logging (e.g. JSON lines) with experiment, generation,
  and job identifiers.
- Expose metrics such as:
  - Generations completed
  - Jobs submitted/succeeded/failed
  - CSC latency and throughput
  - LoS and convergence trends
- Add simple dashboards or exported data suitable for external dashboards
  (e.g. Node-RED, Prometheus).

## Phase 20 — Version Freeze & LTS

**Goal:** Provide a stable long-term support baseline.

- Lock and document schema versions for:
  - Population and DNA
  - Export bundles and manifests
  - Interop formats
- Provide migration helpers for older populations and results.
- Tag a long-term support release (e.g. `v1.0.0-lts`) with clear compatibility
  and upgrade guarantees.
