from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.drama_composition import KoreanDramaCompositionEngine, DramaCompositionGate

if __name__ == "__main__":
    composition = KoreanDramaCompositionEngine().compose("주인공이 수련, 추방, 귀환의 세 국면을 통과하는 한국 드라마")
    gate = DramaCompositionGate().validate(composition)
    result = {"composition": composition.to_dict(), "gate": gate, "status": gate["status"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if gate["status"] == "pass" else 1)
