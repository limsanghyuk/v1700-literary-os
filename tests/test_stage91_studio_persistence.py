from v1700.gates.stage91_release_gate import run_stage91_release_gate
from v1700.writer_studio.event_replay import StudioEventReplayEngine, run_stage91_event_replay_smoke
from v1700.writer_studio.persistence import StudioPersistenceStore, build_stage91_base_workspace
from v1700.writer_studio.review_queue import StudioReviewQueue


def test_stage91_base_workspace_preserves_stage90_lineage():
    workspace = build_stage91_base_workspace()
    assert workspace.stage == "91"
    assert workspace.status == "pass"
    assert "stage90" in workspace.inherited_stages
    assert workspace.provider_default_calls == 0
    assert workspace.node2_raw_reveal_access_count == 0
    assert "persistence_snapshot" in workspace.export_targets


def test_stage91_persistence_snapshots_are_checksum_bearing():
    workspace = build_stage91_base_workspace()
    store = StudioPersistenceStore()
    first = store.persist(workspace, sequence=0, reason="test_initial", review_queue_size=0, event_count=0)
    second = store.persist(workspace, sequence=1, reason="test_repeat", review_queue_size=0, event_count=1)
    assert first.checksum == second.checksum
    assert first.panel_count == workspace.panel_count
    assert first.item_count >= 30
    assert store.latest().snapshot_id == "stage91_snapshot_001"


def test_stage91_review_queue_state_machine_resolves_blocking_items():
    queue = StudioReviewQueue()
    item = queue.add_item(
        source_event_id="EV_TEST",
        panel_id="reveal_budget_board",
        severity="blocking",
        category="reveal_policy",
        summary="Reveal policy requires approval.",
        branchpoint_refs=("BP_STAGE86_EPISODE_REVEAL_BUDGET",),
    )
    assert queue.report().status == "blocked"
    queue.transition(item.item_id, status="approved", note="approved in test")
    report = queue.report()
    assert report.blocking_count == 0
    assert report.approved_count == 1


def test_stage91_event_replay_smoke_passes():
    result = run_stage91_event_replay_smoke()
    assert result["status"] == "pass"
    assert result["event_count"] >= 18
    assert result["replayed_event_count"] == result["event_count"]
    assert result["persistence_snapshot_count"] >= 3
    assert result["review_queue_total_items"] >= 6
    assert result["review_queue_blocking_count"] == 0
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access_count"] == 0


def test_stage91_event_replay_checksum_is_deterministic():
    first = StudioEventReplayEngine().replay().to_dict()
    second = StudioEventReplayEngine().replay().to_dict()
    assert first["replay_checksum"] == second["replay_checksum"]
    assert first["snapshot_checksums"] == second["snapshot_checksums"]


def test_stage91_release_gate_passes():
    result = run_stage91_release_gate()
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access_count"] == 0
