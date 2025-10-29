from __future__ import annotations

import argparse
from pathlib import Path

from evo.interop.trigger import await_completion, submit_job


def main() -> None:
    p = argparse.ArgumentParser(description="Submit Evo job to CSC")
    p.add_argument("bundle", type=Path)
    p.add_argument("--generation", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--mode", choices=["file", "http"], default="file")
    p.add_argument("--jobs-dir", default="jobs")
    p.add_argument("--http-base", default="http://localhost:8080")
    p.add_argument("--timeout-s", type=int, default=3600)
    args = p.parse_args()

    cfg = {
        "mode": args.mode,
        "jobs_dir": args.jobs_dir,
        "http_base": args.http_base,
        "poll_interval_ms": 500,
    }
    handle = submit_job(cfg, args.bundle, args.generation, args.seed, {})
    rec = await_completion(cfg, handle, args.timeout_s)
    print(rec)


if __name__ == "__main__":
    main()
