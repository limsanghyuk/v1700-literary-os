from __future__ import annotations


def build_review_queue_panel() -> dict:
    items = [
        {
            "revision_id": "rev-001",
            "source": "stage101_scenario_room",
            "severity": "WARN",
            "issue_type": "dialogue_silence_balance",
            "recommendation": "shift exposition into prop cue and silence beat",
            "writer_decision": "PENDING",
        },
        {
            "revision_id": "rev-002",
            "source": "stage102_writer_trial",
            "severity": "INFO",
            "issue_type": "reader_orientation",
            "recommendation": "keep station location label visible in scene card",
            "writer_decision": "PENDING",
        },
    ]
    unresolved_block_count = sum(1 for item in items if item["severity"] == "BLOCK" and item["writer_decision"] not in {"APPROVED", "REJECTED"})
    return {
        "status": "pass" if unresolved_block_count == 0 else "blocked",
        "queue_id": "stage104-review-queue",
        "items": items,
        "revision_queue_size": len(items),
        "unresolved_block_count": unresolved_block_count,
        "writer_approval_required": True,
        "provider_call_count": 0,
    }
