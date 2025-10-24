# Evolution Guide (Phase 6)

This guide describes the minimal evolutionary loop implemented in Phase 6.

## Loop Stages
1. **Load population** from CSC results: read `spec.json`, `dna.json`, and `fitness.json`.
2. **Selection** using tournament selection (k=3).
3. **Variation**
   - **Crossover** (≈70%): block-wise parameter/toggle mixing.
   - **Mutation** (≈30%): small bounded nudges with discrete snapping.
4. **Replacement** with **elitism** (top 10% preserved byte-for-byte).
5. **Export** next generation folder and bundle:

/g002/
/seed_0001/spec.json
/seed_0001/dna.json
population_manifest.json
(zipped as g002_input.zip when needed)

## Determinism
- All randomness flows through `rng_context("evolution", root_seed)`.
- Elites are copied first to stabilize ordering.
- Exporter rewrites `identity` breadcrumbs inside spec (safe for CSC to ignore).

## Operator Notes
- **Mutation**: ±10% nudges, snapped to table-friendly increments.
- **Crossover**: field-wise choose from either parent for `params` and `toggles`.
- **DNA**: `ops_log` is appended with operator names for traceability.

## Next Steps
- Phase 7 will deepen lineage tracking, add parent hashes, and better op metadata.
