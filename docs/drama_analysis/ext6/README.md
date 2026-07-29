# EXT6 드라마 보강 허브

- 상태: `ACTIVE / USER APPROVED`
- 기준일: `2026-07-29`
- Core 권위: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`
- EXT6 권위: `EXT6_SINGLE_AUTHORITY_V1_2`
- Gold method anchor: 《비밀의숲》
- Legacy normalization anchor: 《돌아온일지매》

## 필수 로드 순서

1. `CURRENT_EXT6_POINTER.json`
2. `EXT6_SINGLE_AUTHORITY_V1_2.md`
3. `EXT6_EXACT_SCHEMA_REGISTRY_V1_1.json`
4. `EXT6_ROLLOUT_QUEUE_85WORKS_20260729.json`
5. 대상 작품의 EXT6 work state·마지막 검증 보고서

## 핵심 결정

EXT6는 Stage01~04를 대체하지 않는다. 원본–SceneCard 정렬, 등장 인물·언급 인물, 인물 부하, 장면 포괄성을 증명하고 기존 Stage03의 누락 위험을 찾는 보조 증거 계층이다. 기존 의미 정본은 보존하고 실제 상태·관계 변화가 원문에서 다시 확인된 경우에만 `SELECTIVE_APPEND`한다.

## 현재 상태

- 《비밀의숲》: EXT6 V1.1 전 시즌 완료, Functional Holdout PASS, gold method anchor
- 《돌아온일지매》: 전 시즌 legacy EXT6 존재, 65장면 계보 정규화 별도 필요
- `101번째프로포즈`: EXT6 V1.2 증거 계층 PASS, 위험 감사 진행
- 이후 작품: 고정 큐의 가나다순 실행

## 금지

- 출연량만으로 CharacterArc 자동 생성
- 공동 등장만으로 RelationshipArc 자동 생성
- 기존 Stage01~04 전면 재저작
- 기존 레코드 덮어쓰기·삭제
- 후보 Arc에서 holdout 질문 자동 생성
- 사용자 승인 없는 CANONICAL 자동 승격
