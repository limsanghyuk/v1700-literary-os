from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from v1700.corpus_absorption import run_local_corpus_absorption


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a metadata-only canonical corpus absorption pack.")
    parser.add_argument("--corpus-root", type=Path, default=None, help="Path to the local corpus root.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Optional output directory for the absorption pack.")
    args = parser.parse_args()
    result = run_local_corpus_absorption(ROOT, corpus_root=args.corpus_root, output_dir=args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
