from v1700.gates.stage107_release_gate import _check


def test_stage107_negative_guard_blocks_false_condition():
    assert _check(False)["status"] == "blocked"
