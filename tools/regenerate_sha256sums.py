from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from v1700.release_integrity.asset_checker import build_sha256_sums_lines


def main() -> int:
    root = ROOT
    filelist_path = root / "FILELIST.txt"
    sums_path = root / "SHA256SUMS.txt"
    lines = build_sha256_sums_lines(root, filelist_path)
    sums_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(sums_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
