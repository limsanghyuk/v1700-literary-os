from v1700.narrative_memory.curator import CuratedNode, NarrativeMemoryCurator


def test_narrative_memory_curator_preserves_branchpoints_and_debts():
    nodes = [
        CuratedNode("old", score=0.01, last_episode_idx=1),
        CuratedNode("branch", score=0.01, last_episode_idx=1, node_type="branchpoint"),
        CuratedNode("debt", score=0.01, last_episode_idx=1, node_type="payoff_debt"),
    ]
    report = NarrativeMemoryCurator().curate(nodes, current_episode=24, dry_run=True)
    assert report.status == "pass"
    assert report.removed_count == 1
    assert report.protected_preserved == 2
