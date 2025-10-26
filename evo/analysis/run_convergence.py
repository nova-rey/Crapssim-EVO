from __future__ import annotations

from pathlib import Path
from typing import List

from .convergence import GenRollup, compute_rollup
from .reader import (
    iter_seed_dirs,
    link_prev_results,
    list_generation_dirs,
    read_dna,
    read_fitness,
    read_population_manifest,
)
from .reporters import (
    write_convergence_csv,
    write_convergence_json,
    write_operator_stats,
)


def run_for_root(root: Path, window: int = 5) -> None:
    gens = list_generation_dirs(root)
    if not gens:
        return
    rollups: List[GenRollup] = []
    skipped: List[str] = []
    for i, gen_dir in enumerate(gens):
        manifest = read_population_manifest(gen_dir)
        prev_results = link_prev_results(gen_dir)
        fitness_scores: List[float] = []
        rois: List[float] = []
        drawdowns: List[float] = []
        dnas = []
        for seed_dir in iter_seed_dirs(gen_dir):
            dnas.append(read_dna(seed_dir))
            if not prev_results:
                continue
            seed_id = seed_dir.name
            fit = read_fitness(prev_results, seed_id)
            if fit:
                fitness_score = fit.get("fitness_score")
                if isinstance(fitness_score, (int, float)):
                    fitness_scores.append(float(fitness_score))
                roi = fit.get("roi")
                if isinstance(roi, (int, float)):
                    rois.append(float(roi))
                drawdown = fit.get("drawdown_max")
                if isinstance(drawdown, (int, float)):
                    drawdowns.append(float(drawdown))
        if not prev_results:
            skipped.append(gen_dir.name)

        rollups.append(
            compute_rollup(
                gen_id=gen_dir.name,
                fitness_scores=fitness_scores,
                rois=rois,
                drawdowns=drawdowns,
                diversity=manifest.get("diversity"),
                los=(manifest.get("adaptive") or {}).get("los"),
                mode=manifest.get("mode"),
            )
        )

        if i == len(gens) - 1:
            write_operator_stats(gen_dir, dnas)

    current = gens[-1]
    write_convergence_json(current, rollups, window=window, skipped=skipped)
    write_convergence_csv(current, rollups)
