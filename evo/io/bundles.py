from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Optional


class BundleError(Exception):
    """Raised for bundle validation or integrity errors."""


def _safe_extract(zip_path: Path, dest_dir: Path) -> None:
    """Safely extract a zip archive into dest_dir without allowing path traversal."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            target_path = dest_dir / member.filename
            if not str(target_path.resolve()).startswith(str(dest_dir.resolve())):
                raise BundleError(f"Zip-slip attempt: {member.filename}")
            if member.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
            else:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, open(target_path, "wb") as dst:
                    shutil.copyfileobj(src, dst)


def open_bundle(path: Path, staging_root: Optional[Path] = None) -> Path:
    """Unpack bundle safely into a staging directory; return path."""
    if not path.exists():
        raise FileNotFoundError(path)
    staging_dir = Path(tempfile.mkdtemp(prefix="bundle_", dir=staging_root))
    _safe_extract(path, staging_dir)
    return staging_dir


def validate_input_bundle(staging_dir: Path) -> None:
    """Ensure at least one seed_*/spec.json exists and no duplicates."""
    seeds = list(staging_dir.glob("seed_*/spec.json"))
    if not seeds:
        raise BundleError("No seed_*/spec.json found.")
    ids = [p.parent.name for p in seeds]
    if len(ids) != len(set(ids)):
        raise BundleError("Duplicate seed IDs detected.")


def iter_seed_specs(staging_dir: Path) -> Iterable[tuple[str, Path]]:
    """Yield (seed_id, spec_path) for discovered seeds."""
    for spec in sorted(staging_dir.glob("seed_*/spec.json")):
        yield spec.parent.name, spec


def prepare_results_layout(staging_dir: Path) -> Path:
    """Ensure /run exists and return it."""
    run_dir = staging_dir / "run"
    run_dir.mkdir(exist_ok=True)
    return run_dir


def write_run_artifacts(staging_dir: Path, seed_id: str, artifacts: Dict[str, Path]) -> None:
    """Copy artifacts into run/<seed_id>/."""
    run_seed_dir = staging_dir / "run" / seed_id
    run_seed_dir.mkdir(parents=True, exist_ok=True)
    for key, src in artifacts.items():
        dst = run_seed_dir / Path(src).name
        shutil.copy2(src, dst)


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def write_checksums(staging_dir: Path, rel_paths: list[str]) -> None:
    """Compute SHA256 checksums for provided paths relative to staging_dir."""
    lines = []
    for rel in rel_paths:
        p = staging_dir / rel
        if p.exists() and p.is_file():
            lines.append(f"{_hash_file(p)}  {rel}")
    out = staging_dir / "run" / "checksums.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_contents_index(staging_dir: Path) -> None:
    """Enumerate all files and write run/CONTENTS.json."""
    index = []
    for p in sorted(staging_dir.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(staging_dir)).replace(os.sep, "/")
            index.append(
                {
                    "path": rel,
                    "bytes": p.stat().st_size,
                    "sha256": _hash_file(p),
                }
            )
    out = staging_dir / "run" / "CONTENTS.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(index, out.open("w", encoding="utf-8"), indent=2)


def write_bundle(staging_dir: Path, out_zip: Path) -> Path:
    """Repack entire staging_dir into a .zip archive, preserving unknown files."""
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(staging_dir.rglob("*")):
            if p.is_file():
                arcname = str(p.relative_to(staging_dir)).replace(os.sep, "/")
                zf.write(p, arcname)
    return out_zip


def write_bundle_manifest(staging_dir: Path) -> None:
    """Create meta/bundle.json describing this bundle."""
    meta_dir = staging_dir / "meta"
    meta_dir.mkdir(exist_ok=True)
    manifest = {
        "bundle_schema_version": "1.0",
        "producer": "EVO",
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "format": "zip",
        "contents": {
            "seeds_glob": "seed_*/spec.json",
            "run_dir": "run/",
            "checksums": "run/checksums.txt",
            "index": "run/CONTENTS.json",
        },
    }
    (meta_dir / "bundle.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
