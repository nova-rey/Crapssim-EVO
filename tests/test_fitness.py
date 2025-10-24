import json
from pathlib import Path

from evo import fitness


def make_fake_run(tmp_path: Path, bankrolls=(1000, 1100, 950, 1200)):
    run_dir = tmp_path / "run" / "seed_0001"
    run_dir.mkdir(parents=True)
    csv_path = run_dir / "journal.csv"
    rows = ["hand_id,bankroll_after,pso_flag"]
    for i, bankroll in enumerate(bankrolls):
        pso_flag = "1" if i == 2 else "0"
        rows.append(f"{i},{bankroll},{pso_flag}")
    csv_path.write_text("\n".join(rows))
    return run_dir


def test_compute_fitness_from_csv(tmp_path: Path):
    run_dir = make_fake_run(tmp_path)
    out_path = fitness.compute_fitness(run_dir, "seed_0001")
    data = json.loads(out_path.read_text())
    assert data["roi"] > 0
    assert "fitness_score" in data
    assert data["schema_version"] == "1.0"


def test_drawdown_and_pso_metrics(tmp_path: Path):
    run_dir = make_fake_run(tmp_path, (1000, 1100, 900, 950))
    out_path = fitness.compute_fitness(run_dir, "seed_0002")
    data = json.loads(out_path.read_text())
    assert data["drawdown_max"] < 0
    assert 0 <= data["pso_rate"] <= 1
