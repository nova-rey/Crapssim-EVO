# Pipeline Flow

## Conveyor Belt

[Evolver] → bundle_in.zip → [CSC Simulator] → bundle_out.zip → [Evolver]

### 1️⃣ Evo → CSC
- Evo builds a generation bundle (`g002_input.zip`).
- Each seed has `spec.json` + `dna.json`.
- Bundle includes `population_manifest.json`.

### 2️⃣ CSC → Evo
- CSC unboxes bundle.
- Runs each `spec.json`.
- Produces `journal.csv`, `report.json`, `manifest.json`.
- Re-boxes all output into `g002_results.zip`.

### 3️⃣ Evo Grades
- Unboxes `g002_results.zip`.
- Verifies checksums and schema versions.
- Reads journals → computes fitness.
- Updates `dna.json` and population manifest.
- Exports next gen `g003_input.zip`.

### 4️⃣ Repeat
Loop continues until convergence or manual stop.

### RNG & Metadata
- Evo assigns new RNG seeds per generation.
- CSC logs its own run seeds for reproducibility.
- Both write manifests with schema and hash fields.
