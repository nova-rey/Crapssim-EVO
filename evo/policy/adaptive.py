"""
Adaptive evolution policy.
Decides when to switch between NORMAL and WILDCARD modes based on LoS.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable

from evo.metrics.los import compute_los


@dataclass
class AdaptiveState:
    mode: str = "NORMAL"
    los: float = 0.0
    meh_counter: int = 0
    last_reason: str = "init"
    T_stag: float = 80.0
    meh_band: tuple[float, float] = (55.0, 79.9)
    meh_limit: int = 8

    def update(
        self,
        prev_topk: Iterable[float],
        curr_topk: Iterable[float],
        diversity: float,
    ) -> None:
        prev_list = list(prev_topk)
        curr_list = list(curr_topk)
        self.los = compute_los(prev_list, curr_list, diversity)
        if self.los >= self.T_stag:
            self.mode, self.meh_counter, self.last_reason = "WILDCARD", 0, "stagnation"
        elif self.meh_band[0] <= self.los <= self.meh_band[1]:
            self.meh_counter += 1
            if self.meh_counter >= self.meh_limit:
                self.mode, self.meh_counter, self.last_reason = "WILDCARD", 0, "meh-plateau"
            else:
                self.mode = "NORMAL"
        else:
            self.mode, self.meh_counter, self.last_reason = "NORMAL", 0, "healthy"

    def snapshot(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "los": self.los,
            "meh_counter": self.meh_counter,
            "trigger_reason": self.last_reason,
        }


ADAPTIVE = AdaptiveState()
