from __future__ import annotations

import json
from pathlib import Path

from v1700.corpus_absorption import ABSORPTION_MODE, run_local_corpus_absorption


def test_local_corpus_absorption_builds_safe_metadata_only_outputs(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    corpus_root = tmp_path / "corpus_ko"
    repo_root.mkdir()
    corpus_root.mkdir()
    (corpus_root / "features").mkdir()
    (corpus_root / "scenes").mkdir()
    (corpus_root / "chunks").mkdir()
    (corpus_root / "txt").mkdir()
    (corpus_root / "emb_cache").mkdir()
    (corpus_root / "chroma").mkdir()

    (corpus_root / "manifest.json").write_text(
        json.dumps({"counts": {"source_files": 1, "converted_works": 1}, "tri_store": {"feature_table": "scene_features.db"}}),
        encoding="utf-8",
    )
    (corpus_root / "sources.json").write_text(
        json.dumps([{"id": "sample_work", "media": "drama", "src": "sample_work.hwp", "type": "HWP5"}], ensure_ascii=False),
        encoding="utf-8",
    )
    (corpus_root / "qc_report.json").write_text(
        json.dumps([{"work": "sample_work", "flags": "OK"}], ensure_ascii=False),
        encoding="utf-8",
    )
    (corpus_root / "nkg_summary.json").write_text(
        json.dumps({"works": 1, "characters": 4, "edges_next": 3}, ensure_ascii=False),
        encoding="utf-8",
    )
    (corpus_root / "parse_stats.json").write_text(json.dumps({"sample_work": []}, ensure_ascii=False), encoding="utf-8")
    (corpus_root / "scene_features.db").write_bytes(b"")
    (corpus_root / "chroma" / "chroma.sqlite3").write_bytes(b"SQLite format 3\x00" + (b"\x00" * 200))
    (corpus_root / "emb_cache" / "embeddings-001.npy").write_bytes(b"1234")
    (corpus_root / "txt" / "sample_work.txt").write_text("RAW_TEXT_SHOULD_NOT_ESCAPE", encoding="utf-8")
    (corpus_root / "features" / "sample_work.json").write_text(
        json.dumps(
            [
                {
                    "scene_no": 1,
                    "conflict_intensity": 0.8,
                    "scene_energy_ratio": 1.2,
                    "motif_residue_score": 0.3,
                    "curiosity_gradient": 0.5,
                    "dialogue_ratio": 0.7,
                    "n_chars": 3,
                    "n_dialogue": 12,
                    "n_lines": 20,
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (corpus_root / "scenes" / "sample_work.jsonl").write_text(
        json.dumps(
            {
                "work_id": "sample_work",
                "scene_no": 1,
                "method": "slug",
                "heading": "INT ROOM",
                "text": "RAW_TEXT_SHOULD_NOT_ESCAPE",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (corpus_root / "chunks" / "sample_work.jsonl").write_text(
        json.dumps({"work_id": "sample_work", "scene_no": 1, "text": "RAW_TEXT_SHOULD_NOT_ESCAPE"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    result = run_local_corpus_absorption(repo_root=repo_root, corpus_root=corpus_root, output_dir=repo_root / "release/current/test_pack")

    assert result["status"] == "pass"
    assert result["mode"] == ABSORPTION_MODE
    assert result["verbatim_text_exported"] is False
    assert result["raw_vectors_exported"] is False
    assert result["counters"]["work_count"] == 1
    assert result["counters"]["rag_ready_count"] == 1
    assert result["counters"]["learning_ready_count"] == 1

    work = result["parts"]["canonical_work_registry"][0]
    assert work["work_id"] == "sample_work"
    assert work["scene_count"] == 1
    assert work["chunk_count"] == 1
    assert work["feature_scene_count"] == 1
    assert work["parse_methods"] == {"slug": 1}

    rag = result["parts"]["rag_index_registry"][0]
    assert rag["scene_index_ready"] is True
    assert rag["chunk_index_ready"] is True

    learning = result["parts"]["learning_signal_registry"][0]
    assert learning["learning_ready"] is True
    assert learning["mean_conflict_intensity"] == 0.8

    report_text = (repo_root / "release/current/test_pack/corpus_absorption_report.json").read_text(encoding="utf-8")
    assert "RAW_TEXT_SHOULD_NOT_ESCAPE" not in report_text

    fixture_summary = (repo_root / "fixtures/research/drama_script_metadata_inventory_summary.json").read_text(encoding="utf-8")
    assert "RAW_TEXT_SHOULD_NOT_ESCAPE" not in fixture_summary
