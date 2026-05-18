from __future__ import annotations
from v1700.v485_bridge.contracts import V485AbsorptionCandidate

def build_absorption_candidate_matrix() -> dict:
    candidates = [
        V485AbsorptionCandidate("drama_episode_generator", "DramaEpisodeGenerator", "V485", "v1700.v485_bridge.drama_episode_bridge", "WRAP_ONLY", "MEDIUM", True, True, True, "Absorb execution flow, not metadata."),
        V485AbsorptionCandidate("scene_generation_pipeline", "SceneGenerationPipeline", "V485", "v1700.v485_bridge.scene_pipeline_bridge", "WRAP_ONLY", "MEDIUM", True, True, True, "Connect to ReviewQueue and WriterDecision."),
        V485AbsorptionCandidate("anthropic_adapter_pattern", "AnthropicAdapter", "V485", "v1700.provider_live_sandbox.anthropic_live_adapter", "WRAP_ONLY", "HIGH", True, True, True, "Live calls remain sandbox-only."),
        V485AbsorptionCandidate("ollama_adapter_pattern", "OllamaAdapter", "V485", "v1700.provider_live_sandbox.ollama_live_adapter", "WRAP_ONLY", "MEDIUM", True, True, True, "Local endpoint through sandbox guard."),
        V485AbsorptionCandidate("generate_5episodes_cli_flow", "generate_5episodes.py", "V485", "tools/run_stage111_sample_episode_bridge.py", "ACCEPT", "LOW", False, True, True, "Accept as V1700 sample runner pattern only."),
        V485AbsorptionCandidate("v485_release_gate", "tools/run_release_gate.py", "V480/V485 drift", "none", "REJECT", "BLOCK", False, False, False, "Do not replace V1700 gate."),
        V485AbsorptionCandidate("v485_metadata", "README/MANIFEST/live_core_manifest", "drift", "none", "REJECT", "BLOCK", False, False, False, "Do not overwrite V1700 metadata."),
        V485AbsorptionCandidate("v485_raw_live_call_path", "direct adapter generate", "V485", "none", "BLOCK", "BLOCK", True, True, True, "Release path direct live call is forbidden."),
        V485AbsorptionCandidate("v485_otel_layer", "OpenTelemetry", "V485", "future observability", "DEFER", "MEDIUM", False, False, True, "Optional dependency layer deferred."),
        V485AbsorptionCandidate("v485_fastapi_studio_api", "Studio API", "V485", "future studio API", "DEFER", "MEDIUM", False, False, True, "Potential Stage112+ candidate."),
    ]
    issues = [c.candidate_id for c in candidates if c.absorption_status == "BLOCK" and c.risk_level != "BLOCK"]
    return {
        "stage": "111.5",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "candidates": [c.to_dict() for c in candidates],
        "direct_merge_allowed": False,
        "wrap_only_required": True,
    }
