from __future__ import annotations

import math
import random
from pathlib import Path
from typing import Any, List

from .dna import build_parent_hashes, make_rng_subseed, update_dna
from .io.export import write_generation_folder
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

    offspring: list[tuple[Individual, list[dict[str, Any]]]] = []
    with rng_context("evolution", root_seed):
        while len(offspring) < (pop_size - elite_k):
            roll = random.random()
            if len(current) >= 2 and roll < cx_prob:
                a = tournament(current, k=3)
                b = tournament(current, k=3)
                if a.seed_id == b.seed_id:
                    b = tournament(current, k=3)
                child = crossover_individuals(a, b)
                op_entries = [{"type": "crossover", "mode": "blocks"}]
            else:
                parent = tournament(current, k=3)
                nudge = 0.1 if roll < cx_prob + mut_prob else 0.05
                child = mutate_individual(parent, nudge_frac=nudge)
                op_entries = [{"type": "mutation", "nudge_frac": nudge}]
            child.seed_id = "TBD"
            child.generation = int(gen_id.strip("g") or "0") + 1
            child.fitness = 0.0
            offspring.append((child, op_entries))

    next_pop: List[Individual] = []
    next_pop.extend(elites)
    next_gen_label = f"g{int(gen_id.strip('g') or '0')+1}"
    for idx, (child, op_entries) in enumerate(offspring, start=1):
        parent_specs: list[tuple[str, Path]] = []
        for pid in child.parents[:2] if child.parents else []:
            ppath = results_root / pid / "spec.json"
            if ppath.exists():
                parent_specs.append((pid, ppath))
        parent_hashes = build_parent_hashes(parent_specs)
        rng_subseed = make_rng_subseed(next_gen_label, idx, root_seed)
        candidate_id = f"seed_{idx:04d}"
        child.dna = update_dna(
            child.dna,
            gen_id=next_gen_label,
            candidate_id=candidate_id,
            parents=child.parents if child.parents else [],
            parent_hashes=parent_hashes,
            rng_subseed=rng_subseed,
            op_entries=op_entries,
        )
        next_pop.append(child)

    write_generation_folder(
        out_dir,
        gen_id=next_gen_label,
        individuals=next_pop,
        elite_ids=elite_ids,
    )
    return next_pop
