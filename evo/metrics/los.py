from __future__ import annotations

from statistics import mean
from typing import List

# Scales normalized ΔEF to keep LoS sensitive to small EF changes.
# Tuned empirically; adjust in future phases if needed.
LOS_DELTA_SCALE = 16.0


def _safe_mean(xs: List[float]) -> float:
    return float(mean(xs)) if xs else 0.0


def compute_los(prev_topk: List[float], curr_topk: List[float], diversity: float) -> float:
    """
    Level of Stagnation (LoS): 0..100
      - Low (0–30): healthy
      - Mid (30–70): slowing
      - High (70–100): stagnation

    LoS blends (normalized EF drop) and (lack of diversity):
      LoS = 100 * (0.6 * ΔEF_norm + 0.4 * (1 - diversity_norm))

    Where:
      ΔEF_norm = clamp(
          (prev_mean - curr_mean) / max(|prev_mean|, |curr_mean|, 1e-9) * LOS_DELTA_SCALE,
          0,
          1,
      )
      diversity_norm = clamp(diversity, 0, 1)   # already 0..1 by design
    """
    if not prev_topk or not curr_topk:
        return 0.0

    prev_m = _safe_mean(prev_topk)
    curr_m = _safe_mean(curr_topk)
    delta = max(0.0, prev_m - curr_m)
    denom = max(abs(prev_m), abs(curr_m), 1e-9)

    delta_norm = min(max((delta / denom) * LOS_DELTA_SCALE, 0.0), 1.0)
    div_norm = min(max(diversity, 0.0), 1.0)

    los = 100.0 * (0.6 * delta_norm + 0.4 * (1.0 - div_norm))
    return round(float(los), 3)
