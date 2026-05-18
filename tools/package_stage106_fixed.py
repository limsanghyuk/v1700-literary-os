from __future__ import annotations
import hashlib, json, sys, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
PACKAGE = "V1700_stage106_adaptive_author_profile_style_genome_FIXED.zip"


def package_stage106_fixed(root: Path | None = None, out_dir: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    out_dir = out_dir or root.parent
    out = out_dir / PACKAGE
    exclude_dirs = {".git", "__pycache__", ".pytest_cache", ".gitnexus", ".venv", "venv"}
    exclude_suffixes = {".pyc", ".tmp", ".log"}
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(root).parts
            rel = path.relative_to(root).as_posix()
            if any(part in exclude_dirs for part in rel_parts):
                continue
            if path.suffix in exclude_suffixes:
                continue
            zf.write(path, rel)
    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
    bad_sep = [n for n in names if "\\" in n]
    cache = [n for n in names if "__pycache__" in n or n.endswith(".pyc") or ".pytest_cache" in n or ".gitnexus" in n]
    if bad_sep or cache:
        raise SystemExit({"bad_sep": bad_sep[:5], "cache": cache[:5]})
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    (out_dir / f"{PACKAGE}.sha256").write_text(sha + "\n", encoding="utf-8")
    (out_dir / "V1700_stage106_FIXED_filelist.txt").write_text("\n".join(names) + "\n", encoding="utf-8")
    report = {"stage": "106", "status": "pass", "package": out.name, "sha256": sha, "entries": len(names), "backslash_path_entries": len(bad_sep), "cache_entries": len(cache)}
    (out_dir / "stage106_FIXED_integrity_validation_report.md").write_text("# Stage106 FIXED Integrity Validation Report\n\n" + "\n".join(f"- {k}: {v}" for k, v in report.items()) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    result = package_stage106_fixed()
    print(json.dumps(result, ensure_ascii=True, indent=2))
