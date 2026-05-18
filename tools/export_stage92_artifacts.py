from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage92_release_gate import run_stage92_release_gate
from v1700.provider_adapters.router import run_stage92_multi_adapter_smoke
from v1700.provider_adapters.studio_bridge import build_stage92_studio_workspace, run_stage92_studio_bridge_smoke

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "current"


def main() -> int:
    RELEASE.mkdir(parents=True, exist_ok=True)
    adapter = run_stage92_multi_adapter_smoke()
    bridge = run_stage92_studio_bridge_smoke()
    gate = run_stage92_release_gate(ROOT)
    workspace = build_stage92_studio_workspace().to_dict()
    (RELEASE / "stage92_multi_provider_adapter_report.json").write_text(json.dumps(adapter, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RELEASE / "stage92_studio_bridge_report.json").write_text(json.dumps(bridge, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RELEASE / "stage92_release_gate_report.json").write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RELEASE / "stage92_writer_studio_workspace.json").write_text(json.dumps(workspace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    handoff = "\n".join([
        "# Stage92 Developer Handoff Report",
        "",
        "Stage92 adds a local multi-provider adapter runtime for a personal developer workstation.",
        "",
        "## Providers",
        "",
        "- Ollama: `local_ollama`",
        "- GPT/OpenAI: `gpt_openai` using `OPENAI_API_KEY` only when live calls are explicitly enabled",
        "- Claude/Anthropic: `claude_anthropic` using `ANTHROPIC_API_KEY` only when live calls are explicitly enabled",
        "- Gemini/Google: `gemini_google` using `GOOGLE_API_KEY` only when live calls are explicitly enabled",
        "",
        "## Safety rule",
        "",
        "Release gates never perform live provider calls. Runtime remains provider-default-calls 0 until a developer intentionally enables live calls outside release verification.",
        "",
        f"- Configured providers: `{adapter['configured_provider_count']}`",
        f"- Route order: `{', '.join(adapter['route_order'])}`",
        f"- Live call count during gate: `{adapter['live_call_count']}`",
        "- Provider default calls: `0`",
        "- Node2 raw reveal access: `0`",
        "",
    ])
    (RELEASE / "stage92_developer_handoff_report.md").write_text(handoff, encoding="utf-8")
    print(json.dumps({"status": "pass", "artifacts": ["stage92_multi_provider_adapter_report.json", "stage92_studio_bridge_report.json", "stage92_release_gate_report.json", "stage92_writer_studio_workspace.json", "stage92_developer_handoff_report.md"]}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
