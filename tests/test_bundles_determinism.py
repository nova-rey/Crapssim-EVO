import json
from pathlib import Path

from evo.io.bundles import (
    compute_zip_hash,
    write_bundle_zip,
    write_interop_manifest,
)


def test_deterministic_zip(tmp_path: Path):
    g = tmp_path / "g010"
    g.mkdir()
    (g / "a.txt").write_text("alpha")
    (g / "b.txt").write_text("beta")

    z1 = tmp_path / "b1.zip"
    z2 = tmp_path / "b2.zip"
    write_bundle_zip(g, z1, deterministic=True)
    write_bundle_zip(g, z2, deterministic=True)

    assert compute_zip_hash(z1) == compute_zip_hash(z2)

    manifest = write_interop_manifest(z1, "g010", deterministic=True)
    data = json.loads(manifest.read_text())
    assert data["schema_version"] == "0.1"
    assert data["deterministic"] is True
    assert data["generation"] == "g010"
    assert len(data["bundle_id"]) == 64
