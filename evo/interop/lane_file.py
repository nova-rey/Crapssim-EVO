from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .types import JobPayload, read_json, stable_request_id
from .util import atomic_write_json, compute_sha256, sleep_ms


def _load_interop_manifest(bundle_path: Path) -> Dict[str, Any]:
    # interop_manifest.json sits beside the bundle
    manifest = bundle_path.parent / "interop_manifest.json"
    return read_json(manifest)


def submit_file_job(
    cfg: Dict[str, Any],
    bundle_path: Path,
    generation: str,
    seed: int,
    run_flags: Dict[str, Any],
) -> str:
    bundle_path = bundle_path.resolve()
    interop = _load_interop_manifest(bundle_path)
    bundle_id = interop["bundle_id"]
    # sanity: recompute hash
    assert compute_sha256(bundle_path) == bundle_id, "bundle_id hash mismatch"

    request_id = stable_request_id(bundle_id, generation, seed)
    jobs_dir = Path(cfg.get("jobs_dir", "jobs"))
    incoming = jobs_dir / "incoming"
    incoming.mkdir(parents=True, exist_ok=True)

    job = JobPayload(
        schema_version="0.1",
        request_id=request_id,
        bundle_id=bundle_id,
        bundle_path=str(bundle_path),
        generation=generation,
        seed=int(seed),
        run_flags=dict(run_flags or {}),
        max_rolls=None,
        webhook_url=None,
    )
    job_path = incoming / f"{bundle_id}.job.json"
    atomic_write_json(job_path, job.__dict__)
    return request_id


def wait_file_done(cfg: Dict[str, Any], request_id: str, timeout_s: int) -> Dict[str, Any]:
    jobs_dir = Path(cfg.get("jobs_dir", "jobs"))
    done_dir = jobs_dir / "done"
    done_dir.mkdir(parents=True, exist_ok=True)

    poll_ms = int(cfg.get("poll_interval_ms", 500))
    deadline = done_dir.stat().st_mtime + max(timeout_s, 0)

    while True:
        for p in sorted(done_dir.glob("*.done.json")):
            rec = read_json(p)
            if rec.get("request_id") == request_id:
                return rec
        if timeout_s and (Path(".").stat().st_mtime > deadline):
            return {
                "schema_version": "0.1",
                "request_id": request_id,
                "status": "error",
                "error_code": "TIMEOUT",
                "error_detail": "No done receipt before timeout",
            }
        sleep_ms(poll_ms)
