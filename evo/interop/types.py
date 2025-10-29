from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class JobPayload:
    schema_version: str
    request_id: str
    bundle_id: str
    bundle_path: str
    generation: str
    seed: int
    run_flags: Dict[str, Any]
    max_rolls: Optional[int]
    webhook_url: Optional[str]

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2, sort_keys=True)


@dataclass
class DoneReceipt:
    schema_version: str
    request_id: str
    bundle_id: str
    generation: str
    run_id: str
    results_root: str
    summary: Dict[str, Any]
    status: str


def stable_request_id(bundle_id: str, generation: str, seed: int) -> str:
    raw = f"{bundle_id}|{generation}|{seed}".encode("utf-8")
    return f"evo-{sha256(raw).hexdigest()}"


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
