import json
from pathlib import Path

from evo.evolver import evolve
from evo.io.export import zip_generation_folder
from evo.rng import seed_global


def make_phase5_like_run(tmp_path: Path, seed_id: str, fitness: float) -> Path:
    seed_dir = tmp_path / seed_id
    seed_dir.mkdir(parents=True)
    (seed_dir / "spec.json").write_text(
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
        )
    )
    (seed_dir / "dna.json").write_text(json.dumps({"evo_schema_version": "0.1"}, indent=2))
    run_seed_dir = tmp_path / "run" / seed_id
    run_seed_dir.mkdir(parents=True)
    (run_seed_dir / "fitness.json").write_text(json.dumps({"fitness_score": fitness}, indent=2))
    return tmp_path


def test_evolve_produces_next_generation(tmp_path: Path) -> None:
    results_root = tmp_path / "g001_results"
    results_root.mkdir()
    make_phase5_like_run(results_root, "seed_0001", 0.2)
    make_phase5_like_run(results_root, "seed_0002", 0.8)

    out_dir = tmp_path / "g002"
    seed_global(123)
    next_pop = evolve(results_root, out_dir, gen_id="g001", root_seed=123, pop_size=2)
    assert len(next_pop) == 2
    assert (out_dir / "population_manifest.json").exists()
    specs = list(out_dir.glob("seed_*/spec.json"))
    assert len(specs) == 2


def test_export_zip(tmp_path: Path) -> None:
    out_dir = tmp_path / "g002"
    (out_dir / "seed_0001").mkdir(parents=True)
    (out_dir / "seed_0001" / "spec.json").write_text("{}")
    (out_dir / "seed_0001" / "dna.json").write_text("{}")
    (out_dir / "population_manifest.json").write_text("{}")
    out_zip = tmp_path / "g002_input.zip"
    zip_generation_folder(out_dir, out_zip)
    assert out_zip.exists()
