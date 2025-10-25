"""
Simple diversity metric based on unique spec hashes.
"""

from __future__ import annotations

from typing import Dict, List


def diversity_index(results: List[Dict]) -> float:
    seen = set()
    for r in results:
        seen.add(r.get("spec_hash") or str(r))
    return min(1.0, len(seen) / max(len(results), 1))
