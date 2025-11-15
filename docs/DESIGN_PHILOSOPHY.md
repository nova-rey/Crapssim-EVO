# CrapsSim-Evo — Design Philosophy

CrapsSim-Evo is an evolutionary harness for craps strategies. The goal is to
provide a deterministic, explainable, and composable system that can be trusted
for long-running experimentation and real-world decision-making.

This document captures the core design principles that guide implementation.

## 1. Determinism First

- Given the same inputs (specs, seeds, configuration and engine version),
  Evo must produce the same outputs.
- Randomness is confined to clearly identified RNGs with explicit seeding.
- Export bundles and manifests aim for byte-level stability when run in
  deterministic mode.
- Evolution campaigns should be replayable end-to-end, including:
  - DNA and lineage
  - Operator usage
  - Convergence metrics

## 2. Separation of Concerns

- **Evo** is responsible for strategy generation, mutation, selection, and
  high-level orchestration.
- **CSC** is responsible for simulating the craps table and enforcing table
  legality and rules.
- Behavior DSL execution lives inside CSC; Evo designs behaviors but never
  drives the engine at runtime.
- The boundaries between Evo and CSC are artifact-based:
  - Specs and bundles in
  - Logs, journals, and fitness summaries out

## 3. Structural vs Behavioral DNA

- Structural aspects of a strategy (bets, amounts, odds, press/regress rules,
  stop thresholds) are treated separately from behavioral aspects (IF/THEN
  rules, DSL sentences, and policy choices).
- Structural DNA defines the baseline “shape” of a strategy.
- Behavioral DNA defines how the strategy reacts to table state over time.
- Evo should be able to evolve:
  - Structural-only strategies
  - Behavioral-only strategies
  - Hybrid strategies (with explicit configuration and guardrails)

## 4. Explainable Evolution

- Every meaningful change to a strategy should be traceable through DNA:
  - Parent hashes
  - Operator logs
  - Mutation and crossover events
- Fitness calculations are based on transparent metrics (EF, ROI, drawdown,
  etc.) with documented weights.
- Convergence and operator statistics help explain why the population moved
  the way it did.

## 5. Safety and Guardrails

- Evo must never intentionally produce table-illegal configurations. All
  structural mutations pass through legality checks aligned with CSC.
- Behavior mutations must remain within the supported DSL grammar and verb
  set; invalid rules are rejected or sanitized before export.
- Evolutionary parameters are bounded:
  - Max mutation strength
  - Max number of behavior edits per child
  - Rate limits on wildcard or disruptive changes

## 6. Progressive Complexity

- The system should be useful early with simple, structural evolution only.
- Additional complexity (behavioral DSL, multi-lineage runs, island models)
  is layered in gradually, guided by stable interfaces and configuration.
- Features are introduced behind configuration flags with sane defaults.

## 7. Observability and Operations

- Long-running campaigns require visibility:
  - Structured logs for events and errors
  - Metrics for throughput and performance
  - Artifacts for convergence and trend analysis
- Evo should be operable both on a single workstation and in a data-center
  style environment with multiple workers.

## 8. Versioning and Compatibility

- Data formats (DNA, bundles, manifests, fitness summaries) have explicit,
  documented schema versions.
- Breaking changes are gated behind version bumps and, where practical,
  conversion tools.
- A long-term support line provides a stable base for external tools and
  integrations.

## 9. Human-Friendly Workflows

- Despite internal complexity, user-facing flows should remain simple:
  - Choose base strategies
  - Configure a campaign
  - Run evolution
  - Inspect winners and convergence
- Documentation should guide users from “first run” through more advanced
  experiments without requiring deep familiarity with internal internals.
