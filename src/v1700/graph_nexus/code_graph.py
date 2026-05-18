from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class CodeNode:
    path: str
    defines: tuple[str, ...] = ()
    imports: tuple[str, ...] = ()
    tested_by: tuple[str, ...] = ()
    gated_by: tuple[str, ...] = ()
    stage_origin: str = "STAGE72"

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "defines": list(self.defines),
            "imports": list(self.imports),
            "tested_by": list(self.tested_by),
            "gated_by": list(self.gated_by),
            "stage_origin": self.stage_origin,
        }


@dataclass(frozen=True)
class CodeGraph:
    nodes: tuple[CodeNode, ...] = ()
    fallback_used: bool = True
    source: str = "python_fallback"

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "fallback_used": self.fallback_used,
            "node_count": len(self.nodes),
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def find(self, needle: str) -> list[CodeNode]:
        needle_lower = needle.lower()
        return [
            node
            for node in self.nodes
            if needle_lower in node.path.lower()
            or any(needle_lower in item.lower() for item in node.defines)
        ]


class CodeGraphBuilder:
    def build(self, root: Path) -> CodeGraph:
        src_root = root / "src" / "v1700"
        test_files = [path for path in (root / "tests").rglob("test_*.py") if path.is_file()]
        nodes: list[CodeNode] = []
        for path in sorted(src_root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            rel = path.relative_to(root).as_posix()
            defines, imports = self._scan_python(path)
            nodes.append(
                CodeNode(
                    path=rel,
                    defines=defines,
                    imports=imports,
                    tested_by=self._matching_tests(rel, defines, test_files, root),
                    gated_by=self._matching_gates(rel),
                    stage_origin=self._stage_origin(rel),
                )
            )
        return CodeGraph(nodes=tuple(nodes), fallback_used=True)

    def _scan_python(self, path: Path) -> tuple[tuple[str, ...], tuple[str, ...]]:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            return (), ()
        defines: list[str] = []
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                defines.append(node.name)
            elif isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        return tuple(sorted(set(defines))), tuple(sorted(set(imports)))

    def _matching_tests(
        self, rel: str, defines: tuple[str, ...], test_files: list[Path], root: Path
    ) -> tuple[str, ...]:
        haystack = " ".join([rel, *defines]).lower()
        matches: list[str] = []
        for test_file in test_files:
            name = test_file.name.lower()
            if any(part and part in name for part in Path(rel).stem.lower().split("_")):
                matches.append(test_file.relative_to(root).as_posix())
            elif "node2" in haystack and "node2" in name:
                matches.append(test_file.relative_to(root).as_posix())
            elif "graph_nexus" in haystack and "stage72_1" in name:
                matches.append(test_file.relative_to(root).as_posix())
        return tuple(sorted(set(matches)))

    def _matching_gates(self, rel: str) -> tuple[str, ...]:
        gates: list[str] = []
        if "/gates/" in rel:
            gates.append(Path(rel).stem)
        if "node2_prose_renderer" in rel:
            gates.append("node_projection_gate")
        if "graph_nexus" in rel or "sidecars/gitnexus" in rel:
            gates.append("graph_nexus_release_gate")
        return tuple(sorted(set(gates)))

    def _stage_origin(self, rel: str) -> str:
        if "graph_nexus" in rel or "sidecars/gitnexus" in rel:
            return "STAGE72.1"
        if "node2_prose_renderer" in rel:
            return "STAGE71_72"
        return "STAGE72"
