from __future__ import annotations

import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from ..population import Individual


def write_generation_folder(
    out_dir: Path, gen_id: str, individuals: Iterable[Individual], elite_ids: set[str] | None = None
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    elite_ids = elite_ids or set()
    pop_manifest = {
        "evo_schema_version": "0.1",
        "gen_id": gen_id,
        "mode": "NORMAL",
        "pop_size": 0,
        "candidates": [],
    }
    for idx, ind in enumerate(individuals, start=1):
        seed_dir = out_dir / f"seed_{idx:04d}"
        seed_dir.mkdir(parents=True, exist_ok=True)
        if ind.seed_id in elite_ids:
            (seed_dir / "spec.json").write_text(json.dumps(ind.spec, indent=2), encoding="utf-8")
            dna = dict(ind.dna)
            dna.setdefault("identity", {})
            dna["identity"].update(
                {"source": "evolver", "gen_id": gen_id, "candidate_id": seed_dir.name}
            )
            (seed_dir / "dna.json").write_text(json.dumps(dna, indent=2), encoding="utf-8")
        else:
            spec = dict(ind.spec)
            identity = spec.get("identity", {})
            identity.update({"source": "evolver", "gen_id": gen_id, "candidate_id": seed_dir.name})
            spec["identity"] = identity
            (seed_dir / "spec.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")
            (seed_dir / "dna.json").write_text(json.dumps(ind.dna, indent=2), encoding="utf-8")
        pop_manifest["candidates"].append({"id": seed_dir.name})
        pop_manifest["pop_size"] += 1
    (out_dir / "population_manifest.json").write_text(
        json.dumps(pop_manifest, indent=2), encoding="utf-8"
    )
    return out_dir


def zip_generation_folder(src_dir: Path, out_zip: Path) -> Path:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(src_dir.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(src_dir).as_posix())
        info = {
            "bundle_schema_version": "1.0",
            "producer": "EVO",
            "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "format": "zip",
            "contents": {"seeds_glob": "seed_*/spec.json"},
        }
        zf.writestr("meta/bundle.json", json.dumps(info, indent=2))
    return out_zip
