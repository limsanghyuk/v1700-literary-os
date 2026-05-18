import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import json
from v1700.longform import run_longform_execution_smoke

if __name__ == "__main__":
    print(json.dumps(run_longform_execution_smoke(), ensure_ascii=False, indent=2))
