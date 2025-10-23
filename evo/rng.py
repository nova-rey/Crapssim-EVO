from __future__ import annotations

import hashlib
import random
from typing import Any, Dict


def seed_global(seed: int) -> None:
    random.seed(seed)


def hash_dict(d: Dict[str, Any]) -> str:
    """
    Stable SHA256 of a dict by encoding keys in sorted order.
    """

    def encode(obj) -> bytes:
        if isinstance(obj, dict):
            items = []
            for k in sorted(obj.keys()):
                items.append(encode(k))
                items.append(encode(obj[k]))
            return b"{" + b"".join(items) + b"}"
        elif isinstance(obj, list):
            return b"[" + b"".join(encode(x) for x in obj) + b"]"
        elif isinstance(obj, (str, bytes)):
            b = obj.encode("utf-8") if isinstance(obj, str) else obj
            return b"s" + b
        elif isinstance(obj, (int, float, bool)) or obj is None:
            return f"p{repr(obj)}".encode("utf-8")
        else:
            return f"t{type(obj).__name__}:{repr(obj)}".encode("utf-8")

    return hashlib.sha256(encode(d)).hexdigest()


def make_subseed(name: str, root_seed: int) -> int:
    blob = f"{name}:{root_seed}".encode("utf-8")
    return int(hashlib.sha256(blob).hexdigest()[:12], 16)
