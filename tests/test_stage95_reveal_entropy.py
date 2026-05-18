from v1700.narrative_physics.reveal_entropy import RevealEntropyBudgetEngine


def test_stage95_reveal_entropy_blocks_raw_reveal_marker():
    evidence = {
        "episodes": [
            {
                "episode_id": "E01",
                "blocked_direct_reveal_count": 1,
                "reveal_policy_count": 1,
                "scenes": [{"text": "RAW_REVEAL: hidden"}],
            }
        ]
    }

    report = RevealEntropyBudgetEngine().calculate(evidence).to_dict()
    assert report["status"] == "blocked"
    assert report["reveal_leakage_count"] == 1
