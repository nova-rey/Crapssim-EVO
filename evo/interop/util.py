from __future__ import annotations

import json
import os
import time
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict


def atomic_write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".partial")
    data = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def compute_sha256(file_path: Path) -> str:
    h = sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sleep_ms(ms: int) -> None:
    time.sleep(max(ms, 0) / 1000.0)
