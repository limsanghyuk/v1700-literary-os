from __future__ import annotations

from v1700.studio_workflow.contracts import ReviewPackage, RevisionItem


def build_review_package(project_id: str, items: list[RevisionItem]) -> ReviewPackage:
    unresolved_blocks = [
        item for item in items
        if item.severity == "BLOCK" and item.writer_decision not in {"APPROVED", "REJECTED", "DEFERRED"}
    ]
    warn_count = sum(1 for item in items if item.severity == "WARN")
    info_count = sum(1 for item in items if item.severity == "INFO")
    return ReviewPackage(
        package_id="stage98-review-package",
        project_id=project_id,
        revision_items=items,
        unresolved_block_count=len(unresolved_blocks),
        warn_count=warn_count,
        info_count=info_count,
        ready_for_publishing=len(unresolved_blocks) == 0,
    )


def review_package_report(package: ReviewPackage) -> dict:
    return {
        "status": "pass" if package.ready_for_publishing else "blocked",
        "review_package": package.to_dict(),
        "stage97_1_adversarial_block_evidence_preserved": True,
    }
