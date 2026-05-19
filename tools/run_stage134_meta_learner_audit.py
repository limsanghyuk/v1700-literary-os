from __future__ import annotations

import json

from v1700.meta_learner_audit import run_stage134_meta_learner_audit


if __name__ == "__main__":
    print(json.dumps(run_stage134_meta_learner_audit(), ensure_ascii=False, indent=2))
