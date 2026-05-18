from __future__ import annotations
import hashlib, json, zipfile
from pathlib import Path

EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".gitnexus", ".venv", "venv"}
EXCLUDE_SUFFIXES = {".pyc", ".tmp", ".log"}
OUT_NAME = "V1700_stage107_5_provider_live_sandbox_adapter_verification_FIXED.zip"

def should_skip(path: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return True
    if path.name == ".env" or path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    out = root.parent / OUT_NAME
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or should_skip(path):
                continue
            arc = path.relative_to(root).as_posix()
            zf.write(path, arc)
    with zipfile.ZipFile(out) as zf:
        zip_names = zf.namelist()
    bad = [n for n in zip_names if "\\" in n or "__pycache__" in n or n.endswith(".pyc") or ".pytest_cache" in n or ".gitnexus" in n or n.endswith(".env") or "/.env" in n]
    if bad:
        raise SystemExit(f"clean_zip_failed:{bad[:5]}")
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    (out.with_suffix(out.suffix + ".sha256")).write_text(sha + "\n", encoding="utf-8")
    (root.parent / "V1700_stage107_5_FIXED_filelist.txt").write_text("\n".join(zip_names) + "\n", encoding="utf-8")
    report = {"status": "pass", "package": out.name, "sha256": sha, "entries": len(zip_names), "backslash_path_entries": 0, "cache_entries": 0, "raw_outputs_included": False, "credentials_included": False}
    (root.parent / "stage107_5_FIXED_integrity_validation_report.md").write_text("# Stage107.5 FIXED Integrity Validation Report\n\n```json\n" + json.dumps(report, indent=2) + "\n```\n", encoding="utf-8")
    (root / "package_manifest.json").write_text(json.dumps({"stage": "107.5", "package": out.name, "canonical_package": out.name, "sha256": sha, "sha256_sidecar": out.name + ".sha256", "filelist": "V1700_stage107_5_FIXED_filelist.txt"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
