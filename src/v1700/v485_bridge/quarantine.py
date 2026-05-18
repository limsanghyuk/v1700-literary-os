from __future__ import annotations
from pathlib import Path

FORBIDDEN_DIRECT_IMPORTS = (
    "literary_system.llm_bridge",
    "tools.run_release_gate",
    "MANIFEST_V485_COMPLETE",
)

def quarantine_policy() -> dict:
    return {
        "status": "pass",
        "direct_code_import_allowed": False,
        "metadata_direct_import_allowed": False,
        "release_gate_replacement_allowed": False,
        "allowed_absorption_mode": "wrap_only_or_recompiled_contract",
        "forbidden_direct_imports": list(FORBIDDEN_DIRECT_IMPORTS),
    }

def assert_no_v485_direct_imports(root: Path) -> dict:
    hits: list[str] = []
    for base in (root / "src", root / "tools", root / "tests"):
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if path.name == "quarantine.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for forbidden in FORBIDDEN_DIRECT_IMPORTS:
                if forbidden in text:
                    hits.append(path.relative_to(root).as_posix() + ":" + forbidden)
    return {"status": "pass" if not hits else "blocked", "direct_import_hits": hits}
