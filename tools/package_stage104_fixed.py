from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage104_release_gate import run_stage104_release_gate
from tools.export_stage104_artifacts import PACKAGE_NAME, export_stage104_artifacts


def package_stage104_fixed(root: Path | None = None, out_dir: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    out_dir = out_dir or root.parent
    export_stage104_artifacts(root)
    gate = run_stage104_release_gate(root)
    if gate.get("status") != "pass":
        raise SystemExit(f"stage104 gate blocked: {gate.get('issues')}")
    out = out_dir / PACKAGE_NAME
    exclude_dirs = {".git", "__pycache__", ".pytest_cache", ".gitnexus", ".venv"}
    exclude_suffixes = {".pyc", ".tmp", ".log"}
    names: list[str] = []
    with ZipFile(out, "w", ZIP_DEFLATED) as zf:
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if any(part in exclude_dirs for part in p.parts):
                continue
            if p.suffix in exclude_suffixes:
                continue
            arc = p.relative_to(root).as_posix()
            zf.write(p, arc)
            names.append(arc)
    with ZipFile(out) as zf:
        zip_names = zf.namelist()
    bad_sep = [name for name in zip_names if "\\" in name]
    cache = [name for name in zip_names if "__pycache__" in name or name.endswith(".pyc") or ".pytest_cache" in name or ".gitnexus" in name]
    if bad_sep or cache:
        raise SystemExit({"bad_sep": bad_sep[:5], "cache": cache[:5]})
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    sha_path = out.with_suffix(out.suffix + ".sha256")
    sha_path.write_text(sha + "\n", encoding="utf-8")
    filelist_path = out_dir / "V1700_stage104_FIXED_filelist.txt"
    filelist_path.write_text("\n".join(zip_names) + "\n", encoding="utf-8")
    integrity_path = out_dir / "stage104_FIXED_integrity_validation_report.md"
    integrity_path.write_text(
        "# Stage104 FIXED Integrity Validation Report\n\n"
        f"- status: pass\n- sha256: {sha}\n- entries: {len(zip_names)}\n"
        "- backslash_path_entries: 0\n- cache_entries: 0\n"
        "- stage104_release_gate: pass\n",
        encoding="utf-8",
    )
    return {
        "status": "pass",
        "zip": out.as_posix(),
        "sha256": sha,
        "filelist": filelist_path.as_posix(),
        "integrity_report": integrity_path.as_posix(),
        "entries": len(zip_names),
    }


if __name__ == "__main__":
    result = package_stage104_fixed()
    print(json.dumps(result, ensure_ascii=True, indent=2))
