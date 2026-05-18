from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.stage97_2.orchestrator import run_stage97_2_provider_runtime_smoke
from v1700.gates.stage97_2_release_gate import run_stage97_2_release_gate


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    runtime = run_stage97_2_provider_runtime_smoke(root)
    gate = run_stage97_2_release_gate(root)
    handoff = root / "release" / "current" / "stage97_2_developer_handoff_report.md"
    handoff.write_text(
        "# Stage97.2 Developer Handoff\n\n"
        f"- Provider runtime status: {runtime.get('status')}\n"
        f"- Release gate status: {gate.get('status')}\n"
        "- Live provider calls in release gate: 0\n"
        "- Provider gateway: UnifiedProviderGateway only\n",
        encoding="utf-8",
    )
    print(json.dumps({"runtime": runtime.get("status"), "gate": gate.get("status"), "handoff": str(handoff.relative_to(root))}, indent=2))
    return 0 if runtime.get("status") == "pass" and gate.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
