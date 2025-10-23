# Architecture

## Technology
- **Language:** Python 3.11+
- **Evolution Library:** [LEAP](https://github.com/AureumChaos/LEAP)
- **Packaging:** `.zip` bundles for input/output
- **No external DB:** all state is manifest-driven on disk.

## Planned Layout

evo/
fitness.py
genome.py
pipeline.py
stagnation.py
ops_standard.py
ops_wildcard.py
manifests.py
io.py
cli/
evolve.py
configs/
example.yml
tests/
…
docs/
…

## Module Roles
- **fitness.py** — parse CSC logs, compute EV, drawdown, PSO, etc.  
- **genome.py** — encode/decode spec JSONs; enforce bounds, repair.  
- **pipeline.py** — assemble LEAP pipeline; switch between normal and wildcard modes.  
- **stagnation.py** — compute LoS and trigger rules.  
- **ops_standard / ops_wildcard.py** — crossover and mutation operators.  
- **manifests.py** — create population and run manifests.  
- **io.py** — handle `.zip` extraction, validation, and writing.

## Determinism Rules
- One run-level RNG seed + sub-seeds per operator.
- All seeds, ops, and hashes logged to manifest.
- Identical bundle + config ⇒ identical next generation.
