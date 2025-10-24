from __future__ import annotations

import math
import random
from pathlib import Path
from typing import List

from .mutation import crossover_individuals, mutate_individual
from .population import Individual, load_individual_from_run
from .rng import rng_context
from .selection import elitism, tournament


def load_population(results_root: Path, generation: int) -> List[Individual]:
    """Load individuals from /run/<seed_id>/ subfolders."""
    pop: List[Individual] = []
    run_dir = results_root / "run"
    for seed_dir in sorted(p for p in run_dir.iterdir() if p.is_dir()):
        pop.append(load_individual_from_run(seed_dir, generation))
    return pop


def evolve(
    results_root: Path,
    out_dir: Path,
    gen_id: str,
    root_seed: int,
    pop_size: int | None = None,
    elite_ratio: float = 0.1,
    cx_prob: float = 0.7,
    mut_prob: float = 0.3,
) -> List[Individual]:
    """Perform one evolutionary step to produce the next generation."""
    current = load_population(results_root, generation=int(gen_id.strip("g") or "0"))
    if pop_size is None:
        pop_size = len(current)
    elite_k = max(1, math.floor(pop_size * elite_ratio))
    elites = elitism(current, elite_k)
    elite_ids = {e.seed_id for e in elites}

    offspring: List[Individual] = []
    with rng_context("evolution", root_seed):
        while len(offspring) < (pop_size - elite_k):
            roll = random.random()
            if len(current) >= 2 and roll < cx_prob:
                a = tournament(current, k=3)
                b = tournament(current, k=3)
                if a.seed_id == b.seed_id:
                    b = tournament(current, k=3)
                child = crossover_individuals(a, b)
            else:
                parent = tournament(current, k=3)
                nudge = 0.1 if roll < cx_prob + mut_prob else 0.05
                child = mutate_individual(parent, nudge_frac=nudge)
            child.seed_id = "TBD"
            child.generation = int(gen_id.strip("g") or "0") + 1
            child.fitness = 0.0
            offspring.append(child)

    next_pop = elites + offspring
    for ind in next_pop:
        ind.dna.setdefault("lineage_note", f"g{ind.generation}")

    from .io.export import write_generation_folder

    write_generation_folder(
        out_dir,
        gen_id=f"g{int(gen_id.strip('g') or '0')+1}",
        individuals=next_pop,
        elite_ids=elite_ids,
    )
    return next_pop
