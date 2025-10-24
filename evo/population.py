from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict


@dataclass
class Individual:
    seed_id: str
    generation: int
    spec: Dict[str, Any]
    dna: Dict[str, Any]
    fitness: float
    parents: list[str] = field(default_factory=list)

    def clone(self) -> "Individual":
        return Individual(
            seed_id=self.seed_id,
            generation=self.generation,
            spec=copy.deepcopy(self.spec),
            dna=copy.deepcopy(self.dna),
            fitness=self.fitness,
            parents=list(self.parents),
        )


def load_individual_from_run(run_seed_dir: Path, generation: int) -> Individual:
    seed_id = run_seed_dir.name
    spec = json.loads((run_seed_dir.parent.parent / seed_id / "spec.json").read_text())
    dna_path = run_seed_dir.parent.parent / seed_id / "dna.json"
    dna = json.loads(dna_path.read_text()) if dna_path.exists() else {"evo_schema_version": "0.1"}
    fitness_json = json.loads((run_seed_dir / "fitness.json").read_text())
    fitness = float(fitness_json.get("fitness_score", 0.0))
    return Individual(seed_id=seed_id, generation=generation, spec=spec, dna=dna, fitness=fitness)
