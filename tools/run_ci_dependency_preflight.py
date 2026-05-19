from __future__ import annotations

import ast
import json
import sys
import sysconfig
try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 support.
    import tomli as tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_IMPORTS = {"tools", "v1700"}


def _stdlib_modules() -> set[str]:
    modules = set(sys.stdlib_module_names)
    stdlib_path = Path(sysconfig.get_paths()["stdlib"])
    for path in stdlib_path.glob("*.py"):
        modules.add(path.stem)
    return modules


def _dev_dependency_names() -> set[str]:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    deps = pyproject.get("project", {}).get("optional-dependencies", {}).get("dev", [])
    names: set[str] = set()
    for dep in deps:
        normalized = dep.split("[", 1)[0]
        normalized = normalized.split(";", 1)[0]
        normalized = normalized.split(">=", 1)[0]
        normalized = normalized.split("==", 1)[0]
        normalized = normalized.split("~=", 1)[0]
        normalized = normalized.split("<", 1)[0]
        normalized = normalized.strip().lower().replace("-", "_")
        if normalized:
            names.add(normalized)
    return names


def _imports_under_tests() -> set[str]:
    imports: set[str] = set()
    for path in (ROOT / "tests").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".", 1)[0])
    return imports


def main() -> int:
    stdlib = _stdlib_modules()
    dev_deps = _dev_dependency_names()
    imports = _imports_under_tests()
    external = {
        name.lower().replace("-", "_")
        for name in imports
        if name not in stdlib and name not in PROJECT_IMPORTS and not name.startswith("__")
    }
    missing = sorted(external - dev_deps)
    report = {
        "status": "pass" if not missing else "fail",
        "test_imports_external": sorted(external),
        "dev_dependencies": sorted(dev_deps),
        "missing_from_dev_dependencies": missing,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
