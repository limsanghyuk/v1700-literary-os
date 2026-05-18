from v1700.studio_beta.apply_guard import run_revision_apply_guard

def test_writer_decision_guard_blocks_unauthorized_apply():
    guard = run_revision_apply_guard()
    assert guard["status"] == "pass"
    assert guard["writer_approval_required"] is True
    assert guard["unauthorized_apply_count"] == 0
