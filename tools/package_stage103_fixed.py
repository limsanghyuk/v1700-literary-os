from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage103_release_gate import run_stage103_release_gate
from v1700.stage103.release_notes import PACKAGE_NAME

EXCLUDE_DIRS = {".git", ".gitnexus", ".venv", "__pycache__", ".pytest_cache"}
EXCLUDE_SUFFIXES = {".pyc", ".tmp", ".log"}


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    gate = run_stage103_release_gate(root)
    package_dir = root.parents[1] / "packages" if len(root.parents) > 1 else root.parent / "packages"
    package_dir.mkdir(parents=True, exist_ok=True)
    out = package_dir / PACKAGE_NAME
    names = package(root, out)
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    sha_path = out.with_suffix(out.suffix + ".sha256")
    filelist_path = package_dir / "V1700_stage103_FIXED_filelist.txt"
    integrity_path = package_dir / "stage103_FIXED_integrity_validation_report.md"
    sha_path.write_text(sha + "\n", encoding="utf-8")
    filelist_path.write_text("\n".join(names) + "\n", encoding="utf-8")
    validation = validate_zip(out)
    integrity_path.write_text(
        "# Stage103 FIXED Integrity Validation\n\n"
        f"- gate status: {gate['status']}\n"
        f"- zip status: {validation['status']}\n"
        f"- sha256: {sha}\n"
        f"- entries: {len(names)}\n",
        encoding="utf-8",
    )
    payload = {
        "status": "pass" if gate["status"] == "pass" and validation["status"] == "pass" else "blocked",
        "zip": str(out),
        "sha256": sha,
        "entries": len(names),
        **validation,
    }
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0 if payload["status"] == "pass" else 1


def package(root: Path, out: Path) -> list[str]:
    names: list[str] = []
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            if path.suffix in EXCLUDE_SUFFIXES:
                continue
            arc = path.relative_to(root).as_posix()
            zf.write(path, arc)
            names.append(arc)
    return names


def validate_zip(out: Path) -> dict:
    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
    bad_sep = [name for name in names if "\\" in name]
    cache = [name for name in names if "__pycache__" in name or name.endswith(".pyc") or ".pytest_cache" in name]
    forbidden = [name for name in names if name.startswith((".git/", ".gitnexus/", ".venv/"))]
    return {
        "status": "pass" if not bad_sep and not cache and not forbidden else "blocked",
        "zip_path_separator_status": "pass" if not bad_sep else "blocked",
        "clean_packaging_status": "pass" if not cache and not forbidden else "blocked",
        "bad_separator_entries": bad_sep[:10],
        "cache_entries": cache[:10],
        "forbidden_entries": forbidden[:10],
    }


if __name__ == "__main__":
    raise SystemExit(main())
