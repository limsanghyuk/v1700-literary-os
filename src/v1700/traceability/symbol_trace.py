from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.traceability.contracts import SymbolTraceEntry

LIVE_RUNTIME = "LIVE_RUNTIME"
TEST_GUARDED = "TEST_GUARDED"


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _entry(
    branchpoint_id: str,
    priority: str,
    concept: str,
    code_symbols: tuple[str, ...],
    evidence_files: tuple[str, ...],
    tests: tuple[str, ...],
    gates: tuple[str, ...],
    rationale: str,
    runtime_status: str = LIVE_RUNTIME,
) -> SymbolTraceEntry:
    return SymbolTraceEntry(
        branchpoint_id=branchpoint_id,
        priority=priority,
        concept=concept,
        runtime_status=runtime_status,
        code_symbols=code_symbols,
        evidence_files=evidence_files,
        tests=tests,
        gates=gates,
        rationale=rationale,
    )


def build_stage85_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE85_NODE2_REVEAL_BOUNDARY",
            "P0",
            "Node2 renders reader-facing surface only and cannot access raw reveal authority.",
            (
                "v1700.nodes.node2_prose_renderer.compiler.Node2ProseCompiler",
                "v1700.gates.node_projection_gate.run_node_projection_gate",
            ),
            (
                "src/v1700/nodes/node2_prose_renderer/compiler.py",
                "src/v1700/gates/node_projection_gate.py",
                "manifests/live_core_manifest.json",
            ),
            (
                "tests/test_stage84_v370_runtime_absorption.py",
                "tests/test_stage72_1_graph_nexus_release_gate.py",
            ),
            ("node_projection_gate", "stage84_release_gate", "stage85_release_gate"),
            "This protects the user's reveal-budget and authority-boundary design from prose-layer leakage.",
        ),
        _entry(
            "BP_STAGE85_PROVIDER_ZERO_LOCAL_FIRST",
            "P0",
            "Default execution remains local-first with provider_default_calls fixed at 0.",
            (
                "v1700.runtime.provider_boundary.ProviderBoundary",
                "v1700.runtime_absorption.v370_absorption.LLMNodeRouter",
            ),
            (
                "src/v1700/runtime/provider_boundary.py",
                "src/v1700/runtime_absorption/v370_absorption.py",
                "manifests/live_core_manifest.json",
            ),
            (
                "tests/test_stage84_v370_runtime_absorption.py",
            ),
            ("runtime_smoke", "stage84_release_gate", "stage85_release_gate"),
            "This preserves the cost-control rule while allowing optional adapters to exist.",
        ),
        _entry(
            "BP_STAGE85_GRAPHNEXUS_AUTHORITY",
            "P0",
            "GraphNexus remains the internal authority graph: CodeGraph, NarrativeGraph, and StageLineageGraph.",
            (
                "v1700.graph_nexus.registry.GraphNexusRegistry",
                "v1700.gates.graph_nexus_release_gate.run_graph_nexus_release_gate",
            ),
            (
                "src/v1700/graph_nexus/registry.py",
                "src/v1700/gates/graph_nexus_release_gate.py",
                "manifests/graph_nexus_manifest.json",
            ),
            (
                "tests/test_stage72_1_graph_nexus_three_graphs.py",
                "tests/test_stage72_1_graph_nexus_release_gate.py",
            ),
            ("graph_nexus_release_gate", "stage85_release_gate"),
            "GitNexus may enrich CodeGraph, but it must not replace the narrative and lineage authority layers.",
        ),
        _entry(
            "BP_STAGE85_BRANCHPOINT_SURVIVAL",
            "P0",
            "BranchpointLogicGraph keeps legacy literary logic alive across staged evolution.",
            (
                "v1700.lineage.stage83_1_consistency_audit.build_core_logic_survival_matrix_v3",
                "v1700.lineage.branchpoint_registry.build_branchpoint_registry",
            ),
            (
                "src/v1700/lineage/stage83_1_consistency_audit.py",
                "src/v1700/lineage/branchpoint_registry.py",
                "manifests/core_logic_survival_matrix_v3.json",
            ),
            (
                "tests/test_stage83_1_consistency_audit.py",
                "tests/test_gitnexus_branchpoint_bridge.py",
            ),
            ("stage83_1_release_gate", "stage85_release_gate"),
            "This directly answers the user's concern that past patches can become disconnected from the current core.",
        ),
        _entry(
            "BP_STAGE85_KOREAN_DRAMA_HIERARCHY",
            "P0",
            "Series, macro plot, episode, micro plot, sequence, and scene remain distinct runtime levels.",
            (
                "v1700.drama_composition.engine.KoreanDramaCompositionEngine",
                "v1700.gates.stage80_release_gate.run_stage80_release_gate",
            ),
            (
                "src/v1700/drama_composition/engine.py",
                "src/v1700/drama_composition/contracts.py",
                "src/v1700/gates/stage80_release_gate.py",
            ),
            ("tests/test_stage80_korean_drama_composition.py",),
            ("stage80_release_gate", "stage85_release_gate"),
            "This keeps the user's macro/micro story architecture from collapsing into generic plotting.",
        ),
        _entry(
            "BP_STAGE85_STAGE84_ABSORPTION_SAFE",
            "P0",
            "Claude V370 runtime muscle is absorbed under V1700 authority without copying the whole Claude architecture.",
            (
                "v1700.runtime_absorption.v370_absorption.run_stage84_absorption_smoke",
                "v1700.gates.stage84_release_gate.run_stage84_release_gate",
            ),
            (
                "src/v1700/runtime_absorption/v370_absorption.py",
                "src/v1700/gates/stage84_release_gate.py",
                "manifests/v370_feature_map_manifest.json",
            ),
            ("tests/test_stage84_v370_runtime_absorption.py",),
            ("stage84_release_gate", "stage85_release_gate"),
            "Stage85 must increase traceability without weakening the Stage84 surface-runtime absorption.",
        ),
        _entry(
            "BP_STAGE85_COMMERCIAL_EVIDENCE_PACK",
            "P0",
            "Commercial longform release evidence remains tied to three episodes, rendered scenes, and gates.",
            (
                "v1700.commercial_release.engine.CommercialLongformReleaseEngine",
                "v1700.gates.stage83_release_gate.run_stage83_release_gate",
            ),
            (
                "src/v1700/commercial_release/engine.py",
                "src/v1700/gates/stage83_release_gate.py",
                "sample_longform_project_01/commercial_release_manifest.json",
            ),
            ("tests/test_stage83_commercial_release_candidate.py",),
            ("stage83_release_gate", "stage85_release_gate"),
            "This prevents Stage85 refactoring from becoming detached from product-level evidence.",
        ),
        _entry(
            "BP_STAGE85_KOREAN_ANTI_LLM_FILTER",
            "P1",
            "KoreanAntiLLMFilter removes cliche and AI-like phrasing before reader-facing evaluation.",
            ("v1700.runtime_absorption.v370_absorption.KoreanAntiLLMFilter",),
            ("src/v1700/runtime_absorption/v370_absorption.py",),
            ("tests/test_stage84_v370_runtime_absorption.py",),
            ("stage84_release_gate", "stage85_release_gate"),
            "This is one of the user's most visible quality concerns: sentence surface and anti-LLM texture.",
        ),
        _entry(
            "BP_STAGE85_STYLE_DNA",
            "P1",
            "StyleDNA preserves writerly rhythm, genre register, and prose taste as an explicit surface module.",
            ("v1700.runtime_absorption.v370_absorption.StyleDNA",),
            ("src/v1700/runtime_absorption/v370_absorption.py",),
            ("tests/test_stage84_v370_runtime_absorption.py",),
            ("stage84_release_gate", "stage85_release_gate"),
            "This anchors the user's authorial-DNA concept to a runtime symbol and test.",
        ),
        _entry(
            "BP_STAGE85_CLOSED_LOOP_RENDERER",
            "P1",
            "ClosedLoopRenderer performs render, filter, score, validate, and trace collection as a local loop.",
            (
                "v1700.runtime_absorption.v370_absorption.ClosedLoopRenderer",
                "v1700.runtime_absorption.v370_absorption.LocalJudgmentValidator",
            ),
            ("src/v1700/runtime_absorption/v370_absorption.py",),
            ("tests/test_stage84_v370_runtime_absorption.py",),
            ("stage84_release_gate", "stage85_release_gate"),
            "This keeps surface prose improvement measurable without delegating default judgment to an external provider.",
        ),
        _entry(
            "BP_STAGE85_SELF_LEARNING_TRACE",
            "P1",
            "SelfLearningCollector records accepted local traces as the seed of future quality improvement.",
            ("v1700.runtime_absorption.v370_absorption.SelfLearningCollector",),
            (
                "src/v1700/runtime_absorption/v370_absorption.py",
                "release/current/stage84_trace_dataset/stage84_trace_dataset.jsonl",
            ),
            ("tests/test_stage84_v370_runtime_absorption.py",),
            ("stage84_release_gate", "stage85_release_gate"),
            "This keeps self-learning as local trace evidence, not uncontrolled model fine-tuning.",
        ),
        _entry(
            "BP_STAGE85_GITNEXUS_OPTIONAL_SIDECAR",
            "P1",
            "GitNexus provides high-resolution code impact analysis while remaining optional.",
            (
                "v1700.sidecars.gitnexus.probe.probe_gitnexus",
                "v1700.sidecars.gitnexus.adapter.GitNexusAdapter",
            ),
            (
                "src/v1700/sidecars/gitnexus/probe.py",
                "src/v1700/sidecars/gitnexus/adapter.py",
                "manifests/gitnexus_optional_sidecar_manifest.json",
            ),
            (
                "tests/test_stage72_1_gitnexus_optional_sidecar.py",
                "tests/test_gitnexus_branchpoint_bridge.py",
            ),
            ("graph_nexus_release_gate", "stage85_release_gate"),
            "This is the boundary that lets developers use GitNexus without forcing users to install it.",
        ),
    )


