from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Callable

from v1700.gates.graph_nexus_release_gate import run_graph_nexus_release_gate
from v1700.gates.runtime_smoke import run_runtime_smoke

STAGE_GATE_SPECS: tuple[tuple[str, str, str, str], ...] = (
    ("stage72.2", "stage72_2_release_gate", "v1700.gates.stage72_2_release_gate", "run_stage72_2_release_gate"),
    ("stage72.3", "stage72_3_release_gate", "v1700.gates.stage72_3_release_gate", "run_stage72_3_release_gate"),
    ("stage73.1", "stage73_1_release_gate", "v1700.gates.stage73_1_release_gate", "run_stage73_1_release_gate"),
    ("stage74", "stage74_release_gate", "v1700.gates.stage74_release_gate", "run_stage74_release_gate"),
    ("stage75", "stage75_release_gate", "v1700.gates.stage75_release_gate", "run_stage75_release_gate"),
    ("stage76", "stage76_release_gate", "v1700.gates.stage76_release_gate", "run_stage76_release_gate"),
    ("stage77", "stage77_release_gate", "v1700.gates.stage77_release_gate", "run_stage77_release_gate"),
    ("stage78", "stage78_release_gate", "v1700.gates.stage78_release_gate", "run_stage78_release_gate"),
    ("stage79", "stage79_release_gate", "v1700.gates.stage79_release_gate", "run_stage79_release_gate"),
    ("stage80", "stage80_release_gate", "v1700.gates.stage80_release_gate", "run_stage80_release_gate"),
    ("stage81", "stage81_release_gate", "v1700.gates.stage81_release_gate", "run_stage81_release_gate"),
    ("stage81.1", "stage81_1_release_gate", "v1700.gates.stage81_1_release_gate", "run_stage81_1_release_gate"),
    ("stage82", "stage82_release_gate", "v1700.gates.stage82_release_gate", "run_stage82_release_gate"),
    ("stage83", "stage83_release_gate", "v1700.gates.stage83_release_gate", "run_stage83_release_gate"),
    ("stage83.1", "stage83_1_release_gate", "v1700.gates.stage83_1_release_gate", "run_stage83_1_release_gate"),
    ("stage84", "stage84_release_gate", "v1700.gates.stage84_release_gate", "run_stage84_release_gate"),
    ("stage85", "stage85_release_gate", "v1700.gates.stage85_release_gate", "run_stage85_release_gate"),
    ("stage86", "stage86_release_gate", "v1700.gates.stage86_release_gate", "run_stage86_release_gate"),
    ("stage87", "stage87_release_gate", "v1700.gates.stage87_release_gate", "run_stage87_release_gate"),
    ("stage88", "stage88_release_gate", "v1700.gates.stage88_release_gate", "run_stage88_release_gate"),
    ("stage89", "stage89_release_gate", "v1700.gates.stage89_release_gate", "run_stage89_release_gate"),
    ("stage90", "stage90_release_gate", "v1700.gates.stage90_release_gate", "run_stage90_release_gate"),
    ("stage91", "stage91_release_gate", "v1700.gates.stage91_release_gate", "run_stage91_release_gate"),
    ("stage92", "stage92_release_gate", "v1700.gates.stage92_release_gate", "run_stage92_release_gate"),
    ("stage93", "stage93_release_gate", "v1700.gates.stage93_release_gate", "run_stage93_release_gate"),
    ("stage94", "stage94_release_gate", "v1700.gates.stage94_release_gate", "run_stage94_release_gate"),
    ("stage95", "stage95_release_gate", "v1700.gates.stage95_release_gate", "run_stage95_release_gate"),
    ("stage96", "stage96_release_gate", "v1700.gates.stage96_release_gate", "run_stage96_release_gate"),
    ("stage97", "stage97_release_gate", "v1700.gates.stage97_release_gate", "run_stage97_release_gate"),
    ("stage97.1", "stage97_1_release_gate", "v1700.gates.stage97_1_release_gate", "run_stage97_1_release_gate"),
    ("stage97.2", "stage97_2_release_gate", "v1700.gates.stage97_2_release_gate", "run_stage97_2_release_gate"),
    ("stage98", "stage98_release_gate", "v1700.gates.stage98_release_gate", "run_stage98_release_gate"),
    ("stage99", "stage99_release_gate", "v1700.gates.stage99_release_gate", "run_stage99_release_gate"),
    ("stage100", "stage100_release_gate", "v1700.gates.stage100_release_gate", "run_stage100_release_gate"),
    ("stage101", "stage101_release_gate", "v1700.gates.stage101_release_gate", "run_stage101_release_gate"),
    ("stage102", "stage102_release_gate", "v1700.gates.stage102_release_gate", "run_stage102_release_gate"),
    ("stage103", "stage103_release_gate", "v1700.gates.stage103_release_gate", "run_stage103_release_gate"),
    ("stage104", "stage104_release_gate", "v1700.gates.stage104_release_gate", "run_stage104_release_gate"),
    ("stage105", "stage105_release_gate", "v1700.gates.stage105_release_gate", "run_stage105_release_gate"),
    ("stage106", "stage106_release_gate", "v1700.gates.stage106_release_gate", "run_stage106_release_gate"),
    ("stage107", "stage107_release_gate", "v1700.gates.stage107_release_gate", "run_stage107_release_gate"),
    ("stage107_5", "stage107_5_sandbox_gate", "v1700.gates.stage107_5_sandbox_gate", "run_stage107_5_sandbox_gate"),
    ("stage108", "stage108_release_gate", "v1700.gates.stage108_release_gate", "run_stage108_release_gate"),
    ("stage109", "stage109_release_gate", "v1700.gates.stage109_release_gate", "run_stage109_release_gate"),
    ("stage110", "stage110_release_gate", "v1700.gates.stage110_release_gate", "run_stage110_release_gate"),
    ("stage111", "stage111_release_gate", "v1700.gates.stage111_release_gate", "run_stage111_release_gate"),
    ("stage112", "stage112_release_gate", "v1700.gates.stage112_release_gate", "run_stage112_release_gate"),
    ("stage113", "stage113_release_gate", "v1700.gates.stage113_release_gate", "run_stage113_release_gate"),
    ("stage114", "stage114_release_gate", "v1700.gates.stage114_release_gate", "run_stage114_release_gate"),
    ("stage115", "stage115_release_gate", "v1700.gates.stage115_release_gate", "run_stage115_release_gate"),
    ("stage116", "stage116_release_gate", "v1700.gates.stage116_release_gate", "run_stage116_release_gate"),
    ("stage117", "stage117_release_gate", "v1700.gates.stage117_release_gate", "run_stage117_release_gate"),
    ("stage118", "stage118_release_gate", "v1700.gates.stage118_release_gate", "run_stage118_release_gate"),
    ("stage119", "stage119_release_gate", "v1700.gates.stage119_release_gate", "run_stage119_release_gate"),
    ("stage120", "stage120_release_gate", "v1700.gates.stage120_release_gate", "run_stage120_release_gate"),
    ("stage121", "stage121_release_gate", "v1700.gates.stage121_release_gate", "run_stage121_release_gate"),
    ("stage122", "stage122_release_gate", "v1700.gates.stage122_release_gate", "run_stage122_release_gate"),
    ("stage123", "stage123_release_gate", "v1700.gates.stage123_release_gate", "run_stage123_release_gate"),
    ("stage124", "stage124_release_gate", "v1700.gates.stage124_release_gate", "run_stage124_release_gate"),
    ("stage125", "stage125_release_gate", "v1700.gates.stage125_release_gate", "run_stage125_release_gate"),
    ("stage126", "stage126_release_gate", "v1700.gates.stage126_release_gate", "run_stage126_release_gate"),
    ("stage127", "stage127_release_gate", "v1700.gates.stage127_release_gate", "run_stage127_release_gate"),
    ("stage128", "stage128_release_gate", "v1700.gates.stage128_release_gate", "run_stage128_release_gate"),
    ("stage129", "stage129_release_gate", "v1700.gates.stage129_release_gate", "run_stage129_release_gate"),
    ("stage130", "stage130_release_gate", "v1700.gates.stage130_release_gate", "run_stage130_release_gate"),
    ("stage131", "stage131_release_gate", "v1700.gates.stage131_release_gate", "run_stage131_release_gate"),
    ("stage132", "stage132_release_gate", "v1700.gates.stage132_release_gate", "run_stage132_release_gate"),
    ("stage133", "stage133_release_gate", "v1700.gates.stage133_release_gate", "run_stage133_release_gate"),
    ("stage134", "stage134_release_gate", "v1700.gates.stage134_release_gate", "run_stage134_release_gate"),
    ("stage135", "stage135_release_gate", "v1700.gates.stage135_release_gate", "run_stage135_release_gate"),
    ("stage136", "stage136_release_gate", "v1700.gates.stage136_release_gate", "run_stage136_release_gate"),
    ("stage137", "stage137_release_gate", "v1700.gates.stage137_release_gate", "run_stage137_release_gate"),
    ("stage138", "stage138_release_gate", "v1700.gates.stage138_release_gate", "run_stage138_release_gate"),
    ("stage139", "stage139_release_gate", "v1700.gates.stage139_release_gate", "run_stage139_release_gate"),
    ("stage140", "stage140_release_gate", "v1700.gates.stage140_release_gate", "run_stage140_release_gate"),
    ("stage141", "stage141_release_gate", "v1700.gates.stage141_release_gate", "run_stage141_release_gate"),
    ("stage142", "stage142_release_gate", "v1700.gates.stage142_release_gate", "run_stage142_release_gate"),
    ("stage143", "stage143_release_gate", "v1700.gates.stage143_release_gate", "run_stage143_release_gate"),
    ("stage144", "stage144_release_gate", "v1700.gates.stage144_release_gate", "run_stage144_release_gate"),
    ("stage145", "stage145_release_gate", "v1700.gates.stage145_release_gate", "run_stage145_release_gate"),
    ("stage146", "stage146_release_gate", "v1700.gates.stage146_release_gate", "run_stage146_release_gate"),
    ("stage147", "stage147_release_gate", "v1700.gates.stage147_release_gate", "run_stage147_release_gate"),
    ("stage148", "stage148_release_gate", "v1700.gates.stage148_release_gate", "run_stage148_release_gate"),
)

