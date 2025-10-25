"""
Level-of-Stagnation (LoS) metric.
LoS gauges population stagnation from fitness change and diversity.
"""

from __future__ import annotations

from typing import List

import numpy as np


def compute_los(
    prev_topk: List[float],
    curr_topk: List[float],
    diversity: float,
) -> float:
    """
    Returns a 0–100 stagnation score.
    Low = healthy evolution; high = stagnation.
    """
    if not prev_topk or not curr_topk:
        return 0.0
    prev_mean = float(np.mean(prev_topk))
    curr_mean = float(np.mean(curr_topk))
    delta = max(0.0, prev_mean - curr_mean)
    # normalize ∆EF and diversity into [0,1]
    scale = abs(curr_mean) if abs(curr_mean) > 1e-9 else 1.0
    delta_norm = min(delta / scale * 16.0, 1.0)
    div_clamped = max(0.0, min(diversity, 1.0))
    div_norm = 1.0 - div_clamped
    los = 100.0 * (0.6 * delta_norm + 0.4 * div_norm)
    return round(float(los), 3)
