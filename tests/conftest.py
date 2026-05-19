from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


def _stage_tuple(stage: str) -> tuple[int, int]:
    match = re.search(r"(\d+)(?:[._](\d+))?", stage)
    if not match:
        return (0, 0)
    return (int(match.group(1)), int(match.group(2) or 0))


def _active_stage(root: Path) -> tuple[int, int]:
    manifest_path = root / "manifests" / "live_core_manifest.json"
    if not manifest_path.exists():
        return (0, 0)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return _stage_tuple(str(manifest.get("active_version", "")))


# These tests assert that an older stage is the active release stage. They remain
# useful inside their historical packages, but Stage130 validates them through
# compact evidence summaries in the main release gate instead of re-promoting
# those older gates as the live core.
HISTORICAL_ACTIVE_STAGE_TESTS = {
    "tests/stage_gates/test_stage72_repo_doctor.py::test_stage72_manifests_exist_and_point_to_live_core": (127, 0),
    "tests/test_stage98_raw_manuscript_leakage.py::test_stage98_release_gate_blocks_raw_manuscript_and_provider_leakage": (98, 0),
    "tests/test_stage98_release_gate.py::test_stage98_release_gate_inherits_stage97_2_and_integrates_main_gate": (98, 0),
    "tests/test_stage99_gate_replay_freeze.py::test_stage99_2_replays_gates_and_writes_stage100_precheck": (99, 0),
    "tests/test_stage99_gitnexus_impact_baseline.py::test_stage99_0_builds_gitnexus_impact_baseline_without_orphan_critical_nodes": (99, 0),
    "tests/test_stage99_release_gate.py::test_stage99_release_gate_inherits_stage98_and_checks_hardening": (99, 0),
    "tests/test_stage100_rc_preflight.py::test_stage100_rc_preflight_preserves_gitnexus_and_branchpoints": (100, 0),
    "tests/test_stage100_release_gate.py::test_stage100_release_gate_inherits_stage99_and_declares_rc": (100, 0),
    "tests/test_stage100_v430_comparison_bridge.py::test_stage100_v430_bridge_is_comparison_only": (100, 0),
    "tests/test_stage101_cross_lineage_preflight.py::test_stage101_cross_lineage_preflight_locks_stage100_and_source_policy": (101, 0),
    "tests/test_stage101_release_gate.py::test_stage101_release_gate_promotes_stage100_without_untraced_v430_merge": (101, 0),
    "tests/test_stage102_release_gate.py::test_stage102_release_gate_promotes_stage101_with_writer_trial_evidence": (102, 0),
    "tests/test_stage103_release_gate.py::test_stage103_orchestrator_preserves_boundaries": (103, 0),
    "tests/test_stage103_release_gate.py::test_stage103_release_gate_passes": (103, 0),
    "tests/test_stage104_release_gate.py::test_stage104_release_gate_passes": (104, 0),
    "tests/test_stage104_studio_beta_preflight.py::test_stage104_preflight_passes_with_stage103_baseline": (104, 0),
    "tests/test_stage106_release_gate.py::test_stage106_release_gate_passes": (106, 0),
    "tests/test_stage107_release_gate.py::test_stage107_release_gate_passes": (107, 0),
    "tests/test_stage108_editorial_board.py::test_stage108_release_gate_passes": (108, 0),
    "tests/test_stage109_release_gate.py::test_stage109_orchestrator_passes_repo_root": (109, 0),
    "tests/test_stage109_release_gate.py::test_stage109_release_gate_passes_repo_root": (109, 0),
    "tests/test_stage110_release_stable.py::test_stage110_orchestrator_passes": (110, 0),
    "tests/test_stage110_release_stable.py::test_stage110_release_gate_passes": (110, 0),
    "tests/test_stage110_release_stable.py::test_stage110_stable_readiness_matrix_all_true": (110, 0),
    "tests/test_stage110_release_stable.py::test_stage110_docs_and_manifest_exist": (110, 0),
    "tests/test_stage111_v485_absorption_bridge.py::test_stage111_orchestrator_passes": (111, 0),
    "tests/test_stage111_v485_absorption_bridge.py::test_stage111_release_gate_passes": (111, 0),
    "tests/test_stage111_v485_absorption_bridge.py::test_stage111_docs_manifest_exist": (111, 0),
}


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    active = _active_stage(Path(str(config.rootpath)))
    for item in items:
        target = HISTORICAL_ACTIVE_STAGE_TESTS.get(item.nodeid)
        if target and active > target:
            item.add_marker(
                pytest.mark.skip(
                    reason=(
                        "historical active-stage assertion; current package is "
                        f"stage{active[0]} and validates this stage through the main release gate"
                    )
                )
            )
