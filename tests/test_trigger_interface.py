import json
from pathlib import Path

from evo.interop.trigger import await_completion, submit_job
from evo.interop.util import compute_sha256


def test_trigger_file_mode(tmp_path: Path):
    cfg = {"mode": "file", "jobs_dir": tmp_path / "jobs", "poll_interval_ms": 10}
    runs = tmp_path / "runs" / "g010"
    runs.mkdir(parents=True)
    bundle = runs / "g010.zip"
    bundle.write_bytes(b"dummy")
    bundle_hash = compute_sha256(bundle)
    manifest = {"schema_version": "0.1", "bundle_id": bundle_hash}
    (runs / "interop_manifest.json").write_text(json.dumps(manifest, indent=2))

    handle = submit_job(cfg, bundle, "g010", 1, {})
    done_dir = tmp_path / "jobs" / "done"
    done_dir.mkdir(parents=True, exist_ok=True)
    receipt = {"schema_version": "0.1", "request_id": handle, "status": "ok"}
    (done_dir / "x.done.json").write_text(json.dumps(receipt, indent=2))
    rec = await_completion(cfg, handle, timeout_s=2)
    assert rec["status"] == "ok"
