# EXT6 보류·별도 sidecar 운영 정책 v1

- Document ID: `EXT6-DEFERRED-SIDECAR-POLICY-V1`
- Status: `DEFERRED_OPTIONAL_EXPERIMENT`
- Date: 2026-07-15
- Applies to: 신규 드라마 분석, 기존 Stage01~03 작품의 Stage04 업그레이드, seqcard_ko 데이터베이스

## 1. 결정

```text
EXT6_DEFAULT_ENABLED = false
EXT6_IS_REQUIRED_FOR_STAGE01_04_COMPLETION = false
EXT6_DATABASE_ROLLOUT = deferred
```

EXT6은 Stage01~04 exact schema를 변경하지 않는 별도 sidecar다. 현재 장편 드라마 한 작품을 회차별로 직접독해하고 Stage01~04까지 완결하는 작업에서 컨텍스트·실행 한도 압박이 크므로 기본 운영에서 제외한다.

## 2. 보류 사유

- 장면×인물 단위 CastPresence가 SceneCard보다 훨씬 많은 행을 생성한다.
- EntityBridge·CastPresence·Coverage·Alignment·CharacterLoad 검증이 회차 체크포인트 크기와 컨텍스트를 증가시킨다.
- Stage01~04와 동시에 수행할 경우 회차 영속화 이전 중단 위험이 커진다.
- 현재 우선 목표는 49작품 데이터베이스의 Stage01~04 완결성과 15개 미완료 작품 업그레이드다.
- EXT6 유용성은 존재하지만 전체 코퍼스 비용 대비 효과가 아직 확정되지 않았다.

## 3. 보존하는 자산

다음 계약·파일럿·사고 기록은 삭제하지 않는다.

- `DRAMA_STAGE_EXT6_CONTRACT_MATRIX_V3.md`
- EntityBridge 9키
- CastPresence 10키
- CharacterLoad 17키
- CastCoverageLedger
- SourceSceneAlignmentRecord
- 돌아온일지매 EXT6 적용 경험
- 비밀의숲 GPT×Claude 파일럿·비교 자료

이들은 실험 lineage와 별도 문서 경로에서 유지한다.

## 4. Stage01~04와의 경계

- SceneCard·SequenceBlueprint·Arc·Edge 파일에 EXT6 필드를 추가하지 않는다.
- EXT6 work_id/episode_no 규칙을 Stage01~04 파일에 혼용하지 않는다.
- EXT6 미적용 작품도 Stage01~04 강검증을 통과하면 `PASS_CANDIDATE`가 될 수 있다.
- 데이터베이스의 `STAGE01_04_COMPLETE` 집계는 EXT6 존재 여부와 무관하다.
- EXT6 파일이 없는 것을 warning/error로 처리하지 않는다.

## 5. 검증 게이트 처리

EXT6 비활성 run:

```text
Gate 0: required
Gate 1: required
Gate 2: required
Gate 3: required
Gate 4: NOT_APPLICABLE_EXT6_DEFERRED
Gate 5: required
Gate 6: required
```

EXT6 활성 파일럿:

```text
Gate 4A: exact schema·enum·grain·FK·deterministic recalculation
Gate 4B: evidence·coverage·alignment·misclassification
```

## 6. 재활성화 조건

다음 조건을 모두 충족할 때만 재개한다.

1. 사용자 명시 승인
2. 작품 전체가 아닌 1회차 파일럿
3. Stage01~04 run과 별도 run_id·branch·package
4. 원본과 SourceSceneAlignment 확보
5. 장면별 직접독해 증명
6. Python 의미 생성 없음
7. Gate A/B errors 0
8. 컨텍스트·시간·파일 크기 비용 측정
9. 창작 엔진 또는 검색·비평 성능의 ablation 개선 증명
10. 전 코퍼스 적용 전 별도 승인

## 7. 파일럿 안전 단위

```text
1 episode only
Q1→Q2→Q3→Q4
Stage01 checkpoint first
EXT6 capture/review second
separate EXT6 checkpoint
```

Stage01~04 본체의 회차 체크포인트를 EXT6 실패 때문에 오염시키지 않는다.

## 8. 허브·패키지 정책

- EXT6 문서와 metadata는 허브에 보존 가능하다.
- raw script는 허브에 커밋하지 않는다.
- EXT6 sidecar는 `_ext6_audit`, `authored_bridge`, `authored_cast`, `derived_character_load` 등 별도 폴더를 사용한다.
- Stage01~04 독립 작품 ZIP과 EXT6 파일럿 ZIP은 분리한다.
- 자동 병합으로 canonical을 만들지 않는다.

## 9. 다음 검토 시점

현재 15개 Stage04 미완료 작품의 업그레이드가 상당 부분 완료된 뒤 다음을 검토한다.

- 1회차당 추가 행 수·파일 크기·컨텍스트 비용
- CharacterLoad의 창작 엔진 효용
- 인물 중심 검색/비평 성능 개선
- Stage03 CharacterArc와의 중복도
- provider 간 일치도와 adjudication 비용

그 전까지 EXT6은 `DEFERRED_OPTIONAL_EXPERIMENT` 상태를 유지한다.
