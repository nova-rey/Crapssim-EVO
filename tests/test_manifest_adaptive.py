import json
from pathlib import Path

from evo.evolver import evolve
from evo.rng import seed_global


def _mk_flat_results(root: Path, n: int = 4) -> None:
    for i in range(1, n + 1):
        sid = f"seed_{i:04d}"
        (root / sid).mkdir(parents=True, exist_ok=True)
        (root / sid / "spec.json").write_text("{}", encoding="utf-8")
        (root / sid / "dna.json").write_text("{}", encoding="utf-8")
        (root / "run" / sid).mkdir(parents=True, exist_ok=True)
        (root / "run" / sid / "fitness.json").write_text(
            json.dumps({"fitness_score": 1.0}),
            encoding="utf-8",
        )


def test_manifest_has_adaptive_and_grace(tmp_path: Path):
    results_root = tmp_path / "g001_results"
    results_root.mkdir()
    _mk_flat_results(results_root, n=4)

    out_dir = tmp_path / "g002"
    seed_global(123)
    evolve(results_root, out_dir, gen_id="g001", root_seed=123, pop_size=4)

    mf_path = out_dir / "population_manifest.json"
    assert mf_path.exists(), "population_manifest.json must be written"
    mf = json.loads(mf_path.read_text(encoding="utf-8"))
    assert "adaptive" in mf and "grace" in mf, "manifest must include adaptive+grace blocks"
    snap = mf["adaptive"]
    assert {"mode", "los", "meh_counter", "trigger_reason"} <= set(snap.keys())
    assert isinstance(mf["grace"].get("enabled"), bool)
