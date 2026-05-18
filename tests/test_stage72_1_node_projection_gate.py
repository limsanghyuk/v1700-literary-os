from pathlib import Path

from v1700.gates.node_projection_gate import run_node_projection_gate
from v1700.graph_nexus.graph_nexus_packet import Node2GraphSurfacePacket


ROOT = Path(__file__).resolve().parents[1]


def test_node2_projection_receives_surface_safe_packet_only():
    report = run_node_projection_gate(ROOT)

    assert report["status"] == "pass"
    assert report["node2_raw_graph_access"] is False
    assert report["node2_packet"]["packet_type"] == "Node2GraphSurfacePacket"
    assert "raw_secret" not in report["node2_packet"]


def test_node2_projection_rejects_raw_secret():
    packet = Node2GraphSurfacePacket(scene_id="S", raw_secret="unreleased canon")

    try:
        packet.to_dict()
    except AssertionError as exc:
        assert "raw_secret" in str(exc)
    else:
        raise AssertionError("raw secret should be rejected")
