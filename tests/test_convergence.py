import json
from pathlib import Path

from evo.analysis.convergence import GenRollup, compute_trends
from evo.analysis.reader import list_generation_dirs
from evo.analysis.reporters import operator_stats_for_gen
from evo.analysis.run_convergence import run_for_root


def _mk_gen(
    root: Path,
    label: str,
    fitness_vals,
    roi_vals,
    dd_vals,
    mode="NORMAL",
    los=25.0,
):
    gen_dir = root / label
    gen_dir.mkdir(parents=True)
    for i, _ in enumerate(fitness_vals, start=1):
        seed_dir = gen_dir / f"seed_{i:04d}"
        seed_dir.mkdir()
        (seed_dir / "dna.json").write_text(
            json.dumps({"ops_log": [{"type": "mutation"}]}), encoding="utf-8"
        )
    manifest = {"pop_schema_version": "0.2", "mode": mode, "adaptive": {"los": float(los)}}
    (gen_dir / "population_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    idx = int(label[1:])
    prev = root / f"g{idx-1:03d}_results"
    prev.mkdir()
    for i, (fitness_score, roi, drawdown) in enumerate(
        zip(fitness_vals, roi_vals, dd_vals), start=1
    ):
        run_dir = prev / "run" / f"seed_{i:04d}"
        run_dir.mkdir(parents=True)
        (run_dir / "fitness.json").write_text(
            json.dumps(
                {
                    "fitness_score": fitness_score,
                    "roi": roi,
                    "drawdown_max": drawdown,
                }
            ),
            encoding="utf-8",
        )


def test_rollup_and_csv_json(tmp_path: Path):
    _mk_gen(tmp_path, "g001", [1.0, 0.8], [0.1, 0.05], [-50, -80], mode="NORMAL", los=20.0)
    _mk_gen(tmp_path, "g002", [1.1, 0.9], [0.12, 0.06], [-40, -70], mode="WILDCARD", los=85.0)

    run_for_root(tmp_path, window=5)

    current = tmp_path / "g002"
    convergence_json = json.loads((current / "convergence.json").read_text(encoding="utf-8"))
    assert convergence_json["schema_version"] == "1.0"
    assert convergence_json["gens"][-1]["gen_id"] == "g002"
    assert "trends" in convergence_json and "ef_slope" in convergence_json["trends"]

    csv_path = current / "convergence.csv"
    assert csv_path.exists()
    rows = csv_path.read_text(encoding="utf-8").strip().splitlines()
    assert rows[0].startswith("gen_id") and rows[-1].startswith("g002")


def test_trend_math_consistent():
    gens = [
        GenRollup("g001", 1.0, 1.0, 1.0, None, None, None, None, "NORMAL"),
        GenRollup("g002", 1.2, 1.1, 1.05, None, None, None, None, "NORMAL"),
        GenRollup("g003", 1.3, 1.2, 1.1, None, None, None, None, "NORMAL"),
    ]
    trends = compute_trends(gens, window=3)
    assert trends["ef_slope"] is not None and trends["ef_slope"] > 0
    assert trends["best_plateau_len"] == 0


def test_operator_stats_sane():
    stats = operator_stats_for_gen([{"ops_log": [{"type": "mutation"}, {"type": "crossover"}]}])
    assert set(stats.keys()) == {"counts", "rates"}
    assert "mutation" in stats["counts"] and "crossover" in stats["rates"]


def test_list_generation_dirs(tmp_path: Path):
    (tmp_path / "g002").mkdir()
    (tmp_path / "g001").mkdir()
    (tmp_path / "g000_results").mkdir()
    (tmp_path / "notes").mkdir()
    gens = list_generation_dirs(tmp_path)
    assert [g.name for g in gens] == ["g001", "g002"]
