# Overview

CrapsSim-Evo is a standalone evolutionary system that breeds craps strategy specifications for CrapsSim-Control (CSC).  
It reads CSC result bundles, grades fitness, and generates new seeds to test.

## Core Ideas
- **Isolation:** Evo and CSC communicate only through `.zip` bundles.
- **Determinism:** identical seeds and RNGs always produce identical outcomes.
- **Schema Discipline:** every artifact carries an explicit version tag.
- **Reproducibility:** manifests and hashes allow bit-for-bit replay.

## Key Terms
| Term | Meaning |
|------|----------|
| **Seed / Spec** | One playable strategy definition. |
| **DNA** | Lineage + mutation history for a seed. |
| **Generation** | A complete population of seeds. |
| **LoS (Level of Stagnation)** | Metric deciding when to trigger Wildcard generations. |
| **Wildcard Generation** | A mutation burst when evolution stalls. |
| **Elite / Grace** | Top performers preserved or immune from culling. |

Evo’s job: **analyze journals → compute fitness → evolve → emit next gen.**
