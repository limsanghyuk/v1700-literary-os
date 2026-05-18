from __future__ import annotations

import json

from v1700.sidecars.gitnexus.contracts import GitNexusCommandResult


def normalize_gitnexus_result(result: GitNexusCommandResult) -> dict:
    payload: dict | list | str
    stdout = result.stdout.strip()
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = stdout
    else:
        payload = {}

    return {
        "provider": "gitnexus_cli",
        "capability": result.capability,
        "available": result.ok,
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "payload": payload,
        "stderr": result.stderr.strip(),
    }
