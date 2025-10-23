from __future__ import annotations

import hashlib
import json
import os
import tempfile
import zipfile
from pathlib import Path
from typing import Optional


class BundleError(Exception):
    pass


def _safe_extract(zf: zipfile.ZipFile, dest: Path) -> None:
    dest = dest.resolve()
    for zi in zf.infolist():
        target = (dest / zi.filename).resolve()
        if not str(target).startswith(str(dest)):
            raise BundleError("Illegal path in zip (zip-slip)")
        zf.extract(zi, dest)


def open_bundle(path: Path, staging_root: Optional[Path] = None) -> Path:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    root = Path(staging_root) if staging_root else Path(tempfile.mkdtemp(prefix="evo_bdl_"))
    with zipfile.ZipFile(p, "r") as zf:
        _safe_extract(zf, root)
    return root


def write_bundle(staging_dir: Path, out_zip: Path) -> Path:
    staging_dir = Path(staging_dir)
    out_zip = Path(out_zip)
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for base, _, files in os.walk(staging_dir):
            for fname in files:
                full = Path(base) / fname
                arc = full.relative_to(staging_dir)
                zf.write(full, arcname=str(arc))
    return out_zip


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def write_checksums(staging_dir: Path, rel_paths: list[str]) -> None:
    run_dir = Path(staging_dir) / "run"
    run_dir.mkdir(parents=True, exist_ok=True)
    lines = []
    for rp in rel_paths:
        fp = Path(staging_dir) / rp
        if fp.exists():
            lines.append(f"sha256  {sha256_file(fp)}  {rp}")
    contents = "\n".join(lines)
    if lines:
        contents += "\n"
    (run_dir / "checksums.txt").write_text(contents, encoding="utf-8")


def write_contents_index(staging_dir: Path) -> None:
    root = Path(staging_dir)
    files = []
    for base, _, names in os.walk(root):
        for n in names:
            full = Path(base) / n
            rel = full.relative_to(root)
            files.append(
                {
                    "path": str(rel).replace("\\", "/"),
                    "bytes": full.stat().st_size,
                    "sha256": sha256_file(full),
                }
            )
    run_dir = root / "run"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "CONTENTS.json").write_text(json.dumps({"files": files}, indent=2), encoding="utf-8")
