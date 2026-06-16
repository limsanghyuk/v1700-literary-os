from __future__ import annotations

import json
from pathlib import Path

from v1700.value_proof_arm_b_guidance_surface import run_value_proof_arm_b_guidance_surface


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    result = run_value_proof_arm_b_guidance_surface(repo_root=repo_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
