import json
from pathlib import Path

from evo.dna import build_parent_hashes, make_rng_subseed, normalize_ops_log, spec_hash_from_file


def test_parent_hashes_stable(tmp_path: Path) -> None:
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps({"a": 1, "b": 2}, indent=2), encoding="utf-8")
    h1 = spec_hash_from_file(spec)
    h2 = spec_hash_from_file(spec)
    assert h1 == h2 and len(h1) == 64


def test_build_parent_hashes_deterministic(tmp_path: Path) -> None:
    s1 = tmp_path / "seed_0001_spec.json"
    s1.write_text("{}", encoding="utf-8")
    s2 = tmp_path / "seed_0002_spec.json"
    s2.write_text('{"x":1}', encoding="utf-8")
    mapping = build_parent_hashes([("seed_0002", s2), ("seed_0001", s1)])
    assert list(mapping.keys()) == ["seed_0001", "seed_0002"]


def test_rng_subseed_deterministic() -> None:
    ss1 = make_rng_subseed("g002", 7, 123)
    ss2 = make_rng_subseed("g002", 7, 123)
    ss3 = make_rng_subseed("g002", 8, 123)
    assert ss1 == ss2 and ss1 != ss3


def test_normalize_ops_log_accepts_legacy_and_structured() -> None:
    legacy = ["mutate(nudge=0.1)", "crossover(blocks)"]
    norm = normalize_ops_log(legacy)
    assert isinstance(norm, list) and all(isinstance(x, dict) for x in norm)
    structured = [{"type": "mutation", "nudge_frac": 0.1}]
    norm2 = normalize_ops_log(structured)
    assert norm2[0]["type"] == "mutation"
