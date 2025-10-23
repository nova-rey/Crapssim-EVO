import os
from pathlib import Path

import yaml

from evo.config import load_config


def test_defaults_returned_when_no_file():
    cfg = load_config(None)
    assert isinstance(cfg, dict)
    assert cfg["run_id"] == "anon"
    assert cfg["logging"]["level"] == "INFO"
    assert "seed" in cfg

def test_yaml_file_load_and_merge(tmp_path: Path):
    cfg_path = tmp_path / "conf.yml"
    yaml.safe_dump({"run_id": "custom"}, cfg_path.open("w", encoding="utf-8"))
    cfg = load_config(cfg_path)
    assert cfg["run_id"] == "custom"
    assert cfg["logging"]["level"] == "INFO"  # from defaults

def test_env_variable_expansion(tmp_path: Path):
    os.environ["RANDOM_SEED"] = "42"
    cfg_path = tmp_path / "conf.yml"
    yaml.safe_dump({"seed": "${RANDOM_SEED}"}, cfg_path.open("w", encoding="utf-8"))
    cfg = load_config(cfg_path)
    assert cfg["seed"] == "42"

def test_missing_env_var_literal_remains(tmp_path: Path):
    cfg_path = tmp_path / "conf.yml"
    yaml.safe_dump({"seed": "${UNSET_VAR}"}, cfg_path.open("w", encoding="utf-8"))
    cfg = load_config(cfg_path)
    assert cfg["seed"] == "${UNSET_VAR}"

def test_logging_level_normalized(tmp_path: Path):
    cfg_path = tmp_path / "conf.yml"
    yaml.safe_dump({"logging": {"level": "debug"}}, cfg_path.open("w", encoding="utf-8"))
    cfg = load_config(cfg_path)
    assert cfg["logging"]["level"] == "DEBUG"
