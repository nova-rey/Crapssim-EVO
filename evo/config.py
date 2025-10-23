from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Optional
import os
import yaml

def load_config(path: Optional[str | Path]) -> Dict[str, Any]:
    """
    Load a YAML config file if provided; otherwise return a minimal default.
    Env-var overrides may be added in later phases.
    """
    if path is None:
        return {"run_id": "dev-local", "logging": {"level": "INFO"}}
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    # Minimal normalization for now
    data.setdefault("run_id", p.stem)
    data.setdefault("logging", {"level": "INFO"})
    return data
