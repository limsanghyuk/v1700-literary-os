from v1700.creative_arbitration.candidate_lanes import build_candidate_lanes
from v1700.creative_arbitration.normalization import build_response_normalization_matrix


def test_stage105_response_normalization_schema():
    candidates = build_candidate_lanes()["candidates"]
    report = build_response_normalization_matrix(candidates)
    assert report["status"] == "pass"
    assert report["response_schema"] == "CreativeCandidate/v1"
    assert report["normalized_count"] == len(candidates)
