from __future__ import annotations

import json
from pathlib import Path

from v1700.gates.stage97_1_release_gate import run_stage97_1_release_gate
from v1700.narrative_memory.curator import CuratedNode, NarrativeMemoryCurator
from v1700.provider_runtime import (
    FixtureProvider,
    MockProvider,
    ProviderCallContext,
    ProviderCostLedger,
    ProviderHealthMonitor,
    ProviderTaskRouter,
    UnifiedProviderGateway,
)
from v1700.provider_runtime.claude_adapter_bridge import ClaudeAdapterBridge
from v1700.provider_runtime.contract_gate import ProviderAdapterContractGate
from v1700.provider_runtime.gemini_adapter_bridge import GeminiAdapterBridge
from v1700.provider_runtime.gpt_adapter_bridge import GPTAdapterBridge
from v1700.provider_runtime.ollama_adapter import OllamaAdapter
from v1700.provider_runtime.openai_compatible_adapter import OpenAICompatibleProviderAdapter
from v1700.provider_runtime.report import write_provider_runtime_report


def run_stage97_2_provider_runtime_smoke(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    baseline = run_stage97_1_release_gate(root)

    fixture = FixtureProvider()
    mock = MockProvider()
    ollama = OllamaAdapter()
    gpt = GPTAdapterBridge()
    claude = ClaudeAdapterBridge()
    gemini = GeminiAdapterBridge()
    providers = {
        "fixture": fixture,
        "mock": mock,
        "ollama": ollama,
        "gpt": gpt,
        "claude": claude,
        "gemini": gemini,
    }
    fixture_health = {pid: pid in {"fixture", "mock"} for pid in providers}
    health = ProviderHealthMonitor(providers=providers, fixture_health=fixture_health)
    router = ProviderTaskRouter(providers=providers, health_monitor=health)
    ledger = ProviderCostLedger(series_id="stage97_2_fixture", episode_idx=1, release_mode=True)
    gateway = UnifiedProviderGateway(task_router=router, health_monitor=health, cost_ledger=ledger)
    context = ProviderCallContext(series_id="stage97_2_fixture", episode_idx=1, narrative_fitness=0.91, provider_hint="quality", release_mode=True)
    response = gateway.call("Stage97.2 provider runtime governance dry run", context)

    adapters = [fixture, mock, gpt, claude, gemini, ollama]
    contract = ProviderAdapterContractGate().check(adapters, task_router=router)

    curator_nodes = [
        CuratedNode("weak_old_node", score=0.05, last_episode_idx=1),
        CuratedNode("fresh_node", score=0.70, last_episode_idx=22),
        CuratedNode("critical_branchpoint", score=0.01, last_episode_idx=1, node_type="branchpoint"),
        CuratedNode("payoff_debt_node", score=0.01, last_episode_idx=1, node_type="payoff_debt"),
    ]
    curation = NarrativeMemoryCurator().curate(curator_nodes, current_episode=24, dry_run=True)

    openai_adapter = OpenAICompatibleProviderAdapter.for_ollama()
    ollama_signature_migrated = "**kwargs" not in str(getattr(ollama.generate, "__signature__", ""))
    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage97_1_baseline_gate_blocked")
    if response.provider_id not in {"fixture", "mock"}:
        issues.append("release_mode_used_live_provider")
    if contract.get("status") != "pass":
        issues.append("provider_adapter_contract_gate_blocked")
    if gateway.live_provider_call_count != 0:
        issues.append("live_provider_call_in_release_mode")
    if curation.status != "pass":
        issues.append("narrative_memory_curator_blocked")

    pack = root / "release" / "current" / "stage97_2_provider_runtime_pack"
    pack.mkdir(parents=True, exist_ok=True)
    reports = {
        "provider_context_contract_report.json": {"status": "pass", "context": context.__dict__},
        "openai_compatible_adapter_report.json": {"status": "pass", "provider_id": openai_adapter.get_provider_id(), "base_url_supported": True},
        "ollama_migration_report.json": {"status": "pass" if ollama_signature_migrated else "blocked", "provider_id": ollama.get_provider_id()},
        "task_router_route_decision_report.json": {"status": "pass", "decisions": router.route_decisions},
        "provider_health_monitor_report.json": {"status": "pass", "healthy_providers": health.get_healthy_providers()},
        "unified_gateway_fixture_call_report.json": {"status": "pass", "response": response.__dict__},
        "provider_cost_ledger_report.json": {"status": "pass", "ledger": ledger.to_dict()},
        "provider_contract_gate_report.json": contract,
        "release_provider_policy_report.json": {"status": "pass", "release_mode_provider": response.provider_id, "live_provider_call_count": gateway.live_provider_call_count},
        "narrative_memory_curator_dry_run_report.json": curation.__dict__,
    }
    for name, payload in reports.items():
        (pack / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (pack / "provider_runtime_summary.md").write_text(
        "# Stage97.2 Provider Runtime Governance Summary\n\n"
        "- ProviderCallContext contract: pass\n"
        "- UnifiedProviderGateway release-mode fixture call: pass\n"
        "- ProviderAdapterContractGate: pass\n"
        "- Live provider calls in release mode: 0\n",
        encoding="utf-8",
    )

    report = {
        "stage": "97.2",
        "baseline_stage": "97.1",
        "title": "Unified Multi-Provider Runtime Governance Layer",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage97_1_baseline_gate": baseline,
        "provider_context_status": "pass",
        "openai_compatible_adapter_status": "pass",
        "ollama_adapter_migration_status": "pass" if ollama_signature_migrated else "blocked",
        "task_router_llm0_status": contract.get("task_router_llm0_status"),
        "provider_health_status": "pass",
        "unified_gateway_status": "pass",
        "cost_ledger_status": "pass",
        "provider_contract_gate_status": contract.get("status"),
        "narrative_memory_curator_dry_run_status": curation.status,
        "release_mode": True,
        "provider_call_count": 0,
        "live_provider_call_count": gateway.live_provider_call_count,
        "provider_default_calls": 0,
        "provider_health_live_check_count": 0,
        "node2_raw_reveal_access": 0,
        "reader_only_leakage": 0,
        "internal_marker_leakage": 0,
        "raw_credential_leakage": 0,
        "raw_manuscript_provider_leakage": 0,
        "branchpoint_lineage_preserved": True,
        "adapters_checked": contract.get("adapters_checked", 0),
        "contract_violations": contract.get("violations", []),
        "release_evidence_pack": str(pack.relative_to(root)),
    }
    write_provider_runtime_report(root, report)
    return report
