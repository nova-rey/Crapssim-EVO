# CSC Interface Contract

This defines what CrapsSim-Control (CSC) must support for evolutionary integration.

## Required CSC Outputs
Each run must emit:
- `journal.csv` — canonical roll-by-roll data.
- `report.json` — aggregate results (EV, drawdown, PSO, etc.).
- `manifest.json` — run metadata (schema versions, RNG seeds).
- `spec.json` — the executed seed spec.

## Early Stop Flags
CSC should write:
```json
"early_stop_reason": "bankrupt" | "min_bet_unaffordable" | null

Bundle I/O

CSC gains two CLI flags:

--from-bundle <path.zip>
--bundle-out <path.zip>

These invoke the internal bundles.py module.

Input Layout (from Evo)

/population_manifest.json
/seed_*/spec.json
/seed_*/dna.json

Output Layout (to Evo)

/seed_*/spec.json
/seed_*/dna.json
/run/seed_*/journal.csv
/run/seed_*/report.json
/run/seed_*/manifest.json
/run/checksums.txt
/run/CONTENTS.json
/meta/bundle.json

bundles.py Responsibilities
	•	Safe unzip → staging dir.
	•	Validate presence of seeds/specs.
	•	Preserve unknown files verbatim.
	•	Copy simulation artifacts into /run/.
	•	Compute SHA256 checksums + index.
	•	Repack as .zip.

Validation Rules
	•	Raise error on missing spec.json.
	•	Preserve any unrecognized files.
	•	Never write outside the staging root (zip-slip guard).
	•	Record all schema versions and RNG seeds.

Reproducibility

Every bundle includes:
	•	bundle_schema_version
	•	SHA256 hashes for contents
	•	UTC timestamps
	•	RNG and spec hashes
