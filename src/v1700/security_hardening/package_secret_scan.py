from __future__ import annotations

import json
import zipfile
from pathlib import Path


def scan_package_cleanliness(root: Path) -> dict:
    zip_paths = _active_release_packages(root)
    bad_sep: list[str] = []
    cache_entries: list[str] = []
    for zip_path in zip_paths:
        with zipfile.ZipFile(zip_path) as zf:
            for name in zf.namelist():
                if "\\" in name:
                    bad_sep.append(f"{zip_path.name}:{name}")
                if "__pycache__" in name or name.endswith(".pyc") or ".pytest_cache" in name:
                    cache_entries.append(f"{zip_path.name}:{name}")
    return {
        "status": "pass" if not bad_sep and not cache_entries else "blocked",
        "zip_path_separator_status": "pass" if not bad_sep else "blocked",
        "clean_packaging_status": "pass" if not cache_entries else "blocked",
        "bad_separator_entries": bad_sep[:20],
        "cache_entries": cache_entries[:20],
        "packages_scanned": [path.name for path in zip_paths],
        "scan_scope": "active_release_packages_only",
    }


def _active_release_packages(root: Path) -> list[Path]:
    """Scan only the active release package, not stale historical ZIPs nearby."""
    package_dirs = [root, root.parent]
    if len(root.parents) > 1:
        package_dirs.append(root.parents[1] / "packages")

    package_names = _declared_package_names(root)
    exact_matches: list[Path] = []
    for package_dir in package_dirs:
        if not package_dir.exists():
            continue
        for name in package_names:
            path = package_dir / name
            if path.exists():
                exact_matches.append(path)
    if exact_matches:
        return _dedupe(exact_matches)

    active_version = _active_version(root)
    if active_version:
        pattern = f"*{active_version.lower()}*FIXED*.zip"
        fallback_matches = [
            path
            for package_dir in package_dirs
            if package_dir.exists()
            for path in sorted(package_dir.glob(pattern))
        ]
        if fallback_matches:
            return _dedupe(fallback_matches)

    return []


def _declared_package_names(root: Path) -> list[str]:
    names: list[str] = []
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    package = manifest.get("canonical_package")
    if isinstance(package, str) and package.endswith(".zip"):
        names.append(package)
    return names


def _active_version(root: Path) -> str:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    version = manifest.get("active_version", "")
    return str(version).replace("_", "").lower()


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _dedupe(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    unique: list[Path] = []
    for path in paths:
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique
