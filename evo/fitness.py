from __future__ import annotations

import json
from pathlib import Path

from evo.io import report_parser
from evo.metrics import registry


@registry.register("roi")
def metric_roi(start: float, final: float) -> float:
    return (final - start) / start if start else 0.0


@registry.register("drawdown")
def metric_drawdown(bankrolls: list[float]) -> float:
    if not bankrolls:
        return 0.0
    peak, drawdown = bankrolls[0], 0.0
    for bankroll in bankrolls:
        peak = max(peak, bankroll)
        drawdown = min(drawdown, bankroll - peak)
    return drawdown


@registry.register("pso_rate")
def metric_pso_rate(journal_rows: list[dict[str, str]]) -> float:
    if not journal_rows:
        return 0.0
    pso = sum(1 for row in journal_rows if row.get("pso_flag") == "1")
    hands = len({row.get("hand_id") for row in journal_rows})
    return pso / hands if hands else 0.0


def compute_fitness(run_dir: Path, seed_id: str) -> Path:
    """Compute fitness.json from report.json or journal.csv."""
    report = report_parser.read_report_json(run_dir)
    journal = report_parser.read_journal_csv(run_dir)

    bankrolls: list[float] = []
    for row in journal:
        try:
            bankrolls.append(float(row.get("bankroll_after", 0)))
        except (TypeError, ValueError):
            continue

    start_bankroll = float(
        report.get("bankroll_start", bankrolls[0] if bankrolls else 1000),
    )
    final_bankroll = float(
        report.get("bankroll_final", bankrolls[-1] if bankrolls else start_bankroll),
    )

    roi = registry.get("roi")(start_bankroll, final_bankroll)
    drawdown = registry.get("drawdown")(bankrolls) if bankrolls else 0.0
    pso = registry.get("pso_rate")(journal)
    drawdown_penalty = abs(drawdown) / start_bankroll if start_bankroll else 0.0
    fitness_score = 0.5 * roi - 0.3 * drawdown_penalty + 0.2 * (1 - pso)

    data = {
        "schema_version": "1.0",
        "seed_id": seed_id,
        "bankroll_final": round(final_bankroll, 4),
        "roi": round(roi, 4),
        "drawdown_max": round(drawdown, 4),
        "hands_played": len({row.get("hand_id") for row in journal}) if journal else 0,
        "rolls_played": len(journal),
        "pso_rate": round(pso, 4),
        "fitness_score": round(fitness_score, 4),
        "metrics_used": ["roi", "drawdown", "pso_rate"],
    }

    out_path = run_dir / "fitness.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return out_path
