from __future__ import annotations

import json

from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate


if __name__ == "__main__":
    result = run_symbol_to_branchpoint_trace_gate()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
