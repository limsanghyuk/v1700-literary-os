from __future__ import annotations

import argparse
import json

from v1700.ir.style_profile import StyleProfileIR
from v1700.nodes.node1_architect import Node1Architect
from v1700.nodes.node2_prose_renderer import Node2ProseCompiler

CLI_VERSION = "V1700 Stage143 - User CLI/API Minimum Docs"
DEFAULT_PROMPT = "A cautious heir finally notices the smallest change in the family's ledger."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="V1700 local-first literary runtime")
    parser.add_argument("prompt", nargs="?", default=DEFAULT_PROMPT)
    parser.add_argument("--json", action="store_true", help="emit RenderedProseIR JSON")
    parser.add_argument("--version", action="version", version=CLI_VERSION)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
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
