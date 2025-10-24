from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from .rng import make_subseed

DNA_SCHEMA_VERSION = "0.2"


def load_spec(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def spec_hash_from_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def spec_hash_from_file(path: Path) -> str:
    return spec_hash_from_bytes(path.read_bytes())


def normalize_ops_log(ops_log: Any) -> List[Dict[str, Any]]:
    """
    Accept legacy string ops or structured entries. Return list of dict entries:
    {"type": "mutation"|"crossover", ... , "t": int}
    """
    if isinstance(ops_log, list):
        out: List[Dict[str, Any]] = []
        for item in ops_log:
            if isinstance(item, str):
                out.append({"type": "op", "label": item, "t": 0})
            elif isinstance(item, dict):
                ent = {k: v for k, v in item.items() if isinstance(k, str)}
                ent.setdefault("t", 0)
                out.append(ent)
        return out
    return []


def make_rng_subseed(gen_id: str, index: int, root_seed: int) -> int:
    """Deterministic per-individual subseed based on generation and stable index."""
    return make_subseed(f"{gen_id}:{index:04d}", root_seed)


def build_parent_hashes(parents: Iterable[Tuple[str, Path]]) -> Dict[str, str]:
    """
    parents: iterable of (seed_id, spec_path)
    Returns mapping seed_id -> sha256(spec.json bytes), sorted by seed_id for stability.
    """
    pairs = []
    for seed_id, spec_path in parents:
        pairs.append((seed_id, spec_hash_from_file(spec_path)))
    return {k: v for k, v in sorted(pairs, key=lambda x: x[0])}


def update_dna(
    dna: Dict[str, Any],
    *,
    gen_id: str,
    candidate_id: str,
    parents: List[str],
    parent_hashes: Dict[str, str],
    rng_subseed: int,
    op_entries: List[Dict[str, Any]],
) -> Dict[str, Any]:
    out = dict(dna) if dna else {}
    out["evo_schema_version"] = DNA_SCHEMA_VERSION
    out["parents"] = list(parents)
    out["parent_hashes"] = {k: parent_hashes[k] for k in sorted(parent_hashes.keys())}
    out["rng_subseed"] = int(rng_subseed)
    ident = dict(out.get("identity", {}))
    ident.update({"source": "evolver", "gen_id": gen_id, "candidate_id": candidate_id})
    out["identity"] = ident
    legacy = normalize_ops_log(out.get("ops_log", []))
    seq = list(legacy) + list(op_entries)
    for i, ent in enumerate(seq):
        ent.setdefault("t", i)
    out["ops_log"] = seq
    return out
