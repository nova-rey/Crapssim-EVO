# DNA & Lineage (v0.2)

Phase 7 introduces stronger lineage tracking for evolver outputs.

## Schema Additions
```json
{
  "evo_schema_version": "0.2",
  "parents": ["seed_0001", "seed_0002"],
  "parent_hashes": {
    "seed_0001": "<sha256-of-seed_0001-spec.json>",
    "seed_0002": "<sha256-of-seed_0002-spec.json>"
  },
  "ops_log": [{"type": "mutation", "nudge_frac": 0.1, "t": 0}],
  "rng_subseed": 90123,
  "identity": {"source": "evolver", "gen_id": "g003", "candidate_id": "seed_0007"}
}
```

### Population Manifest Version
Each generation bundle includes a population_manifest.json whose top-level field
"pop_schema_version": "0.2" distinguishes population metadata from DNA schema.

Parent Hashes
- Computed as SHA256 of each parent’s spec.json bytes.
- Stored under parent_hashes keyed by seed id (stable sorted order).
- Enables later verification of any lineage path.

Ops Log
- Structured list of dictionaries: {"type": "...", ..., "t": N}.
- Legacy string entries are normalized on write.

RNG Subseed
- Deterministic per individual using generation label and stable index.
- Guarantees replayability for any stochastic operator.

Elites Clarification
- Elites’ spec.json is preserved byte-for-byte.
- Identity breadcrumbs for elites live only in dna.json.

Compatibility
- Reads legacy ops_log strings and converts them to structured entries.
- evo_schema_version bumped from 0.1 to 0.2.
