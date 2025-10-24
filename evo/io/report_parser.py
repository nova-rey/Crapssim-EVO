from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict


def read_report_json(run_dir: Path) -> Dict[str, Any]:
    """Read report.json if available; return dict or empty."""
    report_path = run_dir / "report.json"
    if report_path.exists():
        with open(report_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def read_journal_csv(run_dir: Path) -> list[Dict[str, Any]]:
    """Read journal.csv as list of dict rows; returns [] if missing."""
    journal_path = run_dir / "journal.csv"
    rows: list[Dict[str, Any]] = []
    if journal_path.exists():
        with open(journal_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader]
    return rows
