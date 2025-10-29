import json
import threading
import time
from pathlib import Path

from evo.interop.lane_file import submit_file_job, wait_file_done
from evo.interop.util import compute_sha256


def _mk_bundle(tmp: Path) -> Path:
    g = tmp / "runs" / "g010"
    g.mkdir(parents=True)
    z = g / "g010.zip"
    z.write_bytes(b"dummy")
    bid = compute_sha256(z)
    (g / "interop_manifest.json").write_text(
        json.dumps({"schema_version": "0.1", "bundle_id": bid}, indent=2)
    )
    return z


def test_file_lane_roundtrip(tmp_path: Path):
    cfg = {"jobs_dir": tmp_path / "jobs", "poll_interval_ms": 50}
    bundle = _mk_bundle(tmp_path)

    req_id = submit_file_job(cfg, bundle, "g010", 123, {"strict": False})
    incoming = tmp_path / "jobs" / "incoming"
    assert list(incoming.glob("*.partial")) == [], "no partials should remain"

    def _writer():
        done = {
            "schema_version": "0.1",
            "request_id": req_id,
            "bundle_id": compute_sha256(bundle),
            "generation": "g010",
            "run_id": "csc-001",
            "results_root": "runs/g010_results",
            "summary": {"top_fitness": 1.0, "pop_size": 1},
            "status": "ok",
        }
        time.sleep(0.1)
        (tmp_path / "jobs" / "done").mkdir(parents=True, exist_ok=True)
        (tmp_path / "jobs" / "done" / "csc-001.done.json").write_text(json.dumps(done, indent=2))

    t = threading.Thread(target=_writer, daemon=True)
    t.start()
    rec = wait_file_done(cfg, req_id, timeout_s=5)
    assert rec["status"] == "ok"
    assert rec["request_id"] == req_id
