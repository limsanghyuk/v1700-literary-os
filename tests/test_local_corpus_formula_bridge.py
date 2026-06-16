from __future__ import annotations

from pathlib import Path

from v1700.corpus_formula_bridge import FORMULA_BRIDGE_MODE, run_local_corpus_formula_bridge


def test_local_corpus_formula_bridge_emits_advisory_signals(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    pack = repo_root / "release/current/corpus_ko_absorption_pack"
    pack.mkdir(parents=True, exist_ok=True)
    repo_root.mkdir(exist_ok=True)

    absorption_report = {
        "corpus_id": "corpus_ko",
        "status": "pass",
        "counters": {"work_count": 1, "rag_ready_count": 1, "learning_ready_count": 1},
        "parts": {
            "learning_signal_registry": [
                {
                    "work_id": "sample_work",
                    "feature_scene_count": 12,
                    "mean_conflict_intensity": 0.8,
                    "mean_scene_energy_ratio": 2.0,
                    "mean_motif_residue_score": 0.4,
                    "mean_curiosity_gradient": 0.6,
                    "mean_dialogue_ratio": 0.5,
                    "signal_keys": [
                        "conflict_intensity",
                        "scene_energy_ratio",
                        "motif_residue_score",
                        "curiosity_gradient",
                        "dialogue_ratio",
                    ],
                    "learning_ready": True,
                }
            ],
            "rag_index_registry": [
                {
                    "work_id": "sample_work",
                    "scene_count": 10,
                    "chunk_count": 20,
                    "scene_index_ready": True,
                    "chunk_index_ready": True,
                }
            ],
        },
    }

    result = run_local_corpus_formula_bridge(repo_root=repo_root, absorption_report=absorption_report)

    assert result["status"] == "pass"
    assert result["mode"] == FORMULA_BRIDGE_MODE
    assert result["counters"]["formula_signal_count"] == 3
    assert result["counters"]["tensor_count"] == 1
    assert result["verbatim_text_exported"] is False
    assert result["raw_vectors_exported"] is False

    tensor = result["parts"]["narrative_state_tensor_registry"][0]
    assert tensor["case_id"] == "sample_work"
    assert tensor["classification"] == "metadata_only_corpus_tensor"

    groups = {signal["formula_group"] for signal in result["parts"]["formula_signal_registry"]}
    assert "Narrative State Tensor" in groups
    assert "Emotional Momentum" in groups
    assert "RAG/BM25/RRF retrieval fusion" in groups
