from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Dict, List, Optional


@dataclass
class GenRollup:
    gen_id: str
    ef_top1: Optional[float]
    ef_top5_mean: Optional[float]
    ef_top10_mean: Optional[float]
    roi_mean: Optional[float]
    drawdown_mean: Optional[float]
    diversity: Optional[float]
    los: Optional[float]
    mode: Optional[str]
    skipped: bool = False


def _safe_mean(xs: List[float]) -> Optional[float]:
    return None if not xs else float(mean(xs))


def _least_squares_slope(y: List[float]) -> Optional[float]:
    """Slope over x = 0..n-1; return None for n<2; deterministic."""
    n = len(y)
    if n < 2:
        return None
    x_mean = (n - 1) / 2.0
    y_mean = mean(y)
    num = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(y))
    den = sum((i - x_mean) ** 2 for i in range(n))
    return float(num / den) if den else 0.0


def compute_rollup(
    gen_id: str,
    fitness_scores: List[float],
    rois: List[float],
    drawdowns: List[float],
    diversity: Optional[float],
    los: Optional[float],
    mode: Optional[str],
) -> GenRollup:
    scores = sorted(fitness_scores, reverse=True)
    top1 = scores[0] if scores else None
    k5 = scores[: min(5, len(scores))]
    k10 = scores[: min(10, len(scores))]
    return GenRollup(
        gen_id=gen_id,
        ef_top1=top1,
        ef_top5_mean=_safe_mean(k5),
        ef_top10_mean=_safe_mean(k10),
        roi_mean=_safe_mean(rois),
        drawdown_mean=_safe_mean(drawdowns),
        diversity=diversity,
        los=los,
        mode=mode,
    )


def compute_trends(gens: List[GenRollup], window: int = 5) -> Dict:
    """Compute slope/volatility/plateau over the last N (default 5) generations."""
    tail = gens[-window:] if gens else []
    ef_series = [g.ef_top5_mean for g in tail if g.ef_top5_mean is not None]
    if len(ef_series) < 2:
        return {"ef_slope": None, "best_plateau_len": 0, "volatility": None}

    slope = _least_squares_slope(ef_series)

    best = max(ef_series)
    best_idx = max(i for i, v in enumerate(ef_series) if v == best)
    plateau = len(ef_series) - 1 - best_idx

    vol = pstdev(ef_series) if len(ef_series) > 1 else 0.0
    return {
        "ef_slope": None if slope is None else round(slope, 6),
        "best_plateau_len": int(plateau),
        "volatility": round(float(vol), 6),
    }