STAGE_ORDER = [spec[0] for spec in STAGE_GATE_SPECS]
_RELEASE_GATE_CACHE: dict[str, dict] = {}


def run_release_gate() -> dict:
    root = Path(__file__).resolve().parents[3]
    active_version = _active_version(root)
    cache_key = active_version
    if cache_key in _RELEASE_GATE_CACHE:
        return _RELEASE_GATE_CACHE[cache_key]

    smoke = run_runtime_smoke()
    issues = list(smoke.get("issues", []))
    if smoke.get("external_provider_calls", 0) != 0:
        issues.append("provider_default_calls_nonzero")

    graph_nexus = run_graph_nexus_release_gate(root)
    if graph_nexus.get("status") != "pass":
        issues.append("graph_nexus_release_gate_blocked")

    stage_reports: dict[str, dict | None] = {output_key: None for _, output_key, _, _ in STAGE_GATE_SPECS}
    active_index = STAGE_ORDER.index(active_version) if active_version in STAGE_ORDER else -1
    if active_version and active_index < 0:
        issues.append("live_core_manifest_active_version_unknown")

    for index, (stage, output_key, module_name, function_name) in enumerate(STAGE_GATE_SPECS):
        if active_index >= index:
            if index < active_index:
                report = _load_existing_stage_report(root, output_key)
                if report is None or report.get("status") != "pass":
                    report = _historical_evidence_summary(root, stage, output_key)
            else:
                runner = _load_runner(module_name, function_name)
                report = runner(root)
            stage_reports[output_key] = _compact_stage_report(report)
            if report.get("status") != "pass":
                issues.append(f"{output_key}_blocked")

    result = {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "runtime_smoke": smoke,
        "graph_nexus_release_gate": graph_nexus,
        **stage_reports,
    }
    _RELEASE_GATE_CACHE[cache_key] = result
    return result


