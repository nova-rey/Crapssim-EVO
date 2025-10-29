from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict

from .types import stable_request_id
from .util import compute_sha256, sleep_ms


def _post(base: str, path: str, payload: Dict[str, Any], idem_key: str) -> Dict[str, Any]:
    url = f"{base.rstrip('/')}{path}"
    req = urllib.request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Idempotency-Key", idem_key)
    data = json.dumps(payload, sort_keys=True).encode("utf-8")
    try:
        with urllib.request.urlopen(req, data=data, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        raise RuntimeError(f"HTTP {e.code}: {body}")


def _get(base: str, path: str) -> Dict[str, Any]:
    url = f"{base.rstrip('/')}{path}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def submit_http_job(
    cfg: Dict[str, Any],
    bundle_path: Path,
    generation: str,
    seed: int,
    run_flags: Dict[str, Any],
) -> str:
    bundle_path = bundle_path.resolve()
    base = cfg.get("http_base", "http://localhost:8080")
    bundle_id = compute_sha256(bundle_path)
    request_id = stable_request_id(bundle_id, generation, seed)

    payload = {
        "schema_version": "0.1",
        "bundle_url": f"file://{bundle_path}",
        "bundle_id": bundle_id,
        "generation": generation,
        "seed": int(seed),
        "run_flags": dict(run_flags or {}),
        "max_rolls": None,
    }
    resp = _post(base, "/runs", payload, idem_key=request_id)
    if not resp.get("accepted"):
        raise RuntimeError("Job not accepted")
    return resp["run_id"]


def wait_http_done(cfg: Dict[str, Any], run_id: str, timeout_s: int) -> Dict[str, Any]:
    base = cfg.get("http_base", "http://localhost:8080")
    poll_ms = int(cfg.get("poll_interval_ms", 500))
    steps = int(max(timeout_s, 0) * 1000 / max(poll_ms, 1)) if timeout_s else 10_000_000

    for _ in range(steps):
        rec = _get(base, f"/runs/{run_id}")
        if rec.get("status") in {"ok", "error"}:
            return rec
        sleep_ms(poll_ms)

    return {
        "schema_version": "0.1",
        "run_id": run_id,
        "status": "error",
        "error_code": "TIMEOUT",
        "error_detail": "No completion before timeout",
    }
