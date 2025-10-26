from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


def list_generation_dirs(root: Path) -> List[Path]:
    """Return generation folders under root ordered by gen label (g001 < g002 < ...)."""
    gens = [
        p for p in root.iterdir() if p.is_dir() and p.name.startswith("g") and p.name[1:].isdigit()
    ]

    def _key(p: Path) -> Tuple[int, str]:
        label = p.name
        if label[0] == "g" and label[1:].isdigit():
            return (int(label[1:]), label)
        return (10**9, label)

    return sorted(gens, key=_key)


def read_population_manifest(gen_dir: Path) -> Dict:
    path = gen_dir / "population_manifest.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def iter_seed_dirs(gen_dir: Path) -> Iterable[Path]:
    for p in sorted(gen_dir.glob("seed_*")):
        if p.is_dir():
            yield p


def read_dna(seed_dir: Path) -> Dict:
    path = seed_dir / "dna.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def read_fitness(prev_results_root: Path, seed_id: str) -> Optional[Dict]:
    """
    Previous generation's results live under prev_results_root/run/<seed_id>/fitness.json.
    Return dict or None.
    """
    path = prev_results_root / "run" / seed_id / "fitness.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def link_prev_results(gen_dir: Path) -> Optional[Path]:
    """
    Heuristic: previous results for gen gNNN are in sibling 'g{NNN-1}_results' if it exists,
    else None. Analysis should skip missing gracefully.
    """
    name = gen_dir.name
    if not (name.startswith("g") and name[1:].isdigit()):
        return None
    prev = f"g{int(name[1:]) - 1:03d}_results"
    candidate = gen_dir.parent / prev
    return candidate if candidate.exists() else None
