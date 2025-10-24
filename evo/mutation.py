from __future__ import annotations

import copy
import random
from typing import Any, Dict

from .population import Individual

_NUMERIC_FIELDS = ("place_6_8", "place_5_9", "odds_multiple", "regress_pct")


def mutate_spec(spec: Dict[str, Any], nudge_frac: float = 0.1) -> Dict[str, Any]:
    """Return a mutated copy of spec.params/toggles (small safe nudges)."""
    s = copy.deepcopy(spec)
    params = s.get("params", {})
    for key in _NUMERIC_FIELDS:
        if key in params and isinstance(params[key], (int, float)):
            base = float(params[key])
            delta = base * nudge_frac * (random.random() * 2 - 1)
            new_val = base + delta
            if key in ("place_6_8",):
                new_val = round(new_val / 6) * 6
            if key in ("place_5_9",):
                new_val = round(new_val / 5) * 5
            if key == "odds_multiple":
                new_val = max(1, round(new_val))
            if key == "regress_pct":
                new_val = min(1.0, max(0.0, new_val))
            params[key] = type(params[key])(new_val)
    s["params"] = params
    return s


def crossover_specs(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """Block-wise crossover: pick params from parent A or B, toggles likewise."""
    child = {"schema_version": a.get("schema_version", "1.0")}
    child["profile_id"] = random.choice([a.get("profile_id"), b.get("profile_id")])
    child_params: Dict[str, Any] = {}
    for k in set(a.get("params", {})) | set(b.get("params", {})):
        pool = []
        if k in a.get("params", {}):
            pool.append(a["params"][k])
        if k in b.get("params", {}):
            pool.append(b["params"][k])
        child_params[k] = random.choice(pool) if pool else None
    child["params"] = child_params
    child_toggles: Dict[str, Any] = {}
    for k in set(a.get("toggles", {})) | set(b.get("toggles", {})):
        pool = []
        if k in a.get("toggles", {}):
            pool.append(a["toggles"][k])
        if k in b.get("toggles", {}):
            pool.append(b["toggles"][k])
        child_toggles[k] = random.choice(pool) if pool else False
    child["toggles"] = child_toggles
    return child


def record_op(dna: Dict[str, Any], op: str) -> None:
    # keep legacy strings for backward compat; evolver will add structured entries later
    dna.setdefault("ops_log", []).append(op)


def mutate_individual(ind: Individual, nudge_frac: float = 0.1) -> Individual:
    child = ind.clone()
    child.spec = mutate_spec(child.spec, nudge_frac=nudge_frac)
    child.parents = [ind.seed_id]
    record_op(child.dna, f"mutate(nudge={nudge_frac})")
    return child


def crossover_individuals(a: Individual, b: Individual) -> Individual:
    child = a.clone()
    child.spec = crossover_specs(a.spec, b.spec)
    child.parents = [a.seed_id, b.seed_id]
    record_op(child.dna, "crossover(blocks)")
    return child