def build_stage86_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE86_SERIES_ARC_PLANNER",
            "P0",
            "SeriesArcPlanner turns a 16-episode season arc into a verified four-act graph.",
            ("v1700.arc_reveal_knowledge.series_arc_planner.SeriesArcPlanner",),
            (
                "src/v1700/arc_reveal_knowledge/series_arc_planner.py",
                "docs/stages/stage86.md",
                "manifests/stage86_v380_feature_map_manifest.json",
            ),
            ("tests/test_stage86_arc_reveal_knowledge.py",),
            ("stage86_release_gate",),
            "This absorbs V380 SeriesArcPlanner as live V1700 code instead of leaving it as a document-only concept.",
        ),
        _entry(
            "BP_STAGE86_CAUSAL_PLOT_GRAPH",
            "P0",
            "CausalPlotGraph stores causal, foreshadow, callback, and emotional escalation edges.",
            ("v1700.arc_reveal_knowledge.causal_plot_graph.CausalPlotGraph",),
            (
                "src/v1700/arc_reveal_knowledge/causal_plot_graph.py",
                "manifests/stage86_v380_feature_map_manifest.json",
            ),
            ("tests/test_stage86_arc_reveal_knowledge.py",),
            ("stage86_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This protects the user's go-like event placement idea with inspectable graph edges.",
        ),
        _entry(
            "BP_STAGE86_EPISODE_REVEAL_BUDGET",
            "P0",
            "EpisodeRevealBudget blocks premature direct reveal while permitting controlled foreshadowing.",
            ("v1700.arc_reveal_knowledge.reveal_budget.EpisodeRevealBudget",),
            (
                "src/v1700/arc_reveal_knowledge/reveal_budget.py",
                "src/v1700/arc_reveal_knowledge/prose_contract_bridge.py",
            ),
            ("tests/test_stage86_arc_reveal_knowledge.py",),
            ("stage86_release_gate",),
            "This keeps reveal budget from collapsing over multi-episode generation.",
        ),
        _entry(
            "BP_STAGE86_CHARACTER_KNOWLEDGE_BRIDGE",
            "P0",
            "CharacterKnowledgeProseBridge converts per-character knowledge status into prose-safe constraints.",
            ("v1700.arc_reveal_knowledge.character_knowledge_bridge.CharacterKnowledgeProseBridge",),
            (
                "src/v1700/arc_reveal_knowledge/character_knowledge_bridge.py",
                "src/v1700/arc_reveal_knowledge/knowledge_contracts.py",
            ),
            ("tests/test_stage86_arc_reveal_knowledge.py",),
            ("stage86_release_gate",),
            "This prevents characters from narrating facts they do not know or facts reserved for the reader.",
        ),
        _entry(
            "BP_STAGE86_PROSE_RENDER_CONTRACT_BRIDGE",
            "P0",
            "KnowledgeStatus and reveal policy are folded into a Node2 SurfaceOnlyContract before prose rendering.",
            (
                "v1700.arc_reveal_knowledge.prose_contract_bridge.build_prose_render_contract",
                "v1700.nodes.node2_prose_renderer.contract.SurfaceOnlyContract",
            ),
            (
                "src/v1700/arc_reveal_knowledge/prose_contract_bridge.py",
                "src/v1700/nodes/node2_prose_renderer/contract.py",
            ),
            ("tests/test_stage86_arc_reveal_knowledge.py",),
            ("stage86_release_gate", "node_projection_gate"),
            "This connects Arc-Reveal-Knowledge absorption to the existing Node2 no-structural-authority rule.",
        ),
        _entry(
            "BP_STAGE86_PROVIDER_ZERO_ABSORPTION",
            "P0",
            "V380 absorption remains local-first and does not introduce default external provider calls.",
            ("v1700.arc_reveal_knowledge.stage86_smoke.run_stage86_arc_reveal_knowledge_smoke",),
            (
                "src/v1700/arc_reveal_knowledge/stage86_smoke.py",
                "src/v1700/gates/stage86_release_gate.py",
            ),
            ("tests/test_stage86_arc_reveal_knowledge.py",),
            ("stage86_release_gate", "release_gate"),
            "This keeps the user's cost-control and provider-zero operating-system principle intact.",
        ),
    )


