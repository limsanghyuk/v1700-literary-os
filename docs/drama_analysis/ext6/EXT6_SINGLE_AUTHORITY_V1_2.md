# EXT6 단일 실행 권위 V1.2

Document ID: `EXT6_SINGLE_AUTHORITY_V1_2`  
Effective date: `2026-07-29`  
Status: `ACTIVE_USER_APPROVED`  
Core authority: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`

## 1. 목적

기존 87작품의 Stage01~04 정본을 보존하면서 인물 포괄성·원본 접지·앙상블 누락을 추가 검사한다. 《비밀의숲》에서 검증된 방법을 gold method anchor로 사용하고, 《돌아온일지매》는 legacy 자료를 현행 규격으로 정규화한 뒤 비교 앵커로 유지한다.

## 2. EXT6 레이어

1. `EntityRegistry`: 작품 내부 인물 identity와 alias 정규화
2. `EntityBridge`: 실제 사용 인물과 registry provenance 연결
3. `SourceHeadingRegistry`: 원본 물리 헤딩·line·offset 목록
4. `SourceSceneAlignment`: 모든 SceneCard와 원본 fragment의 순차 정렬 및 hash
5. `CastPresence`: 장면별 등장·음성·원격·회상·언급과 초점·발화 상태
6. `CastCoverageLedger`: annotated/legitimate empty/unresolved의 완전 분할
7. `CharacterLoad`: CastPresence에서 결정론적으로 파생한 장면·시퀀스·Act 부하
8. `RiskAudit`: 기존 CharacterArc·RelationshipArc의 누락 후보 생성·직접 독해 판정
9. `SelectiveAppendLedger`: 수용·거부 이유와 기존 prefix 불변성
10. `FunctionalHoldout`: 기존 핵심 회수 보존과 보강 질문 개선 검증

## 3. 작품 실행 순서

```text
V10.1 core·대상 work state 로드
→ 원본 hash와 SceneCard ordinal 고정
→ source format adapter 판정
→ EntityRegistry/alias 저작
→ SourceHeadingRegistry
→ SourceSceneAlignment 100%
→ CastPresence 직접 원본 접지
→ CastCoverage 완전 분할
→ CharacterLoad 결정론 파생
→ 독립 EXT6 validator
→ 고위험 인물·관계 후보 생성
→ 후보별 원본·SceneCard·기존 Stage03 직접 대조
→ SELECTIVE_APPEND 또는 REJECT
→ 독립 Functional Holdout
→ 비대상 파일 불변성
→ 작품 단위 Fresh Extraction
→ completion manifest
```

## 4. SourceSceneAlignment 규칙

- SceneCard 수와 alignment 수가 같아야 한다.
- 원본 fragment는 증가 순서이고 겹치거나 역행하지 않는다.
- 원본 전체 SHA와 fragment SHA를 모두 저장한다.
- 허용 유형: `ONE_TO_ONE`, `MERGED_SOURCE_HEADINGS`, `LOGICAL_REHEADING`, `MERGED_SOURCE_HEADINGS_WITH_LOGICAL_REHEADING`.
- 자동 정렬 실패·헤딩 오염·탭 삽입은 수동 override로 고정하고 근거 line을 남긴다.
- V1.2 parser는 선행 탭 대사 형식과 `E/F/N/L/NA/NAR` 전달 표기를 정규화한다.

## 5. CastPresence 규칙

- `ONSCREEN`: 장면의 물리적 인물
- `VOICE_ONLY`: E/N/L 등 음성만 존재
- `PHONE_OR_REMOTE`: F 또는 전화·원격 발화
- `ARCHIVAL_OR_MEMORY`: 회상·사진·영상·CCTV·기억
- `REFERENCED_ONLY`: 대사에서 언급되지만 장면에 존재하지 않음
- presence 의미 판정은 원본에서만 한다. SceneCard·POV는 focality 순위의 보조 신호일 뿐 존재를 제조하지 않는다.

## 6. 위험도 감사

후보 신호:

- `MAJOR/DOMINANT`인데 해당 회차 CharacterArc가 없음
- 여러 회차에서 `MINOR` 이상인데 시즌 CharacterArc가 희박함
- 반복적인 직접 상호작용이 있으나 RelationshipArc가 없음
- 기존 Arc trigger_scene_no에 당사자 CastPresence가 없음
- alias 분산으로 동일 인물이 여러 identity로 갈라짐
- 원본 물리 헤딩과 SceneCard 경계의 불일치

신호는 Arc가 아니다. 후보마다 원본을 직접 다시 읽어 실제 state delta 또는 relationship delta가 있을 때만 수용한다.

## 7. 선택 보강

- 기본 mode: `SELECTIVE_APPEND`
- 기존 bytes는 exact prefix로 보존한다.
- overwrite/delete는 0이어야 한다.
- Stage01·02·04는 변경하지 않는다.
- 새 레코드는 exact V10/V10.1 Stage03 schema를 따른다.
- 기각 후보도 사유를 ledger에 저장한다.

## 8. Functional Holdout

- 질문·정답은 후보 레코드에서 자동 생성하지 않는다.
- baseline 고정 이전에 독립적으로 core 질문을 설계한다.
- supplemental 질문은 원본 사건에서 독립 저작한다.
- core Recall@5는 하락할 수 없다.
- supplemental Recall@5는 개선되어야 한다.
- 비대상 파일 hash와 Fresh Extraction 재현성을 함께 검사한다.

## 9. Gold anchor 판정

《비밀의숲》은 16회·1,037장면 전체 정렬, unresolved 0, CastPresence 3,763, CharacterLoad 663, EntityBridge 139, 위험 후보 55 중 22건 선택 보강, core Recall@5 1.0 유지, supplemental Recall@5 0.0→1.0을 통과했다. 이 방법과 검증 순서를 85작품 rollout의 기준으로 사용한다.

## 10. 큐 정책

`AUTHORED_WORK_INDEX_V23.json`의 순서를 고정한다. 《돌아온일지매》와 《비밀의숲》을 제외한 85작품을 `101번째프로포즈`, `W`, `강남엄마따라잡기` 순으로 진행한다. 작품 하나가 completion manifest와 Fresh Extraction PASS를 얻기 전 다음 작품을 완료 상태로 올리지 않는다.
