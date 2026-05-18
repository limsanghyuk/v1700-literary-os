from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.nodes.node1_architect import Node1Architect
from v1700.nodes.node2_prose_renderer import Node2ProseCompiler, aggregate_report
from v1700.ir.style_profile import StyleProfileIR

if __name__ == "__main__":
    scenes = [Node1Architect().make_scene("주인공이 조력자의 침묵을 처음 의심한다")]
    rendered = Node2ProseCompiler().compile_many(scenes, StyleProfileIR())
    report = aggregate_report(rendered)
    out = Path("release/current/stage72_node2_prose_compiler_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"report": report, "rendered": [r.to_dict() for r in rendered]}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "pass" else 1)
