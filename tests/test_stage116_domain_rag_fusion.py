from pathlib import Path

from v1700.gates.stage116_release_gate import run_stage116_release_gate
from v1700.nie.rag.drama_lexicon import DramaLexicon
from v1700.nie.rag.query_intent_classifier import QueryIntentClassifier
from v1700.nie.rag.rag_fusion_report import build_stage116_rag_fusion_report
from v1700.stage116.orchestrator import run_stage116


def test_query_intent_classifier_uses_domain_weights_without_llm() -> None:
    classifier = QueryIntentClassifier(DramaLexicon())
    character = classifier.classify("민준 수진 대화")
    emotional = classifier.classify("배신감 절정 장면")
    plot = classifier.classify("3화 클라이맥스 사건")
    assert character.intent == "CHARACTER"
    assert character.bm25_weight == 0.70 and character.dense_weight == 0.30 and character.k == 40
    assert emotional.intent == "EMOTIONAL"
    assert emotional.bm25_weight == 0.30 and emotional.dense_weight == 0.70 and emotional.k == 60
    assert plot.intent == "PLOT_EVENT"
    assert plot.bm25_weight == 0.50 and plot.dense_weight == 0.50 and plot.k == 50
    assert classifier.llm_call_count == 0


def test_drama_lexicon_boosts_character_episode_and_drama_terms() -> None:
    lexicon = DramaLexicon()
    assert lexicon.boost_weight("민준") == 1.5
    assert lexicon.boost_weight("3화") == 1.3
    assert lexicon.boost_weight("클라이맥스") == 1.2
    assert lexicon.boost_weight("무관한단어") == 1.0


def test_stage116_report_and_gate_pass() -> None:
    report = build_stage116_rag_fusion_report()
    assert report["status"] == "pass"
    intents = {row["intent"] for row in report["query_intent_classifier"]["classified_queries"]}
    assert intents == {"CHARACTER", "EMOTIONAL", "PLOT_EVENT"}
    root = Path(__file__).resolve().parents[1]
    stage = run_stage116(root)
    assert stage["status"] == "pass"
    gate = run_stage116_release_gate(root)
    assert gate["status"] == "pass"
    assert gate["checks"]["adaptive_bm25_dense_policy_pass"]["status"] == "pass"
    assert gate["checks"]["drama_lexicon_boost_pass"]["status"] == "pass"