def build_stage87_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE87_EIGHT_EPISODE_SCALEUP",
            "P0",
            "Stage87 proves the minimum 8-episode scale-up evidence target with 80 scene-level contracts.",
            ("v1700.episode_scaleup.evidence.EpisodeScaleupEvidenceEngine",),
            (
                "src/v1700/episode_scaleup/evidence.py",
                "docs/stages/stage87.md",
                "release/current/stage87_episode_scaleup_evidence.json",
            ),
            ("tests/test_stage87_episode_scaleup.py",),
            ("stage87_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This is the first explicit evidence layer beyond the Stage83 three-episode pack.",
        ),
        _entry(
            "BP_STAGE87_SIXTEEN_EPISODE_SCALEUP",
            "P0",
            "Stage87 proves full 16-episode season evidence with 160 scene-level contracts.",
            ("v1700.episode_scaleup.evidence.run_stage87_episode_scaleup_smoke",),
            (
                "src/v1700/episode_scaleup/evidence.py",
                "release/current/stage87_episode_scaleup_evidence.json",
                "manifests/stage87_manifest.json",
            ),
            ("tests/test_stage87_episode_scaleup.py",),
            ("stage87_release_gate", "release_gate"),
            "This turns Stage86 Arc-Reveal-Knowledge contracts into scale evidence rather than a single smoke proof.",
        ),
        _entry(
            "BP_STAGE87_REVEAL_KNOWLEDGE_SCALE_LOCK",
            "P0",
            "EpisodeRevealBudget and CharacterKnowledgeProseBridge remain active across long episode maps.",
            (
                "v1700.arc_reveal_knowledge.reveal_budget.EpisodeRevealBudget",
                "v1700.arc_reveal_knowledge.character_knowledge_bridge.CharacterKnowledgeProseBridge",
            ),
            (
                "src/v1700/arc_reveal_knowledge/reveal_budget.py",
                "src/v1700/arc_reveal_knowledge/character_knowledge_bridge.py",
                "src/v1700/episode_scaleup/evidence.py",
            ),
            ("tests/test_stage87_episode_scaleup.py",),
            ("stage86_release_gate", "stage87_release_gate"),
            "This blocks the common regression where scale-up silently drops reveal and knowledge constraints.",
        ),
        _entry(
            "BP_STAGE87_STAGE86_LINEAGE_PRESERVATION",
            "P0",
            "Stage87 inherits Stage86 and Stage85 gates before accepting scale-up evidence.",
            (
                "v1700.gates.stage87_release_gate.run_stage87_release_gate",
                "v1700.gates.stage86_release_gate.run_stage86_release_gate",
            ),
            (
                "src/v1700/gates/stage87_release_gate.py",
                "src/v1700/gates/stage86_release_gate.py",
                "manifests/live_core_manifest.json",
            ),
            ("tests/test_stage87_episode_scaleup.py",),
            ("stage87_release_gate", "release_gate"),
            "This keeps scale-up from becoming a parallel fork outside the branchpoint-governed OS.",
        ),
    )



def build_stage88_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE88_AI_AGENT_EDITOR_PANEL",
            "P0",
            "Stage88 replaces external human editor benchmarking with a deterministic local AI-agent editor panel.",
            (
                "v1700.agent_benchmark.agents.build_default_agent_profiles",
                "v1700.agent_benchmark.harness.AgentBlindBenchmarkHarness",
            ),
            (
                "src/v1700/agent_benchmark/agents.py",
                "src/v1700/agent_benchmark/harness.py",
                "docs/stages/stage88.md",
            ),
            ("tests/test_stage88_agent_benchmark.py",),
            ("stage88_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This preserves the user's request to substitute external editors/readers with artificial intelligence agents while keeping the benchmark reproducible.",
        ),
        _entry(
            "BP_STAGE88_BLIND_SAMPLE_PROTOCOL",
            "P0",
            "Stage88 evaluates blinded Stage87 scale-up samples without exposing model/stage identity to reviewer agents.",
            (
                "v1700.agent_benchmark.contracts.BlindBenchmarkSample",
                "v1700.agent_benchmark.harness.AgentBlindBenchmarkHarness",
            ),
            (
                "src/v1700/agent_benchmark/contracts.py",
                "src/v1700/agent_benchmark/harness.py",
                "release/current/stage88_agent_benchmark_report.json",
            ),
            ("tests/test_stage88_agent_benchmark.py",),
            ("stage88_release_gate",),
            "This prevents agent scoring from becoming a self-confirming non-blind internal smoke test.",
        ),
        _entry(
            "BP_STAGE88_AGENT_CONSENSUS_GATE",
            "P0",
            "Stage88 release requires agent consensus, minimum agent average, and minimum sample average above the quality floor.",
            (
                "v1700.gates.stage88_release_gate.run_stage88_release_gate",
                "v1700.agent_benchmark.harness.run_stage88_agent_benchmark_smoke",
            ),
            (
                "src/v1700/gates/stage88_release_gate.py",
                "src/v1700/agent_benchmark/harness.py",
                "manifests/stage88_manifest.json",
            ),
            ("tests/test_stage88_agent_benchmark.py",),
            ("stage88_release_gate", "release_gate"),
            "This turns synthetic reviewer-agent output into an actual blocking release condition rather than a narrative report.",
        ),
        _entry(
            "BP_STAGE88_PROVIDER_ZERO_AGENT_BENCHMARK",
            "P0",
            "AI-agent benchmark runs locally and preserves provider_default_calls = 0 and Node2 raw reveal access = 0.",
            (
                "v1700.agent_benchmark.harness.run_stage88_agent_benchmark_smoke",
                "v1700.gates.stage88_release_gate.run_stage88_release_gate",
            ),
            (
                "src/v1700/agent_benchmark/harness.py",
                "src/v1700/gates/stage88_release_gate.py",
                "manifests/live_core_manifest.json",
            ),
            ("tests/test_stage88_agent_benchmark.py",),
            ("stage88_release_gate", "release_gate"),
            "This keeps AI-agent evaluation inside the V1700 local-first operating boundary.",
        ),
    )


