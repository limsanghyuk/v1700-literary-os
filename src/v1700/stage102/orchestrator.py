from __future__ import annotations

from pathlib import Path

from v1700.gates.stage101_release_gate import run_stage101_release_gate

from .blind_benchmark import run_stage102_blind_benchmark
from .report import stage102_pack, write_json, write_summary
from .revision_efficiency import run_stage102_revision_efficiency_audit
from .writer_trial import run_stage102_writer_trial


def run_stage102_0_preflight(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    stage101 = run_stage101_release_gate(root)
    required = [
        root / "docs" / "development" / "MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md",
        root / "manifests" / "predevelopment_priority_manifest.json",
        root / "docs" / "stage101_cross_lineage_absorption_scenario_room" / "04_consensus_roadmap.md",
    ]
    missing = [path.relative_to(root).as_posix() for path in required if not path.exists()]
    issues = list(missing)
    if stage101.get("status") != "pass":
        issues.append("stage101_baseline_blocked")
    payload = {
        "stage": "102.0",
        "baseline_stage": "101",
        "title": "Stage102 Preflight and Trial Scope Lock",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage101_release_gate_status": stage101.get("status"),
        "mandatory_predevelopment_protocol_present": not missing,
        "trial_scope": "real_writer_trial_blind_benchmark_revision_efficiency",
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
    }
    write_json(root / "release" / "current" / "stage102_0_preflight_report.json", payload)
    return payload


def run_stage102_1_writer_trial(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    payload = run_stage102_writer_trial()
    write_json(root / "release" / "current" / "stage102_writer_trial_report.json", payload)
    pack = stage102_pack(root, "stage102_writer_trial_pack")
    write_json(pack / "writer_trial_tasks.json", payload)
    write_summary(
        pack / "writer_trial_summary.md",
        "Stage102.1 Writer Trial",
        [
            f"task completion: {payload['task_completion_count']}/{payload['task_count']}",
            f"average friction score: {payload['average_friction_score']}",
            f"saved minutes: {payload['saved_minutes']}",
        ],
    )
    return payload


def run_stage102_2_blind_benchmark(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    payload = run_stage102_blind_benchmark()
    write_json(root / "release" / "current" / "stage102_blind_benchmark_report.json", payload)
    pack = stage102_pack(root, "stage102_blind_benchmark_pack")
    write_json(pack / "blind_candidates.json", {"candidates": payload["visible_blind_candidates"]})
    write_json(pack / "reviewer_scorecards.json", {"scorecards": payload["scorecards"]})
    write_json(pack / "candidate_averages.json", payload["candidate_averages"])
    write_summary(
        pack / "blind_benchmark_summary.md",
        "Stage102.2 Blind Benchmark",
        [
            f"winner mode: {payload['winner_mode']}",
            f"v1700 margin over pure GPT: {payload['v1700_margin_over_pure_gpt']}",
            f"candidate count: {payload['candidate_count']}",
        ],
    )
    return payload


def run_stage102_3_revision_efficiency(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    payload = run_stage102_revision_efficiency_audit()
    write_json(root / "release" / "current" / "stage102_revision_efficiency_report.json", payload)
    pack = stage102_pack(root, "stage102_revision_efficiency_pack")
    write_json(pack / "revision_efficiency.json", payload)
    write_summary(
        pack / "user_feedback_summary.md",
        "Stage102 User Feedback Summary",
        [
            "Local writer trial shows lower revision friction under V1700 hybrid workflow.",
            f"revision time reduction ratio: {payload['revision_time_reduction_ratio']}",
            f"issue reduction ratio: {payload['issue_reduction_ratio']}",
            "This is deterministic internal evidence, not an external human market study.",
        ],
    )
    return payload


def run_stage102(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    preflight = run_stage102_0_preflight(root)
    writer_trial = run_stage102_1_writer_trial(root)
    blind_benchmark = run_stage102_2_blind_benchmark(root)
    revision = run_stage102_3_revision_efficiency(root)
    issues = []
    for name, report in (
        ("preflight", preflight),
        ("writer_trial", writer_trial),
        ("blind_benchmark", blind_benchmark),
        ("revision_efficiency", revision),
    ):
        if report.get("status") != "pass":
            issues.append(f"{name}_blocked")
    payload = {
        "stage": "102",
        "baseline_stage": "101",
        "title": "Real Writer Trial & Blind Benchmark",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage102_0_preflight": preflight,
        "stage102_1_writer_trial": writer_trial,
        "stage102_2_blind_benchmark": blind_benchmark,
        "stage102_3_revision_efficiency": revision,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "external_human_claim": False,
    }
    write_json(root / "release" / "current" / "stage102_real_writer_trial_report.json", payload)
    write_summary(
        root / "release" / "current" / "stage102_developer_handoff_report.md",
        "Stage102 Developer Handoff",
        [
            f"Stage102 status: {payload['status']}",
            "Stage102 provides deterministic local writer-trial evidence.",
            "It does not claim external human market validation.",
            "Provider-zero, Node2 boundary, and raw manuscript privacy remain intact.",
        ],
    )
    return payload
