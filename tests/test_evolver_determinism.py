import hashlib
import json
from pathlib import Path

from evo.evolver import evolve
from evo.rng import seed_global


def _hash_tree(folder: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(folder.rglob("*.json")):
        h.update(p.relative_to(folder).as_posix().encode("utf-8"))
        h.update(p.read_bytes())
    return h.hexdigest()


def _mk_results(tmp: Path) -> None:
    # Build a minimal Phase 5-like results_root with two seeds and fitness
    for sid, fit in (("seed_0001", 0.2), ("seed_0002", 0.8)):
        (tmp / sid).mkdir(parents=True, exist_ok=True)
        (tmp / sid / "spec.json").write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "profile_id": "contra_cruise",
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


def test_evolution_is_reproducible(tmp_path: Path) -> None:
    results_root = tmp_path / "g001_results"
    results_root.mkdir()
    _mk_results(results_root)

    out1 = tmp_path / "g002_a"
    out2 = tmp_path / "g002_b"

    seed_global(123)
    evolve(results_root, out1, gen_id="g001", root_seed=123, pop_size=2)

    seed_global(123)
    evolve(results_root, out2, gen_id="g001", root_seed=123, pop_size=2)

    assert _hash_tree(out1) == _hash_tree(out2)
