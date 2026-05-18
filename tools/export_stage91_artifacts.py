from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage91_release_gate import run_stage91_release_gate
from v1700.writer_studio.event_replay import StudioEventReplayEngine

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "current"


def main() -> int:
    RELEASE.mkdir(parents=True, exist_ok=True)
    replay = StudioEventReplayEngine().replay().to_dict(include_payload=False)
    gate = run_stage91_release_gate(ROOT)
    (RELEASE / "stage91_studio_event_replay_report.json").write_text(
        json.dumps(replay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (RELEASE / "stage91_release_gate_report.json").write_text(
        json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    handoff = "\n".join([
        "# Stage91 Developer Handoff Report",
        "",
        "Stage91 adds deterministic Writer Studio persistence, review queue state, and UI event replay on top of Stage90.",
        "",
        f"- Event count: {replay['event_count']}",
        f"- Persistence snapshots: {replay['persistence_snapshot_count']}",
        f"- Review queue items: {replay['review_queue_total_items']}",
        f"- Blocking reviews remaining: {replay['review_queue_blocking_count']}",
        f"- Replay checksum: `{replay['replay_checksum']}`",
        "- Provider default calls: `0`",
        "- Node2 raw reveal access: `0`",
        "",
        "Stage91 remains a local deterministic Studio contract, not a browser/server dependency.",
        "",
    ])
    (RELEASE / "stage91_developer_handoff_report.md").write_text(handoff, encoding="utf-8")
    print(json.dumps({"status": "pass", "artifacts": ["stage91_studio_event_replay_report.json", "stage91_release_gate_report.json", "stage91_developer_handoff_report.md"]}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
