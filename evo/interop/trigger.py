from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .lane_file import submit_file_job, wait_file_done
from .lane_http import submit_http_job, wait_http_done


def submit_job(
    cfg: Dict[str, Any],
    bundle_path: Path,
    generation: str,
    seed: int,
    run_flags: Dict[str, Any],
):
    mode = (cfg.get("mode") or "file").lower()
    if mode == "file":
        return submit_file_job(cfg, Path(bundle_path), generation, seed, run_flags)
    if mode == "http":
        return submit_http_job(cfg, Path(bundle_path), generation, seed, run_flags)
    raise ValueError(f"Unknown interop mode: {mode}")


def await_completion(cfg: Dict[str, Any], handle: str, timeout_s: int) -> Dict[str, Any]:
    mode = (cfg.get("mode") or "file").lower()
    if mode == "file":
        return wait_file_done(cfg, handle, timeout_s)
    if mode == "http":
        return wait_http_done(cfg, handle, timeout_s)
    raise ValueError(f"Unknown interop mode: {mode}")
