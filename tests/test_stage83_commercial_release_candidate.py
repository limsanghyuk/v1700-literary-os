from pathlib import Path

from v1700.commercial_release import run_commercial_release_candidate
from v1700.gates.stage83_release_gate import run_stage83_release_gate


def test_stage83_commercial_release_candidate_generates_required_evidence(tmp_path: Path):
    result = run_commercial_release_candidate(root=tmp_path)
    assert result["status"] == "pass"
    manifest = result["commercial_release_manifest"]
    assert manifest["episode_count"] == 3
    assert manifest["actual_rendered_scene_count"] >= 30
    assert manifest["quality_average_after"] >= 8.0
    assert manifest["quality_average_delta"] >= 0.5
    assert manifest["reveal_leakage_count"] == 0
    assert manifest["timeline_contradiction_count"] == 0
    assert manifest["blind_v1700_margin_over_pure_gpt"] >= 1.0
    for rel in manifest["episode_files"]:
        path = tmp_path / rel
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "Rendered Scene Drafts" in text
        assert "LOCKED_REVEAL" not in text


def test_stage83_release_gate_passes():
    result = run_stage83_release_gate()
    assert result["status"] == "pass"
    assert result["episode_count"] == 3
    assert result["actual_rendered_scene_count"] >= 30
    assert result["quality_average_after"] >= 8.0
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access_count"] == 0
