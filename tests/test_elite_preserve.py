"""Tests for elite spec preservation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from evo.evolver import evolve
from evo.rng import seed_global


def _sha256(path: Path) -> str:
    hash_obj = hashlib.sha256()
    hash_obj.update(path.read_bytes())
    return hash_obj.hexdigest()


def _mk_results(tmp: Path) -> None:
    """Create a minimal results directory with two seeds."""

    for sid, fit, spec in (
        (
            "seed_0001",
            0.2,
            {
                "params": {
                    "place_6_8": 24,
                    "place_5_9": 20,
                    "odds_multiple": 3,
                    "regress_pct": 0.35,
                }
            },
        ),
        (
            "seed_0002",
            0.9,
            {
                "params": {
                    "place_6_8": 30,
                    "place_5_9": 25,
                    "odds_multiple": 3,
                    "regress_pct": 0.25,
                }
            },
        ),
    ):
        (tmp / sid).mkdir(parents=True, exist_ok=True)
        (tmp / sid / "spec.json").write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "profile_id": "elite_check",
                    "params": spec["params"],
                    "toggles": {"bubble_mode": False},
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        (tmp / sid / "dna.json").write_text(
            json.dumps({"evo_schema_version": "0.1"}, indent=2),
            encoding="utf-8",
        )
        (tmp / "run" / sid).mkdir(parents=True, exist_ok=True)
        (tmp / "run" / sid / "fitness.json").write_text(
            json.dumps({"fitness_score": fit}, indent=2),
            encoding="utf-8",
        )


def test_elite_spec_is_byte_preserved(tmp_path: Path) -> None:
    results_root = tmp_path / "g001_results"
    results_root.mkdir()
    _mk_results(results_root)

    elite_in = results_root / "seed_0002" / "spec.json"
    elite_in_hash = _sha256(elite_in)

    out_dir = tmp_path / "g002"
    seed_global(123)
    evolve(
        results_root,
        out_dir,
        gen_id="g001",
        root_seed=123,
        pop_size=2,
        elite_ratio=0.5,
    )

    elite_out = out_dir / "seed_0001" / "spec.json"
    assert elite_out.exists(), "Expected elite spec.json in seed_0001/"
    elite_out_hash = _sha256(elite_out)

    assert elite_in_hash == elite_out_hash, "Elite spec.json must be byte-for-byte identical"
