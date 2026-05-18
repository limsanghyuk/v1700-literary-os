from v1700.nodes.node2_prose_renderer.marker_stripper import InternalMarkerStripper
from v1700.nodes.node2_prose_renderer.emotion_renderer import EmotionToBehaviorRenderer

def test_marker_stripper_removes_internal_markers():
    text = InternalMarkerStripper().strip("[LOCKED_REVEAL_01] candidate not canon 장면")
    assert "LOCKED_REVEAL" not in text
    assert "candidate" not in text
    assert "not canon" not in text

def test_emotion_renderer_removes_direct_labels():
    renderer = EmotionToBehaviorRenderer()
    text = renderer.rewrite("그는 슬펐다")
    assert "슬펐다" not in text
    assert renderer.direct_emotion_count(text) == 0
