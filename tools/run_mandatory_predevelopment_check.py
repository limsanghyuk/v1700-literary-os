from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _gitnexus_status(root: Path) -> dict:
    command = shutil.which("gitnexus.cmd") or shutil.which("gitnexus")
    if not command:
        return {"installed": False, "status": "fallback_required", "optional_runtime_dependency": True}
    try:
        result = subprocess.run([command, "status"], cwd=root, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=30, check=False)
    except Exception as exc:
        return {"installed": True, "status": "fallback_required", "error": str(exc), "optional_runtime_dependency": True}
    output = (result.stdout or "") + (result.stderr or "")
    return {"installed": result.returncode == 0, "status": "pass" if result.returncode == 0 and "up-to-date" in output.lower() else "fallback_required", "command": command, "output_excerpt": output[:1000], "optional_runtime_dependency": True}


def run_mandatory_predevelopment_check(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    manifest_path = root / "manifests" / "predevelopment_priority_manifest.json"
    live_manifest_path = root / "manifests" / "live_core_manifest.json"
    live_manifest = _read_json(live_manifest_path) if live_manifest_path.exists() else {}
    active_version = str(live_manifest.get("active_version", "stage101"))
    active_gate_path = root / "release" / "current" / f"{active_version.replace('.', '_')}_release_gate_report.json"
    main_gate_path = root / "release" / "current" / "release_gate_report.json"
    package_manifest_path = root / "package_manifest.json"
    sha_path = root / "SHA256SUMS.txt"

    priority_manifest = _read_json(manifest_path) if manifest_path.exists() else {}
    workflow_documents = priority_manifest.get("workflow_documents", [])
    required_files = [
        manifest_path,
        root / "docs" / "development" / "MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md",
        live_manifest_path,
        active_gate_path,
        main_gate_path,
        package_manifest_path,
        sha_path,
        *[root / rel for rel in workflow_documents],
    ]
    missing = [path.relative_to(root).as_posix() for path in required_files if not path.exists()]

    active_gate = _read_json(active_gate_path) if active_gate_path.exists() else {}
    main_gate = _read_json(main_gate_path) if main_gate_path.exists() else {}
    package_manifest = _read_json(package_manifest_path) if package_manifest_path.exists() else {}
    invariants = priority_manifest.get("invariants", {})

    canonical_package = str(package_manifest.get("canonical_package") or package_manifest.get("package") or live_manifest.get("canonical_package", ""))
    sidecar = str(package_manifest.get("sha256_sidecar") or live_manifest.get("canonical_sha256_sidecar", f"{canonical_package}.sha256"))

    invariant_checks = {
        "provider_default_calls": live_manifest.get("provider_default_calls") == invariants.get("provider_default_calls", 0),
        "active_stage_gate_pass": active_gate.get("status") == "pass",
        "main_release_gate_pass": main_gate.get("status") == "pass",
        "branchpoint_lineage_preserved": bool(invariants.get("branchpoint_lineage_preserved")),
        "python_fallback_required": bool(invariants.get("python_fallback_required")),
        "gitnexus_runtime_dependency_required_false": invariants.get("gitnexus_runtime_dependency_required") is False,
        "github_main_green_required": invariants.get("github_main_green_required") is True,
        "release_assets_triplet_required": invariants.get("release_assets_triplet_required") is True,
        "release_zip_declared": canonical_package.endswith(".zip"),
        "release_sidecar_declared": sidecar.endswith(".sha256"),
        "sha256sums_present": sha_path.exists(),
    }
    gitnexus = _gitnexus_status(root)
    status = "pass" if not missing and all(invariant_checks.values()) else "blocked"
    if gitnexus["status"] != "pass" and not invariants.get("python_fallback_required"):
        status = "blocked"

    payload = {
        "stage": "predevelopment",
        "status": status,
        "issues": missing + [name for name, ok in invariant_checks.items() if not ok],
        "active_version": active_version,
        "priority_manifest": manifest_path.relative_to(root).as_posix(),
        "mandatory_protocol": "docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md",
        "workflow_documents": workflow_documents,
        "gitnexus": gitnexus,
        "invariant_checks": invariant_checks,
        "must_check": priority_manifest.get("must_check", []),
    }
    out = root / "release" / "current" / "mandatory_predevelopment_check_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    result = run_mandatory_predevelopment_check()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
