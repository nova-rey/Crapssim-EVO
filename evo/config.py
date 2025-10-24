from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

_ENV_PATTERN = re.compile(r"\$\{([^}^{]+)\}")

_DEFAULTS: Dict[str, Any] = {
    "run_id": "anon",
    "seed": None,
    "logging": {"level": "INFO"},
}


def _expand_env(value: Any) -> Any:
    """Recursively expand ${VAR} expressions using os.environ."""
    if isinstance(value, str):

        def replace_var(match: re.Match[str]) -> str:
            var_name = match.group(1)
            return os.environ.get(var_name, match.group(0))

        return _ENV_PATTERN.sub(replace_var, value)
    elif isinstance(value, dict):
        return {k: _expand_env(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_expand_env(v) for v in value]
    return value


def _merge_defaults(user_cfg: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(_DEFAULTS)
    for key, val in user_cfg.items():
        if isinstance(val, dict) and key in merged and isinstance(merged[key], dict):
            temp = dict(merged[key])
            temp.update(val)
            merged[key] = temp
        else:
            merged[key] = val
    return merged


def load_config(path: Optional[str | Path]) -> Dict[str, Any]:
    """
    Load YAML config file (if provided), merge with defaults, expand env vars.
    Always returns a dict.
    """
    cfg: Dict[str, Any] = {}
    if path:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(p)
        with p.open("r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f) or {}
            if not isinstance(loaded, dict):
                raise ValueError(f"Invalid config format in {p}")
            cfg = loaded
    merged = _merge_defaults(cfg)
    expanded = _expand_env(merged)
    # Normalize logging level
    if "logging" in expanded and isinstance(expanded["logging"], dict):
        lvl = expanded["logging"].get("level", "INFO")
        if isinstance(lvl, str):
            expanded["logging"]["level"] = lvl.upper()
    return expanded


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load CrapsSim-Evo configuration")
    parser.add_argument("path", nargs="?", help="Path to YAML configuration file")
    args = parser.parse_args()
    config = load_config(args.path)
    yaml.safe_dump(config, sys.stdout, sort_keys=False)
