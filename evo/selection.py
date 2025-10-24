from __future__ import annotations

import random
from typing import List

from .population import Individual


def tournament(pop: List[Individual], k: int = 3) -> Individual:
    """Pick the best of k random individuals."""
    contestants = random.sample(pop, k=min(k, len(pop)))
    return max(contestants, key=lambda ind: ind.fitness)


def elitism(pop: List[Individual], elite_k: int) -> List[Individual]:
    return sorted(pop, key=lambda ind: ind.fitness, reverse=True)[:elite_k]
