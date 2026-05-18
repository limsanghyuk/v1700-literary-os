from __future__ import annotations

from collections.abc import Mapping

from v1700.nie.asd.contracts import ArcConsistencyReport, ArcIssue


class ArcConsistencyChecker:
    """V545 arc consistency concept absorbed as deterministic checks."""

    def check(self, graph: Mapping) -> ArcConsistencyReport:
        issues: list[ArcIssue] = []
        for character in graph.get("characters", []):
            cid = str(character.get("id"))
            label = str(character.get("label", cid))
            if not character.get("tracked", True):
                issues.append(ArcIssue(
                    issue_id=f"A-{len(issues)+1:03d}",
                    issue_type="arc_not_tracked",
                    character_id=cid,
                    label=label,
                    severity=float(character.get("severity", 0.35)),
                ))
            first = character.get("episode_first")
            last = character.get("episode_last")
            if first is not None and last is not None and int(first) > int(last):
                issues.append(ArcIssue(
                    issue_id=f"A-{len(issues)+1:03d}",
                    issue_type="arc_episode_inversion",
                    character_id=cid,
                    label=label,
                    severity=0.90,
                ))
        for rel in graph.get("relationships", []):
            if rel.get("post_death_edge", False):
                issues.append(ArcIssue(
                    issue_id=f"A-{len(issues)+1:03d}",
                    issue_type="arc_post_death_edge",
                    character_id=str(rel.get("character_id", rel.get("id"))),
                    label=str(rel.get("label", rel.get("id"))),
                    severity=float(rel.get("severity", 0.50)),
                    related_ids=tuple(map(str, rel.get("related_ids", ()))),
                ))
            contradiction_count = int(rel.get("contradiction_count", 0))
            if contradiction_count >= 2:
                issues.append(ArcIssue(
                    issue_id=f"A-{len(issues)+1:03d}",
                    issue_type="arc_contradiction_overflow",
                    character_id=str(rel.get("character_id", rel.get("id"))),
                    label=str(rel.get("label", rel.get("id"))),
                    severity=float(rel.get("severity", 0.65)),
                    related_ids=tuple(map(str, rel.get("related_ids", ()))),
                ))
        score = sum(issue.severity for issue in issues) / max(1, len(issues))
        status = "pass" if score <= 0.40 else "warn"
        return ArcConsistencyReport(status=status, issues_found=tuple(issues), overall_score=score)
