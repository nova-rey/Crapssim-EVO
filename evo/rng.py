from __future__ import annotations

import hashlib
import random
from contextlib import contextmanager
from typing import Any, Dict


def seed_global(seed: int) -> None:
    """Seed Python's global RNG deterministically."""
    random.seed(int(seed))


def make_subseed(name: str, root_seed: int) -> int:
    """Derive a deterministic 32-bit subseed from a name and root seed."""
    data = f"{name}:{root_seed}".encode("utf-8")
    digest = hashlib.sha256(data).digest()
    return int.from_bytes(digest[:4], "big")


def hash_bytes(data: bytes) -> str:
    """Return SHA256 hex digest for arbitrary bytes."""
    return hashlib.sha256(data).hexdigest()


def hash_dict(d: Dict[str, Any]) -> str:
    """Return a stable SHA256 hex digest for a dictionary (sorted keys)."""
    items = sorted(d.items())
    encoded = "".join(f"{k}:{v!r};" for k, v in items).encode("utf-8")
    return hash_bytes(encoded)


@contextmanager
def rng_context(name: str, root_seed: int):
    """Temporarily reseed RNG using a deterministic subseed."""
    prev_state = random.getstate()
    subseed = make_subseed(name, root_seed)
    random.seed(subseed)
    try:
        yield
    finally:
        random.setstate(prev_state)