def build_stage89_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE89_WRITER_STUDIO_UI_CONTRACT",
            "P0",
            "Stage89 exposes writer-facing Studio panels while preserving V1700 branchpoint governance.",
            (
                "v1700.writer_studio.workspace.WriterStudioWorkspaceBuilder",
                "v1700.writer_studio.workspace.build_writer_studio_workspace",
            ),
            (
                "src/v1700/writer_studio/workspace.py",
                "src/v1700/writer_studio/contracts.py",
                "docs/stages/stage89.md",
            ),
            ("tests/test_stage89_writer_studio_export.py",),
            ("stage89_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This turns the engine into a writer-facing Studio contract without bypassing branchpoint survival gates.",
        ),
        _entry(
            "BP_STAGE89_EXPORT_PIPELINE",
            "P0",
            "Stage89 exports Studio state to JSON, Markdown, HTML, platform pack, and scene CSV artifacts.",
            (
                "v1700.writer_studio.export_pipeline.WriterStudioExportPipeline",
                "v1700.writer_studio.export_pipeline.run_stage89_export_pipeline_smoke",
            ),
            (
                "src/v1700/writer_studio/export_pipeline.py",
                "release/current/stage89_export_bundle_report.json",
                "release/current/stage89_exports/stage89_writer_handoff.md",
            ),
            ("tests/test_stage89_writer_studio_export.py",),
            ("stage89_release_gate", "release_gate"),
            "This makes export a blocking, checksum-bearing pipeline rather than an ad hoc packaging step.",
        ),
        _entry(
            "BP_STAGE89_STATIC_STUDIO_PREVIEW",
            "P1",
            "Stage89 renders a static Writer Studio HTML preview for developer and writer handoff.",
            (
                "v1700.writer_studio.export_pipeline.WriterStudioExportPipeline",
            ),
            (
                "src/v1700/writer_studio/export_pipeline.py",
                "release/current/stage89_exports/stage89_writer_studio_preview.html",
            ),
            ("tests/test_stage89_writer_studio_export.py",),
            ("stage89_release_gate",),
            "This gives the project a lightweight UI artifact without introducing a web runtime dependency.",
        ),
        _entry(
            "BP_STAGE89_PROVIDER_ZERO_EXPORT",
            "P0",
            "Writer Studio and exports preserve provider_default_calls = 0 and Node2 raw reveal access = 0.",
            (
                "v1700.writer_studio.workspace.run_writer_studio_smoke",
                "v1700.gates.stage89_release_gate.run_stage89_release_gate",
            ),
            (
                "src/v1700/writer_studio/workspace.py",
                "src/v1700/gates/stage89_release_gate.py",
                "manifests/live_core_manifest.json",
            ),
            ("tests/test_stage89_writer_studio_export.py",),
            ("stage89_release_gate", "release_gate"),
            "This keeps the writer-facing layer inside the same local-first boundary as Stages 84-88.",
        ),
    )


def build_stage90_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE90_STUDIO_ROUNDTRIP_EDITING",
            "P0",
            "Stage90 applies writer-side Studio edit patches and proves they survive re-export.",
            (
                "v1700.writer_studio.roundtrip.StudioRoundTripEngine",
                "v1700.writer_studio.roundtrip.run_stage90_roundtrip_smoke",
            ),
            (
                "src/v1700/writer_studio/roundtrip.py",
                "release/current/stage90_roundtrip_fidelity_report.json",
                "docs/stages/stage90.md",
            ),
            ("tests/test_stage90_roundtrip_export_fidelity.py",),
            ("stage90_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This makes writer edits a tested round-trip contract rather than a one-way static export.",
        ),
        _entry(
            "BP_STAGE90_EXPORT_FIDELITY_HARDENING",
            "P0",
            "Stage90 compares before/after checksums across JSON, Markdown, HTML, platform pack, and scene CSV exports.",
            (
                "v1700.writer_studio.roundtrip.RoundTripFidelityReport",
                "v1700.gates.stage90_release_gate.run_stage90_release_gate",
            ),
            (
                "src/v1700/writer_studio/roundtrip.py",
                "src/v1700/gates/stage90_release_gate.py",
                "release/current/stage90_release_gate_report.json",
            ),
            ("tests/test_stage90_roundtrip_export_fidelity.py",),
            ("stage90_release_gate", "release_gate"),
            "This turns export fidelity into a blocking release criterion with deterministic evidence.",
        ),
        _entry(
            "BP_STAGE90_PROVIDER_ZERO_ROUNDTRIP",
            "P0",
            "Studio interaction and export fidelity hardening preserve provider_default_calls = 0 and Node2 raw reveal access = 0.",
            (
                "v1700.writer_studio.roundtrip.run_stage90_roundtrip_smoke",
                "v1700.gates.stage90_release_gate.run_stage90_release_gate",
            ),
            (
                "src/v1700/writer_studio/roundtrip.py",
                "src/v1700/gates/stage90_release_gate.py",
                "manifests/live_core_manifest.json",
            ),
            ("tests/test_stage90_roundtrip_export_fidelity.py",),
            ("stage90_release_gate", "release_gate"),
            "This protects the local-first and Node2 surface-only invariants while adding writer interaction semantics.",
        ),
    )


def build_stage91_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE91_STUDIO_PERSISTENCE",
            "P0",
            "Stage91 persists Writer Studio workspace snapshots with deterministic checksums and no database/provider dependency.",
            (
                "v1700.writer_studio.persistence.StudioPersistenceStore",
                "v1700.writer_studio.persistence.build_stage91_base_workspace",
            ),
            (
                "src/v1700/writer_studio/persistence.py",
                "release/current/stage91_studio_event_replay_report.json",
                "docs/stages/stage91.md",
            ),
            ("tests/test_stage91_studio_persistence.py",),
            ("stage91_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This turns Writer Studio state into an auditable persistence contract without introducing a server runtime.",
        ),
        _entry(
            "BP_STAGE91_REVIEW_QUEUE_STATE",
            "P0",
            "Stage91 routes Studio changes through a deterministic review queue with branchpoint-impact references.",
            (
                "v1700.writer_studio.review_queue.StudioReviewQueue",
                "v1700.writer_studio.review_queue.ReviewQueueItem",
            ),
            (
                "src/v1700/writer_studio/review_queue.py",
                "release/current/stage91_studio_event_replay_report.json",
            ),
            ("tests/test_stage91_studio_persistence.py",),
            ("stage91_release_gate",),
            "This protects the user's branchpoint-governed development principle when UI edits are introduced.",
        ),
        _entry(
            "BP_STAGE91_UI_EVENT_REPLAY",
            "P0",
            "Stage91 replays Studio UI events deterministically and verifies replay checksum stability.",
            (
                "v1700.writer_studio.event_replay.StudioEventReplayEngine",
                "v1700.writer_studio.event_replay.run_stage91_event_replay_smoke",
            ),
            (
                "src/v1700/writer_studio/event_replay.py",
                "src/v1700/gates/stage91_release_gate.py",
                "manifests/stage91_manifest.json",
            ),
            ("tests/test_stage91_studio_persistence.py",),
            ("stage91_release_gate", "release_gate"),
            "This gives the Studio an interaction audit trail before adding a live UI server.",
        ),
        _entry(
            "BP_STAGE91_PROVIDER_ZERO_INTERACTION_LAYER",
            "P0",
            "Stage91 interaction replay preserves provider_default_calls = 0 and Node2 raw reveal access = 0.",
            (
                "v1700.writer_studio.event_replay.run_stage91_event_replay_smoke",
                "v1700.gates.stage91_release_gate.run_stage91_release_gate",
            ),
            (
                "src/v1700/writer_studio/event_replay.py",
                "src/v1700/gates/stage91_release_gate.py",
                "manifests/live_core_manifest.json",
            ),
            ("tests/test_stage91_studio_persistence.py",),
            ("stage91_release_gate", "release_gate"),
            "This ensures Studio interactivity does not regress the local-first and Node2 surface-only invariants.",
        ),
    )


