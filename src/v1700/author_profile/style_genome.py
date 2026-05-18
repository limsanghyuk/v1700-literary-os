from __future__ import annotations
from statistics import mean
from .contracts import StyleFeatureVector, StyleGenome
from .feature_extractor import extract_feature_only_style_features


def build_style_genome(author_profile_id: str = "author_profile_stage106") -> dict:
    features_payload = extract_feature_only_style_features(author_profile_id)
    vectors = [StyleFeatureVector(**payload) for payload in features_payload["feature_vectors"]]
    genome = StyleGenome(
        genome_id="style_genome_stage106_feature_only",
        author_profile_id=author_profile_id,
        feature_vectors=tuple(vectors),
        authorial_rhythm=round(mean(v.sentence_rhythm for v in vectors), 3),
        sensory_preference=round(mean(v.sensory_density for v in vectors), 3),
        dialogue_preference=round(mean(v.dialogue_ratio for v in vectors), 3),
        introspection_preference=round(mean(v.introspection_ratio for v in vectors), 3),
        motion_preference=round(mean(v.scene_motion_ratio for v in vectors), 3),
        privacy_mode="FEATURE_ONLY",
        raw_manuscript_retained=False,
        provider_export_allowed=False,
    )
    payload = genome.to_dict()
    payload.update({
        "stage": "106.2",
        "title": "Adaptive Author Profile & Style Genome",
        "status": "pass",
        "feature_only": True,
        "raw_manuscript_provider_leakage": 0,
        "provider_call_count": 0,
        "genome_contract": "style_vector_statistics_only_no_raw_text",
    })
    return payload
