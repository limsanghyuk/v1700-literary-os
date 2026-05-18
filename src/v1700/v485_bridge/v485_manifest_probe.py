from __future__ import annotations
import json, re, os
from pathlib import Path
from .contracts import V485VersionDriftReport

REFERENCE_PROFILE = {
    "package_label": "literary_os_v485_COMPLETE.zip",
    "readme_version": "V430",
    "pyproject_version": "4.8.5",
    "manifest_version": "V485",
    "live_manifest_version": "V481",
    "release_gate_version": "V480",
}

def probe_v485_version_profile(source_dir: Path | None = None) -> dict:
    source_dir = source_dir or _source_from_env()
    if source_dir and source_dir.exists():
        profile = _probe_source_dir(source_dir)
        profile["source_mode"] = "external_source_probe"
    else:
        profile = dict(REFERENCE_PROFILE)
        profile["source_mode"] = "reference_profile_no_external_source_required"
    versions = {profile.get(k, "") for k in ("readme_version", "manifest_version", "live_manifest_version", "release_gate_version")}
    drift = len({v for v in versions if v}) > 1
    report = V485VersionDriftReport(
        package_label=profile.get("package_label", "unknown"),
        readme_version=profile.get("readme_version", "unknown"),
        pyproject_version=profile.get("pyproject_version", "unknown"),
        manifest_version=profile.get("manifest_version", "unknown"),
        live_manifest_version=profile.get("live_manifest_version", "unknown"),
        release_gate_version=profile.get("release_gate_version", "unknown"),
        drift_detected=drift,
        release_block=False,
        direct_metadata_import_allowed=False,
    ).to_dict()
    report["status"] = "pass"
    report["v1700_absorption_policy"] = "metadata_wrapper_required"
    report["source_mode"] = profile.get("source_mode")
    return report

def _source_from_env() -> Path | None:
    raw = os.environ.get("V1700_V485_SOURCE_DIR")
    return Path(raw) if raw else None

def _probe_source_dir(source: Path) -> dict:
    root = source
    if (source / "literary_os_v430_COMPLETE").exists():
        root = source / "literary_os_v430_COMPLETE"
    profile = dict(REFERENCE_PROFILE)
    profile["package_label"] = root.name
    readme = root / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8", errors="ignore")[:2000]
        m = re.search(r"V\d+", text)
        if m:
            profile["readme_version"] = m.group(0)
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"version\s*=\s*['\"]([^'\"]+)", text)
        if m:
            profile["pyproject_version"] = m.group(1)
        vm = re.search(r"V\d+", text)
        if vm:
            profile.setdefault("pyproject_label", vm.group(0))
    manifests = root / "manifests"
    if manifests.exists():
        names = [p.name for p in manifests.glob("*V485*")]
        if names:
            profile["manifest_version"] = "V485"
        live = manifests / "live_core_manifest.json"
        if live.exists():
            try:
                data = json.loads(live.read_text(encoding="utf-8"))
                av = str(data.get("active_version", ""))
                m = re.search(r"V?\d+", av, re.I)
                if m:
                    profile["live_manifest_version"] = m.group(0).upper() if m.group(0).lower().startswith("v") else "V" + m.group(0)
            except Exception:
                pass
    rg = root / "tools" / "run_release_gate.py"
    if rg.exists():
        text = rg.read_text(encoding="utf-8", errors="ignore")[:3000]
        m = re.findall(r"V\d+", text)
        if m:
            profile["release_gate_version"] = m[-1]
    return profile