def build_stage92_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE92_LOCAL_MULTI_PROVIDER_ADAPTER",
            "P0",
            "Stage92 configures local developer adapters for Ollama, GPT, Claude, and Gemini without making any provider call during release gates.",
            (
                "v1700.provider_adapters.router.MultiProviderAdapterRouter",
                "v1700.provider_adapters.config.build_default_multi_provider_configs",
            ),
            (
                "src/v1700/provider_adapters/router.py",
                "src/v1700/provider_adapters/config.py",
                "docs/stages/stage92.md",
            ),
            ("tests/test_stage92_multi_provider_adapter.py",),
            ("stage92_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This satisfies the developer requirement that the personal local computer can configure Ollama, GPT, Claude, and Gemini as a multi-adapter runtime.",
        ),
        _entry(
            "BP_STAGE92_PROVIDER_ZERO_ADAPTER_GUARD",
            "P0",
            "Stage92 adapters remain dry-run by default and release gates never perform live provider calls.",
            (
                "v1700.provider_adapters.adapters.BaseProviderAdapter",
                "v1700.gates.stage92_release_gate.run_stage92_release_gate",
            ),
            (
                "src/v1700/provider_adapters/adapters.py",
                "src/v1700/gates/stage92_release_gate.py",
                "manifests/live_core_manifest.json",
            ),
            ("tests/test_stage92_multi_provider_adapter.py",),
            ("stage92_release_gate", "release_gate"),
            "This preserves provider_default_calls = 0 while still allowing explicit developer-side provider configuration.",
        ),
        _entry(
            "BP_STAGE92_STUDIO_ADAPTER_PANEL",
            "P0",
            "Stage92 exposes the four-provider adapter configuration through a Writer Studio panel without granting Node2 raw reveal access.",
            (
                "v1700.provider_adapters.studio_bridge.build_stage92_provider_panel",
                "v1700.provider_adapters.studio_bridge.build_stage92_studio_workspace",
            ),
            (
                "src/v1700/provider_adapters/studio_bridge.py",
                "manifests/stage92_manifest.json",
            ),
            ("tests/test_stage92_multi_provider_adapter.py",),
            ("stage92_release_gate",),
            "This connects the adapter runtime to the Stage89-91 Studio layer while keeping the interaction and review queue lineage alive.",
        ),
    )


def build_stage93_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE93_LIVE_PROVIDER_OPT_IN_SANDBOX",
            "P0",
            "Stage93 adds a live-provider opt-in sandbox boundary for Ollama, GPT, Claude, and Gemini while release probes perform zero live calls.",
            ("v1700.provider_adapters.live_sandbox.run_stage93_live_provider_sandbox",),
            ("src/v1700/provider_adapters/live_sandbox.py", "manifests/stage93_manifest.json"),
            ("tests/test_stage93_provider_sandbox.py",),
            ("stage93_release_gate", "release_gate"),
            "This lets the developer test local providers intentionally without weakening provider-zero release execution.",
        ),
        _entry(
            "BP_STAGE93_CREDENTIAL_REDACTION_AUDIT",
            "P0",
            "Stage93 audits provider credentials through environment presence and redacted fingerprints only.",
            ("v1700.provider_adapters.credential_audit.audit_provider_credentials",),
            ("src/v1700/provider_adapters/credential_audit.py", "manifests/stage93_branchpoint_trace_manifest.json"),
            ("tests/test_stage93_provider_sandbox.py",),
            ("stage93_release_gate",),
            "This prevents API keys from leaking into release evidence, Studio exports, or benchmark reports.",
        ),
        _entry(
            "BP_STAGE93_PROVIDER_RESPONSE_NORMALIZATION",
            "P0",
            "Stage93 normalizes Ollama, GPT, Claude, and Gemini responses into one V1700 response contract.",
            ("v1700.provider_adapters.normalization.normalize_provider_response", "v1700.provider_adapters.normalization.run_stage93_response_normalization_probe"),
            ("src/v1700/provider_adapters/normalization.py", "release/current/stage93_response_normalization_report.json"),
            ("tests/test_stage93_provider_sandbox.py",),
            ("stage93_release_gate",),
            "This avoids provider-specific response shapes leaking upward into Writer Studio, Node2, or future evaluation code.",
        ),
        _entry(
            "BP_STAGE93_PROVIDER_ZERO_LIVE_SANDBOX_GUARD",
            "P0",
            "Stage93 release gates validate the live sandbox without executing live provider calls.",
            ("v1700.gates.stage93_release_gate.run_stage93_release_gate",),
            ("src/v1700/gates/stage93_release_gate.py", "manifests/live_core_manifest.json"),
            ("tests/test_stage93_provider_sandbox.py",),
            ("stage93_release_gate", "release_gate"),
            "This preserves provider_default_calls = 0 and Node2 raw reveal access = 0 after multi-adapter hardening.",
        ),
    )


def build_stage94_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE94_PROVIDER_EVALUATION_HARNESS",
            "P0",
            "Stage94 evaluates Ollama, GPT, Claude, and Gemini through a common dry-run prompt suite.",
            (
                "v1700.provider_evaluation.harness.ProviderEvaluationHarness",
                "v1700.provider_evaluation.harness.run_stage94_provider_evaluation_smoke",
            ),
            (
                "src/v1700/provider_evaluation/harness.py",
                "docs/stages/stage94.md",
                "manifests/stage94_provider_evaluation_manifest.json",
            ),
            ("tests/test_stage94_provider_evaluation.py",),
            ("stage94_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This creates provider comparison evidence without letting any provider become the hidden runtime authority.",
        ),
        _entry(
            "BP_STAGE94_NORMALIZED_PROVIDER_SCORING",
            "P0",
            "Stage94 scores normalized provider responses across latency, cost, tokens, safety, literary quality, and branchpoint compliance.",
            (
                "v1700.provider_evaluation.scoring.score_normalized_response",
                "v1700.provider_evaluation.scoring.build_provider_profiles",
            ),
            (
                "src/v1700/provider_evaluation/scoring.py",
                "src/v1700/provider_evaluation/contracts.py",
                "manifests/stage94_provider_evaluation_manifest.json",
            ),
            ("tests/test_stage94_provider_evaluation.py",),
            ("stage94_release_gate",),
            "This gives the developer a comparable provider scorecard before Stage95 ensemble arbitration.",
        ),
        _entry(
            "BP_STAGE94_PROVIDER_ZERO_EVALUATION_GUARD",
            "P0",
            "Stage94 release evaluation performs zero live provider calls and keeps Node2 raw reveal access at zero.",
            ("v1700.gates.stage94_release_gate.run_stage94_release_gate",),
            (
                "src/v1700/gates/stage94_release_gate.py",
                "manifests/live_core_manifest.json",
                "manifests/stage94_manifest.json",
            ),
            ("tests/test_stage94_provider_evaluation.py",),
            ("stage94_release_gate", "release_gate"),
            "This preserves Stage93 provider sandbox safety while adding provider comparison.",
        ),
    )


