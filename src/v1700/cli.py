from __future__ import annotations
import argparse, json
from v1700.nodes.node1_architect import Node1Architect
from v1700.nodes.node2_prose_renderer import Node2ProseCompiler
from v1700.ir.style_profile import StyleProfileIR

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="V1700 local-first literary runtime")
    parser.add_argument("prompt", nargs="?", default="주인공이 조력자의 침묵을 처음 의심한다")
    parser.add_argument("--json", action="store_true", help="emit RenderedProseIR JSON")
    args = parser.parse_args(argv)
    scene = Node1Architect().make_scene(args.prompt)
    rendered = Node2ProseCompiler().compile(scene, StyleProfileIR()).rendered
    if args.json:
        print(json.dumps(rendered.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(rendered.final_text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
