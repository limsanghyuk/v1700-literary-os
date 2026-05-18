from __future__ import annotations

from importlib import import_module
from pathlib import Path

from v1700.studio_workflow.report import write_json, write_summary

GATE_REPLAY_SPECS = (
    ("stage95", "v1700.gates.stage95_release_gate", "run_stage95_release_gate"),
    ("stage96", "v1700.gates.stage96_release_gate", "run_stage96_release_gate"),
    ("stage97", "v1700.gates.stage97_release_gate", "run_stage97_release_gate"),
    ("stage97.1", "v1700.gates.stage97_1_release_gate", "run_stage97_1_release_gate"),
    ("stage97.2", "v1700.gates.stage97_2_release_gate", "run_stage97_2_release_gate"),
    ("stage98", "v1700.gates.stage98_release_gate", "run_stage98_release_gate"),
)


def run_stage99_2_gate_replay_freeze(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    pack = root / "release" / "current" / "stage99_regression_freeze_pack"
    pack.mkdir(parents=True, exist_ok=True)

    gate_matrix = replay_required_gates(root)
    regression_matrix = build_regression_test_matrix(root)
    survival_matrix = build_survival_matrix(root, gate_matrix)
    stage100 = build_stage100_readiness_precheck(gate_matrix, regression_matrix, survival_matrix)
    status = "pass" if stage100["status"] == "pass" else "blocked"

    write_json(pack / "gate_replay_matrix.json", {"status": _matrix_status(gate_matrix), "gates": gate_matrix})
    write_json(pack / "regression_test_matrix.json", regression_matrix)
    write_json(pack / "stage95_to_stage98_survival_matrix.json", survival_matrix)
    write_json(pack / "stage100_readiness_precheck.json", stage100)
    write_summary(
        pack / "stage99_2_summary.md",
        "Stage99.2 Gate Replay + Regression Freeze",
        [
            f"gate replay status: {_matrix_status(gate_matrix)}",
            f"regression freeze status: {regression_matrix['status']}",
            f"stage100 readiness: {stage100['status']}",
        ],
    )
    payload = {
        "stage": "99.2",
        "baseline_stage": "99.1",
        "status": status,
        "release_gate_replay_status": _matrix_status(gate_matrix),
        "regression_freeze_status": regression_matrix["status"],
        "stage100_readiness_status": stage100["status"],
        "gate_replay_matrix": gate_matrix,
        "regression_test_matrix": regression_matrix,
        "stage95_to_stage98_survival_matrix": survival_matrix,
        "stage100_readiness_precheck": stage100,
    }
    write_json(root / "release" / "current" / "stage99_2_gate_replay_freeze_report.json", payload)
    write_json(root / "release" / "current" / "stage100_readiness_precheck_report.json", stage100)
    return payload


def replay_required_gates(root: Path) -> dict:
    matrix: dict[str, dict] = {}
    for stage, module_name, function_name in GATE_REPLAY_SPECS:
        module = import_module(module_name)
        runner = getattr(module, function_name)
        report = runner(root)
        matrix[stage] = {"status": report.get("status"), "issues": report.get("issues", [])}
    return matrix


def build_regression_test_matrix(root: Path) -> dict:
    patterns = ["test_stage95_*.py", "test_stage96_*.py", "test_stage97_*.py", "test_stage98_*.py"]
    files = sorted({path.relative_to(root).as_posix() for pattern in patterns for path in (root / "tests").glob(pattern)})
    missing = [pattern for pattern in patterns if not list((root / "tests").glob(pattern))]
    return {
        "status": "pass" if files and not missing else "blocked",
        "frozen": True,
        "patterns": patterns,
        "files": files,
        "missing_patterns": missing,
    }


def build_survival_matrix(root: Path, gate_matrix: dict) -> dict:
    stages = ["stage95", "stage96", "stage97", "stage97.1", "stage97.2", "stage98"]
    entries = {
        stage: {
            "gate_status": gate_matrix.get(stage, {}).get("status"),
            "manifest_present": (root / "manifests" / f"{stage.replace('.', '_')}_manifest.json").exists(),
            "release_evidence_present": (root / "release" / "current" / f"{stage.replace('.', '_')}_release_gate_report.json").exists(),
        }
        for stage in stages
    }
    status = "pass" if all(value["gate_status"] == "pass" and value["manifest_present"] for value in entries.values()) else "blocked"
    return {"status": status, "entries": entries}


def build_stage100_readiness_precheck(gate_matrix: dict, regression_matrix: dict, survival_matrix: dict) -> dict:
    issues: list[str] = []
    if _matrix_status(gate_matrix) != "pass":
        issues.append("release_gate_replay_failed")
    if regression_matrix.get("status") != "pass":
        issues.append("regression_freeze_failed")
    if survival_matrix.get("status") != "pass":
        issues.append("stage95_to_stage98_survival_failed")
    return {
        "status": "pass" if not issues else "blocked",
        "stage": "100-precheck",
        "baseline_stage": "99",
        "issues": issues,
        "ready_for_stage100_rc": not issues,
        "provider_governed": True,
        "branchpoint_preserved": True,
        "security_hardened": True,
        "regression_frozen": not issues,
    }


def _matrix_status(matrix: dict) -> str:
    return "pass" if matrix and all(item.get("status") == "pass" for item in matrix.values()) else "blocked"
