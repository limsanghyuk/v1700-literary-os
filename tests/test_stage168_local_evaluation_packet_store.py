from __future__ import annotations

import json
from pathlib import Path

from v1700.evaluation_packet_store.loader import load_evaluation_packets, validate_evaluation_packet_store
from v1700.evaluation_packet_store import run_stage168_local_evaluation_packet_store
from v1700.gates.stage168_release_gate import run_stage168_release_gate

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "samples/stage168_evaluation_packet_store/evaluation_packets.jsonl"


def test_stage168_evaluation_packet_store_fixture_validates() -> None:
    validation = validate_evaluation_packet_store(STORE, ROOT)
    assert validation["status"] == "pass"
    assert validation["packet_count"] >= 6
    assert all(entry["checksum"] == entry["expected_checksum"] for entry in validation["checksum_index"])


def test_stage168_packets_are_read_only_and_local_only() -> None:
    packets = load_evaluation_packets(STORE)
    assert packets
    assert all(packet["write_policy"] == "READ_ONLY_DISABLED_WRITE" for packet in packets)
    assert all(packet["evaluation_mode"] == "LOCAL_EVALUATION_ONLY" for packet in packets)


def test_stage168_report_passes_and_blocks_runtime_privilege() -> None:
    result = run_stage168_local_evaluation_packet_store(ROOT)
    assert result["status"] == "pass"
    assert result["evaluation_packet_count"] >= 6
    assert result["provider_evaluation_enabled"] is False
    assert result["evaluation_write_enabled"] is False
    assert result["stage166_refs_resolvable"] is True
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage168_release_gate_passes() -> None:
    result = run_stage168_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["stage168"]["evaluation_packet_count"] >= 6
    assert result["evaluation_write_enabled"] is False
    assert result["provider_evaluation_enabled"] is False


def test_stage168_tampered_checksum_blocks(tmp_path: Path) -> None:
    store = tmp_path / "evaluation_packets.jsonl"
    packet = load_evaluation_packets(STORE)[0]
    packet["packet_summary"] = "tampered"
    store.write_text(json.dumps(packet, ensure_ascii=False) + "\n", encoding="utf-8")
    validation = validate_evaluation_packet_store(store, ROOT)
    assert validation["status"] == "blocked"
    assert any(issue.startswith("checksum_mismatch") for issue in validation["issues"])


def test_stage168_missing_stage166_reference_blocks(tmp_path: Path) -> None:
    store = tmp_path / "evaluation_packets.jsonl"
    packet = load_evaluation_packets(STORE)[0]
    packet["required_stage_refs"] = ["release/current/does_not_exist.json"]
    packet["checksum"] = "invalid"
    store.write_text(json.dumps(packet, ensure_ascii=False) + "\n", encoding="utf-8")
    validation = validate_evaluation_packet_store(store, ROOT)
    assert validation["status"] == "blocked"
    assert any("missing_stage_ref" in issue for issue in validation["issues"])




def test_main_release_gate_rechecks_without_process_cache(monkeypatch) -> None:
    from v1700.gates import release_gate

    state = {"blocked": False}

    def fake_runtime_smoke():
        return {"status": "pass", "issues": [], "external_provider_calls": 0}

    def fake_graph_gate(root):
        return {"status": "pass", "issues": []}

    def fake_load_runner(module_name, function_name):
        def runner(root):
            if state["blocked"]:
                return {"status": "blocked", "issues": ["simulated_stage168_block"]}
            return {"status": "pass", "issues": []}
        return runner

    monkeypatch.setattr(release_gate, "STAGE_GATE_SPECS", (("stage168", "stage168_release_gate", "fake", "fake"),))
    monkeypatch.setattr(release_gate, "STAGE_ORDER", ["stage168"])
    monkeypatch.setattr(release_gate, "run_runtime_smoke", fake_runtime_smoke)
    monkeypatch.setattr(release_gate, "run_graph_nexus_release_gate", fake_graph_gate)
    monkeypatch.setattr(release_gate, "_load_runner", fake_load_runner)

    first = release_gate.run_release_gate()
    assert first["status"] == "pass"

    state["blocked"] = True
    second = release_gate.run_release_gate()
    assert second["status"] == "blocked"
    assert "stage168_release_gate_blocked" in second["issues"]
