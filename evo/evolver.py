from __future__ import annotations

import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any, Dict, List

from .dna import build_parent_hashes, make_rng_subseed, update_dna
from .io.export import write_generation_folder
from .metrics.diversity import diversity_index
from .mutation import crossover_individuals, mutate_individual
from .policy.adaptive import ADAPTIVE
from .population import Individual, load_individual_from_run
from .rng import rng_context
from .selection import elitism, tournament

METRICS_CACHE: Dict[str, Any] = {}


def _make_fitness_snapshot(pop: List[Individual]) -> list[dict[str, Any]]:
    snapshot: list[dict[str, Any]] = []
    for ind in pop:
        spec_blob = json.dumps(ind.spec, sort_keys=True)
        spec_hash = hashlib.sha1(spec_blob.encode("utf-8")).hexdigest()
        snapshot.append({"fitness_score": ind.fitness, "spec_hash": spec_hash})
    return snapshot


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

    fitness_results = _make_fitness_snapshot(current)
    prev_topk = METRICS_CACHE.get("prev_topk", [])
    topk_limit = max(1, len(fitness_results) // 10) if fitness_results else 0
    curr_topk = (
        sorted((r["fitness_score"] for r in fitness_results), reverse=True)[:topk_limit]
        if topk_limit
        else []
    )
    diversity = diversity_index(fitness_results) if fitness_results else 0.0
    ADAPTIVE.update(prev_topk, curr_topk, diversity)
    METRICS_CACHE["prev_topk"] = curr_topk
    mode_snapshot = ADAPTIVE.snapshot()
    grace_info = {
        "enabled": ADAPTIVE.mode == "WILDCARD",
        "grace_remaining": 2 if ADAPTIVE.mode == "WILDCARD" else 0,
    }

    if pop_size == 0:
        return []

    elite_k = max(1, math.floor(pop_size * elite_ratio))
    elites = elitism(current, elite_k)
    elite_ids = {e.seed_id for e in elites}

    elite_info: list[tuple[Individual, list[dict[str, Any]]]] = [(elite, []) for elite in elites]
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
                base_nudge = 0.1 if roll < cx_prob + mut_prob else 0.05
                child = mutate_individual(parent, nudge_frac=base_nudge)
                actual_nudge = base_nudge * 2.5 if ADAPTIVE.mode == "WILDCARD" else base_nudge
                op_entries = [
                    {
                        "type": "mutation",
                        "nudge_frac": actual_nudge,
                        "mode": ADAPTIVE.mode,
                    }
                ]
            child.seed_id = "TBD"
            child.generation = int(gen_id.strip("g") or "0") + 1
            child.fitness = 0.0
            offspring.append((child, op_entries))

    next_gen_label = f"g{int(gen_id.strip('g') or '0')+1}"
    combined: list[tuple[Individual, list[dict[str, Any]]]] = elite_info + offspring

    next_pop: List[Individual] = []
    for idx, (candidate, op_entries) in enumerate(combined, start=1):
        parent_specs: list[tuple[str, Path]] = []
        for pid in candidate.parents[:2] if candidate.parents else []:
            ppath = results_root / pid / "spec.json"
            if ppath.exists():
                parent_specs.append((pid, ppath))
        parent_hashes = build_parent_hashes(parent_specs)
        rng_subseed = make_rng_subseed(next_gen_label, idx, root_seed)
        candidate_id = f"seed_{idx:04d}"
        candidate.dna = update_dna(
            candidate.dna,
            gen_id=next_gen_label,
            candidate_id=candidate_id,
            parents=candidate.parents if candidate.parents else [],
            parent_hashes=parent_hashes,
            rng_subseed=rng_subseed,
            op_entries=op_entries,
        )
        if candidate.seed_id not in elite_ids:
            candidate.seed_id = candidate_id
        next_pop.append(candidate)

    manifest_overrides = {"adaptive": mode_snapshot, "grace": grace_info}
    write_generation_folder(
        out_dir,
        gen_id=next_gen_label,
        individuals=next_pop,
        elite_ids=elite_ids,
        manifest_overrides=manifest_overrides,
    )
    return next_pop
