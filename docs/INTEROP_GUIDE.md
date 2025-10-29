# Evo ↔ CSC Interop (Phase 11)

Evo can submit jobs to CSC via two lanes:

- **Lane A (file-drop)** — default, deterministic, no services required.
- **Lane B (HTTP)** — same schema over a REST API with idempotency.

## Config
```toml
[interop]
mode = "file"                   # "file" | "http"
jobs_dir = "jobs"               # Lane A
http_base = "http://localhost:8080"  # Lane B
poll_interval_ms = 500
submit_timeout_s = 10
run_timeout_s = 86400
```

## API

```
handle = submit_job(cfg, Path("runs/g010/g010.zip"), "g010", 12345, {"strict": false})
receipt = await_completion(cfg, handle, timeout_s=3600)
```

## Lane A (file)
- Writes `jobs/incoming/<bundle_id>.job.json` atomically.
- Polls `jobs/done/*.done.json` for matching `request_id`.

## Lane B (http)
- `POST /runs` with `Idempotency-Key: <request_id>` → `{run_id, accepted:true}`
- Poll `GET /runs/{run_id}` until `status: ok|error`.

## Schemas

Shared job/done schemas match CSC docs.

## Determinism
- Request id = `sha256(bundle_id|generation|seed)`.
- Bundle hash verified before submit.
- No timestamps in Evo receipts/logs.
