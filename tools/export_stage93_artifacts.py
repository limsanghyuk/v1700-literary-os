from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.gates.stage93_release_gate import run_stage93_release_gate
from v1700.provider_adapters.credential_audit import audit_provider_credentials
from v1700.provider_adapters.live_sandbox import run_stage93_live_provider_sandbox
from v1700.provider_adapters.normalization import run_stage93_response_normalization_probe

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "current"


def main() -> int:
    RELEASE.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "stage93_credential_audit_report.json": audit_provider_credentials().to_dict(),
        "stage93_response_normalization_report.json": run_stage93_response_normalization_probe().to_dict(),
        "stage93_live_provider_sandbox_report.json": run_stage93_live_provider_sandbox().to_dict(),
        "stage93_release_gate_report.json": run_stage93_release_gate(),
    }
    for name, payload in artifacts.items():
        (RELEASE / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    handoff = RELEASE / "stage93_developer_handoff_report.md"
    handoff.write_text("""# Stage93 Developer Handoff

Stage93 adds a live-provider opt-in sandbox, credential redaction audit, and response normalization layer for Ollama, GPT, Claude, and Gemini. Release gates remain provider-zero.

## Local live opt-in

```bash
export V1700_ALLOW_PROVIDER_CALLS=1
export V1700_STAGE93_EXECUTE_LIVE_PROVIDER=1
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GOOGLE_API_KEY=...
python tools/run_stage93_live_provider_sandbox.py
```

The release gate intentionally runs with live execution disabled and validates redaction, normalization, and zero default calls.
""", encoding="utf-8")
    print(json.dumps({"status": "pass", "artifacts": sorted(artifacts) + ["stage93_developer_handoff_report.md"]}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
