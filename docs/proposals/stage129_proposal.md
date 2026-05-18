# V1700 Stage129 제안서
## MultiWorkCIM + Cross-Work Canon Governor

## 1. 제안명

```text
V1700 Stage129 — MultiWorkCIM + Cross-Work Canon Governor
```

## 2. 제안 배경

Stage127은 MultiWork 직접 병합 전 preflight와 isolation audit를 수행했다.
Stage128은 SharedWorld / SharedCharacter를 read-only adapter로 흡수했다.

그러나 Stage128 이후에도 다음 질문이 남아 있다.

```text
작품별 CIM을 유지하면서, 작품 간 영향 관계와 canon 충돌을 안전하게 계산할 수 있는가?
```

Stage129는 이 질문에 답한다.

## 3. 최종 목표

```text
Project-local CIM은 보존한다.
Cross-project influence는 read-only edge로만 계산한다.
Canon conflict는 score와 decision으로 evidence화한다.
BLOCK 충돌은 자동 수정하지 않고 차단한다.
```

## 4. 필수 구현 항목

1. `multiwork_cim_governor` 패키지
2. Project-local CIM snapshot builder
3. CrossProjectInfluenceEdge read-only validator
4. CanonConflictScore calculator
5. Cross-Work Canon Governor
6. GitNexus / Python fallback preflight
7. Stage129 runner
8. Stage129 release gate
9. Stage129 manifests
10. Stage129 release evidence pack
11. Stage129 tests
12. Stage129 documentation bundle

## 5. 불변조건

```text
provider default calls = 0
live provider call count in release gate = 0
Node2 raw reveal access = 0
raw manuscript provider leakage = 0
raw manuscript cross-project leakage = 0
cross_project_influence_write = 0
canon_auto_resolution_count = 0
cross_work_canon_merge_allowed = false
branchpoint lineage preserved
repo doctor pass
main release gate pass
clean ZIP pass
```

## 6. 성공 기준

```text
Stage128 baseline gate pass
project-local CIM pass
cross-project read-only influence pass
canon BLOCK fixture detected and blocked
canon auto-resolution disabled
GitNexus/Python fallback preflight pass
Stage129 release gate pass
main release gate pass
repo doctor pass
pytest Stage129 pass
re-extracted ZIP verification pass
```

## 7. 개발자 전달 기준

로컬 Codex는 이 제안서를 기준으로 Stage129를 유지·확장하되, Stage130 전에는 write 권한과 canon auto-resolution을 켜지 않는다.
