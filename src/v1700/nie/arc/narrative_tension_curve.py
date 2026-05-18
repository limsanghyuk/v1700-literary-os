from __future__ import annotations

import math
from collections import Counter
from typing import Any, Iterable

from v1700.nie.arc.contracts import SceneTensionPoint, TensionLossReport


class NarrativeTensionCurve:
    """Stage117 deterministic 4-act narrative tension curve.

    The ideal curve follows the Phase-3 NIE blueprint:
        T_ideal(t)=0.60+0.40*sin(2πt-0.50)+0.20*sin(6πt)

    Values are clipped to [0, 1] for gate-friendly scoring. The class accepts
    SceneTensionPoint, dict-like scene samples, or light objects with matching
    attributes so future Stage118/119 orchestrators can reuse it directly.
    """

    DEFAULT_ACT_TARGETS: dict[int, int] = {1: 2, 2: 2, 3: 2, 4: 2}

    def __init__(self, block_threshold: float = 0.18, warn_threshold: float = 0.10) -> None:
        if warn_threshold > block_threshold:
            raise ValueError("warn_threshold cannot exceed block_threshold")
        self.block_threshold = float(block_threshold)
        self.warn_threshold = float(warn_threshold)

    def ideal(self, t: float) -> float:
        t = min(max(float(t), 0.0), 1.0)
        value = 0.60 + 0.40 * math.sin(2.0 * math.pi * t - 0.50) + 0.20 * math.sin(6.0 * math.pi * t)
        return round(min(max(value, 0.0), 1.0), 6)

    def actual(self, scenes: Iterable[Any]) -> list[float]:
        return [self._scene_score(scene) for scene in scenes]

    def ideal_series(self, scenes: Iterable[Any]) -> list[float]:
        return [self.ideal(self._scene_position(scene)) for scene in scenes]

    def tension_loss(self, scenes: Iterable[Any]) -> float:
        rows = list(scenes)
        if not rows:
            return 0.0
        squared = []
        for scene in rows:
            observed = self._scene_score(scene)
            target = self.ideal(self._scene_position(scene))
            squared.append((observed - target) ** 2)
        return round(sum(squared) / len(squared), 6)

    def coverage_loss(self, scenes: Iterable[Any], target_counts: dict[int, int] | None = None) -> float:
        rows = list(scenes)
        targets = target_counts or self.DEFAULT_ACT_TARGETS
        counts = Counter(self._scene_act(scene) for scene in rows)
        loss = sum(max(0, int(target) - int(counts.get(int(act), 0))) ** 2 for act, target in targets.items())
        return float(loss)

    def final_loss(self, scenes: Iterable[Any], lam: float = 0.3, target_counts: dict[int, int] | None = None) -> float:
        rows = list(scenes)
        return round(self.tension_loss(rows) + float(lam) * self.coverage_loss(rows, target_counts), 6)

    def evaluate(self, scenes: Iterable[Any], lam: float = 0.3, target_counts: dict[int, int] | None = None) -> TensionLossReport:
        rows = list(scenes)
        tension = self.tension_loss(rows)
        coverage = self.coverage_loss(rows, target_counts)
        final = round(tension + float(lam) * coverage, 6)
        if final >= self.block_threshold:
            status = "BLOCK"
        elif final >= self.warn_threshold:
            status = "WARN"
        else:
            status = "PASS"
        return TensionLossReport(
            scene_count=len(rows),
            tension_loss=tension,
            coverage_loss=coverage,
            final_loss=final,
            lambda_coverage=float(lam),
            status=status,  # type: ignore[arg-type]
        )

    def per_scene_rows(self, scenes: Iterable[Any]) -> list[dict[str, Any]]:
        rows = []
        for scene in scenes:
            position = self._scene_position(scene)
            observed = self._scene_score(scene)
            target = self.ideal(position)
            rows.append({
                "scene_id": self._scene_id(scene),
                "position": position,
                "act": self._scene_act(scene),
                "actual_tension": observed,
                "ideal_tension": target,
                "squared_error": round((observed - target) ** 2, 6),
            })
        return rows

    @staticmethod
    def _scene_id(scene: Any) -> str:
        if isinstance(scene, dict):
            return str(scene.get("scene_id") or scene.get("id") or "scene")
        return str(getattr(scene, "scene_id", getattr(scene, "id", "scene")))

    @staticmethod
    def _scene_position(scene: Any) -> float:
        if isinstance(scene, dict):
            raw = scene.get("position", scene.get("t", 0.0))
        else:
            raw = getattr(scene, "position", getattr(scene, "t", 0.0))
        return min(max(float(raw), 0.0), 1.0)

    @staticmethod
    def _scene_score(scene: Any) -> float:
        if isinstance(scene, dict):
            raw = scene.get("tension_score", scene.get("tension", 0.0))
        else:
            raw = getattr(scene, "tension_score", getattr(scene, "tension", 0.0))
        return min(max(float(raw), 0.0), 1.0)

    @staticmethod
    def _scene_act(scene: Any) -> int:
        if isinstance(scene, dict):
            raw = scene.get("act")
        else:
            raw = getattr(scene, "act", None)
        if raw is None:
            pos = NarrativeTensionCurve._scene_position(scene)
            return min(int(pos * 4) + 1, 4)
        return min(max(int(raw), 1), 4)
