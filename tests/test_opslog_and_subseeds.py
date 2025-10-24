"""Tests for ops log structure and RNG subseeds."""

from __future__ import annotations

import json
from pathlib import Path

from evo.evolver import evolve
from evo.rng import seed_global


def _mk_results(tmp: Path) -> None:
    """Create a results root with three seeds."""

    for sid, fit in (
        ("seed_0001", 0.3),
        ("seed_0002", 0.7),
        ("seed_0003", 0.5),
    ):
        (tmp / sid).mkdir(parents=True, exist_ok=True)
        (tmp / sid / "spec.json").write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "profile_id": "opslog_check",
                    "params": {
                        "place_6_8": 24,
                        "place_5_9": 20,
                        "odds_multiple": 3,
                        "regress_pct": 0.35,
                    },
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


def test_ops_log_is_structured_and_monotonic(tmp_path: Path) -> None:
    results_root = tmp_path / "g001_results"
    results_root.mkdir()
    _mk_results(results_root)

    out_dir = tmp_path / "g002"
    seed_global(321)
    evolve(
        results_root,
        out_dir,
        gen_id="g001",
        root_seed=321,
        pop_size=3,
        elite_ratio=1 / 3,
    )

    for dna_path in sorted(out_dir.glob("seed_*/dna.json")):
        meta = json.loads(dna_path.read_text(encoding="utf-8"))
        ops = meta.get("ops_log", [])
        assert isinstance(ops, list), "ops_log must be a list"
        for idx, entry in enumerate(ops):
            assert isinstance(entry, dict), "ops_log entries must be dicts"
            assert entry.get("t") == idx, "ops_log.t must be monotonic 0..n-1"


def test_rng_subseed_unique_within_generation(tmp_path: Path) -> None:
    results_root = tmp_path / "g001_results"
    results_root.mkdir()
    _mk_results(results_root)

    out_dir = tmp_path / "g002"
    seed_global(999)
    evolve(results_root, out_dir, gen_id="g001", root_seed=999, pop_size=3)

    subseeds: set[int] = set()
    for dna_path in sorted(out_dir.glob("seed_*/dna.json")):
        meta = json.loads(dna_path.read_text(encoding="utf-8"))
        subseed = meta.get("rng_subseed")
        assert isinstance(subseed, int), "rng_subseed must be an int"
        subseeds.add(subseed)

    assert len(subseeds) == 3, "rng_subseed values must be unique within a generation"
