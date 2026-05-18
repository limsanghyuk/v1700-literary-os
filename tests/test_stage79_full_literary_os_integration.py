from v1700.gates.stage79_release_gate import run_stage79_release_gate
from v1700.integration import run_full_literary_os_smoke


def test_stage79_integrates_all_reabsorbed_branchpoints():
    report = run_full_literary_os_smoke()
    assert report["status"] == "pass"
    final = report["final_output"]
    assert final["episode_count"] == 3
    assert final["sequence_count_total"] >= 29
    assert final["scene_count_total"] >= 532
    assert final["rendered_scene_count"] >= 3
    assert report["node2_raw_reveal_access_count"] == 0
    assert report["provider_default_calls"] == 0


def test_stage79_release_gate():
    assert run_stage79_release_gate()["status"] == "pass"
