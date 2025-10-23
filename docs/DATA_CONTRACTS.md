# Data Contracts

## 1. spec.json (v1.0)
Canonical strategy definition; only file CSC reads.
```json
{
  "schema_version": "1.0",
  "profile_id": "contra_cruise",
  "params": {"place_6_8":24,"place_5_9":20,"odds_multiple":3},
  "toggles": {"bubble_mode": false},
  "identity": {
    "source": "evolver",
    "seed_hash": "a1f3…",
    "gen_id": "g002",
    "candidate_id": "seed_0001"
  }
}

2. dna.json (v0.1)

Lineage and mutation info; ignored by CSC.

{
  "evo_schema_version": "0.1",
  "gen_id": "g002",
  "candidate_id": "seed_0001",
  "mode": "WILDCARD",
  "parents": [{"seed_hash":"b7e2…"},{"seed_hash":"c9aa…"}],
  "ops": ["cx_hybrid","mut_nudge"],
  "rng": {"run_seed":1729,"ops":{"cx":101,"mut":102}},
  "trial_cohort": true,
  "grace_remaining": 2,
  "hashes": {"spec_sha256":"a1f3…","dna_sha256":"4c21…"}
}

3. fitness.json (optional)

Cached metrics for dashboards.

4. population_manifest.json (v0.1)

Generation index.

{
  "gen_id":"g002",
  "mode":"WILDCARD",
  "los":83.4,
  "trigger":"meh_counter>=8",
  "pop_size":120,
  "elite_k":12,
  "objectives":["ev","drawdown","pso_rate"],
  "candidates":[
    {"id":"seed_0001","spec_sha256":"a1f3…","dna_sha256":"4c21…"}
  ]
}
