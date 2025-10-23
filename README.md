# CrapsSim-Evo

CrapsSim-Evo is an autonomous evolutionary engine for optimizing craps betting strategies.  
It lives in its own sandbox and communicates with **CrapsSim-Control (CSC)** entirely through `.zip` bundles.  
Each generation of strategies (“seeds”) is evolved, tested in CSC, and returned for grading and reproduction.

## 🧭 Purpose
- Automate strategy improvement using fitness derived from CSC journals.
- Maintain strict determinism and reproducibility.
- Keep simulation (CSC) and evolution (Evo) fully decoupled.

## 🔁 Conveyor Loop

[Evolver] → bundle_in.zip → [CSC Simulator] → bundle_out.zip → [Evolver]

## 📦 Artifacts
- **spec.json** — playable strategy for CSC.
- **dna.json** — lineage and mutation record (evolver only).
- **journal.csv / report.json / manifest.json** — produced by CSC.
- **population_manifest.json** — per-generation index.
- **bundle.zip** — transport container holding everything above.

## 📅 Status
Planning stage. Implementation begins after CSC spec and bundle module are finalized.