def build_stage97_1_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE97_1_ADVERSARIAL_NEGATIVE_CORPUS",
            "P0",
            "Stage97.1 proves broken longform structures are blocked before Stage98 Studio workflow.",
            (
                "v1700.longform_adversarial.adversarial_case_builder.build_stage97_1_adversarial_cases",
                "v1700.longform_adversarial.adversarial_orchestrator.run_stage97_1_adversarial_validation",
            ),
            (
                "src/v1700/longform_adversarial/adversarial_case_builder.py",
                "src/v1700/longform_adversarial/adversarial_orchestrator.py",
                "docs/stages/stage97_1.md",
            ),
            ("tests/test_stage97_1_release_gate.py",),
            ("stage97_1_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This addresses the gap between normal proof success and failure-case blocking ability.",
        ),
        _entry(
            "BP_STAGE97_1_COEFFICIENT_AND_PRIVACY_BRIDGE",
            "P0",
            "Stage97.1 binds Stage96 coefficient memory and local-only manuscript ingest to adversarial validation.",
            (
                "v1700.longform_adversarial.coefficient_memory_adapter.load_stage96_coefficient_bridge",
                "v1700.longform_adversarial.manuscript_ingest_adapter.run_local_manuscript_ingest_privacy_probe",
            ),
            (
                "src/v1700/longform_adversarial/coefficient_memory_adapter.py",
                "src/v1700/longform_adversarial/manuscript_ingest_adapter.py",
                "release/current/stage96_coefficient_memory.json",
            ),
            (
                "tests/test_stage97_1_coefficient_memory_adapter.py",
                "tests/test_stage97_1_manuscript_ingest_privacy.py",
            ),
            ("stage97_1_release_gate",),
            "This ensures learned local coefficients influence validation while raw manuscript text never leaves local evidence boundaries.",
        ),
        _entry(
            "BP_STAGE97_1_PROVIDER_ZERO_NODE2_GUARD",
            "P0",
            "Stage97.1 release gates keep provider calls, raw manuscript provider leakage, and Node2 raw reveal access at zero.",
            ("v1700.gates.stage97_1_release_gate.run_stage97_1_release_gate",),
            (
                "src/v1700/gates/stage97_1_release_gate.py",
                "manifests/live_core_manifest.json",
                "manifests/stage97_1_manifest.json",
            ),
            ("tests/test_stage97_1_release_gate.py",),
            ("stage97_1_release_gate", "release_gate"),
            "This preserves the operating-system boundary while adding adversarial failure-case validation.",
        ),
    )


def build_stage100_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE100_RC_PREFLIGHT_LOCK",
            "P0",
            "Stage100 locks GitNexus-aware preflight, GraphNexus authority, and Branchpoint survival before RC declaration.",
            (
                "v1700.stage100.gitnexus_rc_preflight.run_stage100_rc_preflight",
                "v1700.gates.stage100_release_gate.run_stage100_release_gate",
            ),
            (
                "src/v1700/stage100/gitnexus_rc_preflight.py",
                "src/v1700/gates/stage100_release_gate.py",
                "manifests/stage100_rc_preflight_manifest.json",
            ),
            ("tests/test_stage100_rc_preflight.py",),
            ("stage100_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This enforces the mandatory pre-development guide before declaring V1700 Literary OS 1.0 RC.",
        ),
        _entry(
            "BP_STAGE100_DUAL_MODE_EVALUATION",
            "P0",
            "Stage100 separates prose-mode and scenario-mode evaluation authority.",
            (
                "v1700.stage100.dual_mode_evaluator.run_stage100_dual_mode_evaluation",
                "v1700.stage100.prose_evaluation.evaluate_prose_candidate",
                "v1700.stage100.scenario_evaluation.evaluate_scenario_candidate",
            ),
            (
                "src/v1700/stage100/dual_mode_evaluator.py",
                "src/v1700/stage100/prose_evaluation.py",
                "src/v1700/stage100/scenario_evaluation.py",
                "manifests/stage100_dual_mode_evaluation_manifest.json",
            ),
            ("tests/test_stage100_dual_mode_evaluation.py",),
            ("stage100_release_gate",),
            "This prevents prose quality and scenario production metrics from being conflated.",
        ),
        _entry(
            "BP_STAGE100_PROVIDER_CERTIFICATION",
            "P0",
            "Stage100 certifies provider contracts while preserving live provider call count zero in release mode.",
            ("v1700.stage100.provider_certification.run_stage100_provider_certification",),
            (
                "src/v1700/stage100/provider_certification.py",
                "manifests/stage100_provider_certification_manifest.json",
            ),
            ("tests/test_stage100_provider_certification.py",),
            ("stage100_release_gate",),
            "This confirms GPT, Claude, Gemini, Ollama, fixture, and mock providers remain governed by V1700 contracts.",
        ),
        _entry(
            "BP_STAGE100_V430_COMPARISON_ONLY",
            "P1",
            "Stage100 compares V430 strengths without merging V430 code into the RC.",
            ("v1700.stage100.v430_comparison_bridge.run_stage100_v430_comparison_bridge",),
            (
                "src/v1700/stage100/v430_comparison_bridge.py",
                "manifests/stage100_v430_comparison_manifest.json",
            ),
            ("tests/test_stage100_v430_comparison_bridge.py",),
            ("stage100_release_gate",),
            "This keeps the RC stable while preserving a clear Stage101 absorption path.",
        ),
        _entry(
            "BP_STAGE100_CLEAN_RC_PACKAGING",
            "P0",
            "Stage100 packaging excludes .git, .gitnexus, .venv, caches, pyc files, and non-POSIX paths.",
            ("tools.package_stage100_fixed.package",),
            (
                "tools/package_stage100_fixed.py",
                "manifests/stage100_manifest.json",
            ),
            ("tests/test_stage100_clean_packaging_policy.py",),
            ("stage100_release_gate",),
            "This gives developers a clean RC ZIP that can be handed off without local execution artifacts.",
        ),
    )


