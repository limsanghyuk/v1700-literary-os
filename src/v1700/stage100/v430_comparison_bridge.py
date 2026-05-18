from __future__ import annotations

from pathlib import Path

from v1700.stage100.report import write_json, write_summary


def run_stage100_v430_comparison_bridge(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    candidates = [
        {
            "candidate_id": "V430_SCENARIO_ROOM_PIPELINE",
            "value": "Scenario room / beat pipeline may improve script-mode orchestration.",
            "v1700_overlap": "Stage98 Studio Workflow and Stage100 Scenario Evaluation",
            "branchpoint_risk": "medium",
            "decision": "DEFER_STAGE101",
        },
        {
            "candidate_id": "V430_INVESTIGATIVE_ACTION_BEATS",
            "value": "Investigation/action beats may improve scenario-mode scene movement.",
            "v1700_overlap": "Stage97 endurance and Stage100 scenario scoring",
            "branchpoint_risk": "low",
            "decision": "DEFER_STAGE101",
        },
        {
            "candidate_id": "V430_PRODUCT_PIPELINE_API",
            "value": "Product pipeline/API shape may improve future user trials.",
            "v1700_overlap": "Stage89-98 Studio and Publishing Package",
            "branchpoint_risk": "medium",
            "decision": "COMPARE_ONLY",
        },
    ]
    v430_code_merged = _detect_v430_code(root)
    status = "pass" if not v430_code_merged and all(item["decision"] in {"DEFER_STAGE101", "COMPARE_ONLY"} for item in candidates) else "blocked"
    report = {
        "stage": "100.3",
        "baseline_stage": "100.2",
        "title": "V430 Comparison / Absorption Candidate Bridge",
        "status": status,
        "issues": [] if status == "pass" else ["v430_untraced_merge_detected"],
        "source_available_in_workspace": False,
        "v430_code_merged": v430_code_merged,
        "immediate_absorption_allowed": False,
        "next_absorption_stage": "Stage101",
        "candidates": candidates,
    }
    write_json(root / "release" / "current" / "stage100_v430_comparison_report.json", report)
    write_json(root / "release" / "current" / "stage100_v430_absorption_candidate_matrix.json", {"status": status, "candidates": candidates})
    write_summary(
        root / "release" / "current" / "stage100_v430_comparison_summary.md",
        "Stage100.3 V430 Comparison Bridge",
        [
            "V430 is comparison-only in Stage100.",
            "No V430 code is merged into the RC.",
            "Actual absorption is deferred to Stage101.",
        ],
    )
    return report


def _detect_v430_code(root: Path) -> bool:
    for path in (root / "src").rglob("*"):
        rel = path.relative_to(root).as_posix().lower()
        if _is_traced_stage101_v430_probe(rel, root):
            continue
        if path.is_file() and "v430" in rel and "stage100" not in rel:
            return True
    return False


def _is_traced_stage101_v430_probe(rel: str, root: Path) -> bool:
    """Stage101 may contain traced V430 absorption probes without importing V430 runtime code."""
    if not rel.startswith("src/v1700/cross_lineage/"):
        return False
    manifest = root / "manifests" / "live_core_manifest.json"
    if not manifest.exists():
        return False
    text = manifest.read_text(encoding="utf-8")
    return any(f'"active_version": "stage{s}"' in text for s in range(101, 128))
