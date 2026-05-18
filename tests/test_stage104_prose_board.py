from v1700.studio_beta.prose_board import build_prose_board

def test_prose_board_passes_without_provider_calls():
    board = build_prose_board()
    assert board["status"] == "pass"
    assert board["mode"] == "PROSE"
    assert board["provider_call_count"] == 0