def build_stage101_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE101_CROSS_LINEAGE_PREFLIGHT",
            "P0",
            "Stage101 probes V430 source availability and blocks untraced cross-lineage merges before absorption.",
            (
                "v1700.stage101.orchestrator.run_stage101_0_cross_lineage_preflight",
                "v1700.cross_lineage.v430_candidate_probe.probe_v430_sources",
                "v1700.cross_lineage.absorption_decision.build_absorption_decisions",
            ),
            (
                "src/v1700/stage101/orchestrator.py",
                "src/v1700/cross_lineage/v430_candidate_probe.py",
                "src/v1700/cross_lineage/absorption_decision.py",
                "manifests/stage101_cross_lineage_absorption_manifest.json",
            ),
            ("tests/test_stage101_cross_lineage_preflight.py", "tests/test_stage101_absorption_matrix.py"),
            ("stage101_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This keeps V430 absorption contract-first and prevents untraced runtime import.",
        ),
        _entry(
            "BP_STAGE101_SCENARIO_ROOM_CONTRACT",
            "P0",
            "Stage101 adds a scenario-room contract layer without changing prose-mode authority.",
            (
                "v1700.stage101.orchestrator.run_stage101_1_scenario_room_contract",
                "v1700.scenario_room.scenario_room_orchestrator.run_scenario_room_integration",
            ),
            (
                "src/v1700/stage101/orchestrator.py",
                "src/v1700/scenario_room/contracts.py",
                "src/v1700/scenario_room/scenario_room_orchestrator.py",
                "manifests/stage101_scenario_room_manifest.json",
            ),
            ("tests/test_stage101_scenario_room_contract.py",),
            ("stage101_release_gate",),
            "This gives scenario mode a production-room surface while preserving V1700 contracts.",
        ),
        _entry(
            "BP_STAGE101_SCENARIO_CUE_INTEGRATION",
            "P0",
            "Stage101 integrates scene beats, investigation/action beats, dialogue/silence cues, and prop reveal cues.",
            (
                "v1700.scenario_room.scene_beat_board.build_scene_beat_board",
                "v1700.scenario_room.investigation_action.build_investigation_action_beats",
                "v1700.scenario_room.dialogue_silence_cue.build_dialogue_silence_cues",
                "v1700.scenario_room.prop_reveal.build_prop_reveal_cues",
            ),
            (
                "src/v1700/scenario_room/scene_beat_board.py",
                "src/v1700/scenario_room/investigation_action.py",
                "src/v1700/scenario_room/dialogue_silence_cue.py",
                "src/v1700/scenario_room/prop_reveal.py",
                "manifests/stage101_branchpoint_trace_manifest.json",
            ),
            (
                "tests/test_stage101_scene_beat_board.py",
                "tests/test_stage101_investigation_action.py",
                "tests/test_stage101_dialogue_silence_cue.py",
                "tests/test_stage101_prop_reveal.py",
            ),
            ("stage101_release_gate",),
            "This connects V430-style scenario movement to scene necessity, agency, Node2 boundaries, and reveal budgets.",
        ),
        _entry(
            "BP_STAGE101_DUAL_MODE_REGRESSION",
            "P1",
            "Stage101 proves scenario-room absorption does not conflate prose and scenario evaluation.",
            (
                "v1700.stage101.orchestrator.run_stage101_3_dual_mode_regression",
                "v1700.gates.stage101_release_gate.run_stage101_release_gate",
            ),
            (
                "src/v1700/stage101/orchestrator.py",
                "src/v1700/gates/stage101_release_gate.py",
                "manifests/stage101_manifest.json",
            ),
            ("tests/test_stage101_dual_mode_regression.py", "tests/test_stage101_release_gate.py"),
            ("stage101_release_gate", "release_gate"),
            "This keeps Stage100 dual-mode separation intact while promoting scenario-room contracts.",
        ),
    )


def build_stage102_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE102_REAL_WRITER_TRIAL",
            "P0",
            "Stage102 runs a deterministic writer workflow trial over the Stage101 engine.",
            (
                "v1700.stage102.writer_trial.run_stage102_writer_trial",
                "v1700.stage102.orchestrator.run_stage102_1_writer_trial",
            ),
            (
                "src/v1700/stage102/writer_trial.py",
                "src/v1700/stage102/orchestrator.py",
                "docs/stages/stage102.md",
                "manifests/stage102_writer_trial_manifest.json",
            ),
            ("tests/test_stage102_writer_trial.py",),
            ("stage102_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This moves the project from internal architecture proof toward writer-facing workflow evidence.",
        ),
        _entry(
            "BP_STAGE102_BLIND_BENCHMARK",
            "P0",
            "Stage102 compares direct provider-style baselines and V1700 modes through blinded local scorecards.",
            (
                "v1700.stage102.blind_benchmark.run_stage102_blind_benchmark",
                "v1700.stage102.candidate_builder.build_stage102_trial_candidates",
            ),
            (
                "src/v1700/stage102/blind_benchmark.py",
                "src/v1700/stage102/candidate_builder.py",
                "manifests/stage102_blind_benchmark_manifest.json",
            ),
            ("tests/test_stage102_blind_benchmark.py",),
            ("stage102_release_gate",),
            "This verifies V1700 against GPT/Claude/Gemini/Ollama-style baselines without live provider calls.",
        ),
        _entry(
            "BP_STAGE102_REVISION_EFFICIENCY",
            "P0",
            "Stage102 measures revision time reduction, issue reduction, plot consistency, payoff debt, and scene necessity.",
            (
                "v1700.stage102.revision_efficiency.run_stage102_revision_efficiency_audit",
                "v1700.stage102.orchestrator.run_stage102_3_revision_efficiency",
            ),
            (
                "src/v1700/stage102/revision_efficiency.py",
                "manifests/stage102_manifest.json",
            ),
            ("tests/test_stage102_revision_efficiency.py",),
            ("stage102_release_gate",),
            "This prevents a good blind score from hiding poor writer revision economics.",
        ),
        _entry(
            "BP_STAGE102_PROVIDER_ZERO_PRIVACY",
            "P0",
            "Stage102 release evidence preserves provider-zero execution, Node2 boundary, and raw manuscript privacy.",
            (
                "v1700.gates.stage102_release_gate.run_stage102_release_gate",
                "v1700.stage102.orchestrator.run_stage102",
            ),
            (
                "src/v1700/gates/stage102_release_gate.py",
                "src/v1700/stage102/orchestrator.py",
                "manifests/stage102_branchpoint_trace_manifest.json",
            ),
            ("tests/test_stage102_release_gate.py",),
            ("stage102_release_gate", "release_gate"),
            "This makes Stage102 a safe evidence layer rather than an uncontrolled external benchmark.",
        ),
    )


def build_stage103_trace_entries() -> tuple[SymbolTraceEntry, ...]:
    return (
        _entry(
            "BP_STAGE103_INSTALL_REPLAY",
            "P0",
            "Stage103 proves fresh-clone install and CI replay commands are explicit developer contracts.",
            (
                "v1700.stage103.install_replay.run_install_replay_probe",
                "v1700.stage103.ci_replay.run_ci_replay_contract",
                "v1700.stage103.orchestrator.run_stage103_1_install_replay",
            ),
            (
                "src/v1700/stage103/install_replay.py",
                "src/v1700/stage103/ci_replay.py",
                "docs/stages/stage103.md",
                "manifests/stage103_deployment_manifest.json",
            ),
            ("tests/test_stage103_install_replay.py",),
            ("stage103_release_gate", "symbol_to_branchpoint_trace_gate"),
            "This moves the project from internal validation toward reproducible developer setup.",
        ),
        _entry(
            "BP_STAGE103_RUNTIME_PROFILE_SEPARATION",
            "P0",
            "Stage103 separates dev, release, and sandbox runtime profiles with live providers disabled by default.",
            (
                "v1700.stage103.runtime_profiles.build_runtime_profiles",
                "v1700.stage103.runtime_profiles.validate_runtime_profiles",
            ),
            (
                "src/v1700/stage103/runtime_profiles.py",
                "manifests/stage103_runtime_profile_manifest.json",
            ),
            ("tests/test_stage103_runtime_profiles.py",),
            ("stage103_release_gate",),
            "This prevents production readiness work from weakening provider-zero release mode.",
        ),
        _entry(
            "BP_STAGE103_LOCAL_VAULT_BACKUP_RESTORE",
            "P0",
            "Stage103 adds local-only manuscript vault and feature-only project backup/restore probes.",
            (
                "v1700.stage103.manuscript_vault.run_local_manuscript_vault_probe",
                "v1700.stage103.backup_restore.run_backup_restore_probe",
            ),
            (
                "src/v1700/stage103/manuscript_vault.py",
                "src/v1700/stage103/backup_restore.py",
                "release/current/stage103_deployment_pack/local_manuscript_vault_report.json",
            ),
            ("tests/test_stage103_vault_backup_error_release.py",),
            ("stage103_release_gate",),
            "This keeps user manuscript privacy intact while adding operational backup discipline.",
        ),
        _entry(
            "BP_STAGE103_ERROR_RELEASE_NOTES",
            "P1",
            "Stage103 standardizes safe error reports and release notes for developer handoff.",
            (
                "v1700.stage103.error_reporting.build_safe_error_report",
                "v1700.stage103.release_notes.build_stage103_release_notes",
            ),
            (
                "src/v1700/stage103/error_reporting.py",
                "src/v1700/stage103/release_notes.py",
                "release/current/stage103_developer_handoff_report.md",
            ),
            ("tests/test_stage103_vault_backup_error_release.py",),
            ("stage103_release_gate",),
            "This is the handoff layer that makes deployment issues reportable without leaking prompts or credentials.",
        ),
        _entry(
            "BP_STAGE103_PROVIDER_ZERO_DEPLOYMENT",
            "P0",
            "Stage103 deployment readiness preserves provider-zero, Node2 boundary, raw manuscript privacy, and clean packaging.",
            (
                "v1700.gates.stage103_release_gate.run_stage103_release_gate",
                "v1700.stage103.orchestrator.run_stage103",
            ),
            (
                "src/v1700/gates/stage103_release_gate.py",
                "src/v1700/stage103/orchestrator.py",
                "manifests/stage103_branchpoint_trace_manifest.json",
            ),
            ("tests/test_stage103_release_gate.py", "tests/test_stage103_clean_packaging_policy.py"),
            ("stage103_release_gate", "release_gate"),
            "This ensures production hardening does not become an uncontrolled provider or packaging regression.",
        ),
    )


