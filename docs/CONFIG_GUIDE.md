# Config & Logging Guide

This document describes the configuration and logging foundations for CrapsSim-Evo.

---

## 🧩 Config System Overview

Evo uses a lightweight YAML-based configuration system that merges:
1. File-based settings (`.yml` or `.yaml`).
2. Default values embedded in `evo/config.py`.
3. Environment variable overrides using `${VAR}` syntax.

### Load Function
```python
from evo.config import load_config

cfg = load_config("configs/example.yml")
```

If no file is provided, defaults from `evo.config.DEFAULT_CONFIG` are returned:

```
run_id: anon
logging:
  level: INFO
seed: null
```

### Environment Expansion

Variables inside `${VAR}` will be replaced with the corresponding environment value.
If the variable is unset, it remains literal (e.g., `${UNKNOWN}` stays `${UNKNOWN}`).

### Default Merge Rules
- User-provided keys override defaults.
- Unknown keys are preserved but not validated yet.
- Future phases may add schema validation.

⸻

## 🪵 Logging Overview

Logging is handled through `evo/logging.py`.

### Setup
```python
from evo.logging import setup_logging
setup_logging(level="INFO")
```

Logs follow a structured UTC format:

```
2025-10-23T15:22:01Z | INFO | evo.module | message
```

### Guidelines
- Default level is INFO.
- Use DEBUG for verbose diagnostics.
- Logging setup is idempotent (safe to call twice).
- No file handler yet—console output only.

⸻

## ✅ Verified Behavior (Phase 2 Complete)

- `load_config()` merges defaults, expands `${VAR}`, and normalizes log level.
- `setup_logging()` outputs lines like:

  ```
  2025-10-23T15:22:01Z | INFO | evo.module | message
  ```

- Both functions are idempotent and covered by tests.
- Env substitution leaves unknown variables intact.
- Logging timestamps are UTC and end with “Z”.

⸻

## Future Enhancements

| Phase | Planned Feature | Description |
|-------|-----------------|-------------|
| Phase 2 | Env var expansion | Already implemented. |
| Phase 3 | Deterministic seeding | Log RNG seeds for reproducibility. |
| Phase 5 | File handler | Optional log to run_id.log. |
| Phase 7 | JSON log mode | Structured logs for machine parsing. |

---

## 🎲 RNG Configuration

Phase 3 introduces deterministic random control utilities.

### Example Usage

```python
from evo import rng
import random

rng.seed_global(123)
print(rng.make_subseed("operator_A", 123))

with rng.rng_context("mutation", 123):
    value = random.random()
```

Every run is replayable given the same seed in your config file:

```
seed: 123
```

### Stability Notes

- Same seed + same name ⇒ same subseed.
- RNG context restores the prior state after exit.
- No NumPy RNGs yet; those will use `make_subseed()` later.
