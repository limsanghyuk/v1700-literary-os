from v1700.studio_beta.review_queue_panel import build_review_queue_panel

def test_review_queue_has_no_unresolved_blocks():
    report = build_review_queue_panel()
    assert report["status"] == "pass"
    assert report["unresolved_block_count"] == 0