def _symbol_to_file(symbol: str) -> str:
    parts = symbol.split(".")
    if len(parts) < 3 or parts[0] != "v1700":
        return ""
    module_parts = parts[:-1]
    return "src/" + "/".join(module_parts) + ".py"


def _missing_existing_paths(root: Path, paths: tuple[str, ...]) -> list[str]:
    missing: list[str] = []
    for rel in paths:
        if rel.endswith("_gate") or rel == "runtime_smoke":
            continue
        if not (root / rel).exists():
            missing.append(rel)
    return missing


def _entry_status(root: Path, entry: SymbolTraceEntry) -> dict[str, Any]:
    symbol_files = tuple(filter(None, (_symbol_to_file(symbol) for symbol in entry.code_symbols)))
    missing = sorted(
        set(
            _missing_existing_paths(root, entry.evidence_files)
            + _missing_existing_paths(root, entry.tests)
            + _missing_existing_paths(root, symbol_files)
        )
    )
    return {
        "branchpoint_id": entry.branchpoint_id,
        "priority": entry.priority,
        "covered": not missing,
        "missing_paths": missing,
        "symbol_files": list(symbol_files),
    }


def _coverage(statuses: list[dict[str, Any]], priority: str) -> dict[str, Any]:
    subset = [item for item in statuses if item["priority"] == priority]
    covered = [item for item in subset if item["covered"]]
    total = len(subset)
    return {
        "priority": priority,
        "total": total,
        "covered": len(covered),
        "coverage": round(len(covered) / total, 3) if total else 1.0,
        "missing_branchpoints": [item["branchpoint_id"] for item in subset if not item["covered"]],
    }


def build_symbol_to_branchpoint_trace_manifest(root: Path | None = None) -> dict[str, Any]:
    root = root or _project_root()
    entries = build_stage85_trace_entries() + build_stage86_trace_entries() + build_stage87_trace_entries() + build_stage88_trace_entries() + build_stage89_trace_entries() + build_stage90_trace_entries() + build_stage91_trace_entries() + build_stage92_trace_entries() + build_stage93_trace_entries() + build_stage94_trace_entries() + build_stage97_1_trace_entries() + build_stage100_trace_entries() + build_stage101_trace_entries() + build_stage102_trace_entries() + build_stage103_trace_entries()
    statuses = [_entry_status(root, entry) for entry in entries]
    p0 = _coverage(statuses, "P0")
    p1 = _coverage(statuses, "P1")
    issues: list[str] = []
    if p0["coverage"] < 1.0:
        issues.append("p0_branchpoint_trace_coverage_below_100_percent")
    if p1["coverage"] < 0.8:
        issues.append("p1_branchpoint_trace_coverage_below_80_percent")
    return {
        "stage": "97.1",
        "status": "pass" if not issues else "blocked",
        "title": "Symbol-to-Branchpoint Traceability with Stage97.1 Adversarial Validation Evidence",
        "principle": "Connect literary logic to concrete code symbols, tests, and release gates without making GitNexus mandatory at runtime.",
        "issues": issues,
        "entry_count": len(entries),
        "coverage": {
            "P0": p0,
            "P1": p1,
            "overall": {
                "total": len(statuses),
                "covered": len([item for item in statuses if item["covered"]]),
                "coverage": round(len([item for item in statuses if item["covered"]]) / max(len(statuses), 1), 3),
            },
        },
        "entry_statuses": statuses,
        "entries": [entry.to_dict() for entry in entries],
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }


def render_trace_matrix_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Stage97.1 Symbol-to-Branchpoint Trace Matrix",
        "",
        "This matrix shows which literary logic survives as live code, tests, and release gates.",
        "",
        "| Priority | Branchpoint | Runtime status | Code symbols | Tests | Gates |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in manifest["entries"]:
        lines.append(
            "| {priority} | {branchpoint} | {status} | {symbols} | {tests} | {gates} |".format(
                priority=entry["priority"],
                branchpoint=entry["branchpoint_id"],
                status=entry["runtime_status"],
                symbols="<br>".join(entry["code_symbols"]),
                tests="<br>".join(entry["tests"]),
                gates="<br>".join(entry["gates"]),
            )
        )
    lines.extend(
        [
            "",
            "## Coverage",
            "",
            f"- P0 coverage: {manifest['coverage']['P0']['coverage']}",
            f"- P1 coverage: {manifest['coverage']['P1']['coverage']}",
            f"- Overall coverage: {manifest['coverage']['overall']['coverage']}",
            "",
        ]
    )
    return "\n".join(lines)


def export_symbol_to_branchpoint_trace_manifest(root: Path | None = None) -> dict[str, str]:
    root = root or _project_root()
    manifest = build_symbol_to_branchpoint_trace_manifest(root)
    manifest_dir = root / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / "symbol_to_branchpoint_trace_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    stage_dir = root / "docs" / "stages"
    stage_dir.mkdir(parents=True, exist_ok=True)
    matrix_path = stage_dir / "stage97_1_symbol_to_branchpoint_matrix.md"
    matrix_path.write_text(render_trace_matrix_markdown(manifest) + "\n", encoding="utf-8")
    return {
        "symbol_to_branchpoint_trace_manifest": str(manifest_path.relative_to(root)),
        "stage97_1_symbol_to_branchpoint_matrix": str(matrix_path.relative_to(root)),
    }
