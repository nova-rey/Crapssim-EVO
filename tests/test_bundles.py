import json
import zipfile
from pathlib import Path

import pytest

from evo.io import bundles


def make_fake_bundle(tmp_path: Path):
    root = tmp_path / "seed_0001"
    root.mkdir(parents=True)
    spec = root / "spec.json"
    spec.write_text("{}")
    extra = tmp_path / "notes.txt"
    extra.write_text("keep me")
    out_zip = tmp_path / "bundle.zip"
    with zipfile.ZipFile(out_zip, "w") as zf:
        zf.write(spec, "seed_0001/spec.json")
        zf.write(extra, "notes.txt")
    return out_zip


def test_round_trip_preserves_files(tmp_path: Path):
    z = make_fake_bundle(tmp_path)
    staging = bundles.open_bundle(z)
    bundles.validate_input_bundle(staging)
    out_zip = tmp_path / "out.zip"
    bundles.write_bundle(staging, out_zip)
    with zipfile.ZipFile(z, "r") as orig, zipfile.ZipFile(out_zip, "r") as rep:
        assert set(orig.namelist()) == set(rep.namelist())


def test_zip_slip_rejected(tmp_path: Path):
    bad_zip = tmp_path / "evil.zip"
    with zipfile.ZipFile(bad_zip, "w") as zf:
        zf.writestr("../evil.txt", "oops")
    with pytest.raises(bundles.BundleError):
        bundles.open_bundle(bad_zip)


def test_validate_missing_seed_raises(tmp_path: Path):
    empty_zip = tmp_path / "empty.zip"
    with zipfile.ZipFile(empty_zip, "w") as zf:
        zf.writestr("nothing.txt", "hi")
    staging = bundles.open_bundle(empty_zip)
    with pytest.raises(bundles.BundleError):
        bundles.validate_input_bundle(staging)


def test_checksums_and_contents(tmp_path: Path):
    z = make_fake_bundle(tmp_path)
    staging = bundles.open_bundle(z)
    run_dir = bundles.prepare_results_layout(staging)
    dummy = run_dir / "dummy.txt"
    dummy.write_text("abc")
    bundles.write_checksums(staging, ["run/dummy.txt"])
    chk = (run_dir / "checksums.txt").read_text()
    assert "dummy.txt" in chk
    bundles.write_contents_index(staging)
    data = json.loads((run_dir / "CONTENTS.json").read_text())
    assert any("seed_0001/spec.json" in x["path"] for x in data)


def test_write_bundle_manifest(tmp_path: Path):
    z = make_fake_bundle(tmp_path)
    staging = bundles.open_bundle(z)
    bundles.write_bundle_manifest(staging)
    meta_file = staging / "meta" / "bundle.json"
    assert meta_file.exists()
    info = json.loads(meta_file.read_text())
    assert info["bundle_schema_version"] == "1.0"