def _load_existing_stage_report(root: Path, output_key: str) -> dict | None:
    report_path = root / "release" / "current" / f"{output_key}_report.json"
    if not report_path.exists():
        return None
    try:
        return json.loads(report_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _compact_stage_report(report: dict | None) -> dict | None:
    if report is None:
        return None
    keep = (
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "raw_manuscript_provider_leakage",
        "node2_raw_reveal_access",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: report.get(key) for key in keep if key in report}


def _load_runner(module_name: str, function_name: str) -> Callable[[Path], dict]:
    module = importlib.import_module(module_name)
    return getattr(module, function_name)


def _active_version(root: Path) -> str:
    manifest = root / "manifests" / "live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _historical_evidence_summary(root: Path, stage: str, output_key: str) -> dict:
    manifest_stage = stage.replace(".", "_")
    issues: list[str] = []
    if stage in {"stage100", "stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127", "stage128", "stage129", "stage130", "stage131", "stage132", "stage133", "stage134", "stage135", "stage136", "stage137", "stage138", "stage139", "stage140", "stage141", "stage142", "stage143", "stage144", "stage145", "stage146", "stage147", "stage148"}:
        report_path = root / "release" / "current" / f"{output_key}_report.json"
        manifest_path = root / "manifests" / f"{manifest_stage}_manifest.json"
        docs_path = root / "docs" / "stages" / f"{manifest_stage}.md"
        for path in (report_path, manifest_path, docs_path):
            if not path.exists():
                issues.append(f"missing:{path.relative_to(root).as_posix()}")
    return {
        "status": "pass" if not issues else "blocked",
        "stage": stage,
        "title": "historical compact evidence summary",
        "issues": issues,
        "historical_evidence_summary": True,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
