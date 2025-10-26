from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List

from .convergence import GenRollup, compute_trends


def write_convergence_json(
    out_dir: Path, gens: List[GenRollup], window: int, skipped: List[str]
) -> Path:
    payload = {
        "schema_version": "1.0",
        "window": int(window),
        "gens": [
            {
                "gen_id": g.gen_id,
                "ef_top1": g.ef_top1,
                "ef_top5_mean": g.ef_top5_mean,
                "ef_top10_mean": g.ef_top10_mean,
                "roi_mean": g.roi_mean,
                "drawdown_mean": g.drawdown_mean,
                "diversity": g.diversity,
                "los": g.los,
                "mode": g.mode,
            }
            for g in gens
        ],
        "trends": compute_trends(gens, window=window),
        "skipped": skipped,
    }
    path = out_dir / "convergence.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_convergence_csv(out_dir: Path, gens: List[GenRollup]) -> Path:
    path = out_dir / "convergence.csv"
    cols = [
        "gen_id",
        "ef_top1",
        "ef_top5_mean",
        "ef_top10_mean",
        "roi_mean",
        "drawdown_mean",
        "diversity",
        "los",
        "mode",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for g in gens:
            writer.writerow(
                {
                    "gen_id": g.gen_id,
                    "ef_top1": g.ef_top1,
                    "ef_top5_mean": g.ef_top5_mean,
                    "ef_top10_mean": g.ef_top10_mean,
                    "roi_mean": g.roi_mean,
                    "drawdown_mean": g.drawdown_mean,
                    "diversity": g.diversity,
                    "los": g.los,
                    "mode": g.mode,
                }
            )
    return path


def operator_stats_for_gen(seed_dnas: Iterable[Dict]) -> Dict:
    """
    Approximate operator efficacy by counting op presence by surviving rank.
    We track raw counts and normalized rates; simple and deterministic.
    """
    counts = Counter()
    for dna in seed_dnas:
        for entry in dna.get("ops_log", []):
            label = entry.get("type") or entry.get("label") or "op"
            counts[label] += 1
    total = sum(counts.values()) or 1
    rates = {k: v / total for k, v in counts.items()}
    return {"counts": dict(counts), "rates": rates}


def write_operator_stats(out_dir: Path, seed_dnas: Iterable[Dict]) -> Path:
    stats = operator_stats_for_gen(seed_dnas)
    path = out_dir / "operator_stats.json"
    path.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    return path
