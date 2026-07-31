# EXT6 단일 실행 권위 V1.2

Document ID: `EXT6_SINGLE_AUTHORITY_V1_2`  
Effective date: `2026-07-29`  
Last amended: `2026-07-31`  
Status: `ACTIVE_USER_APPROVED_SINGLE_METHOD_AUTHORITY`  
Core authority: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`

## 1. 목적

기존 Stage01~04 정본을 보존하면서 인물 포괄성·원본 접지·앙상블 누락을 추가 검사한다. 《비밀의숲》에서 검증된 방법을 gold method anchor로 사용하고, 《돌아온일지매》는 legacy 비교 앵커로 유지한다.

이 문서는 EXT6 분석 방법과 실행 순서의 유일한 권위 문서다. 이후 발견되는 데이터 오류·정렬 오류·검증기 오류·Entity 오류는 이 문서의 버전을 올리지 않고 동일 문서와 운영 문서를 수정·보강하여 해결한다.

## 2. 권위 우선순위와 버전 동결

1. 사용자의 최신 명시 지시
2. `EXT6_SINGLE_AUTHORITY_V1_2` — 분석 방법·완료 정의·실행 순서
3. `EXT6_EXACT_SCHEMA_REGISTRY_V1_1` — 레코드 키·enum·자료형
4. 《비밀의숲》 — gold method anchor
5. `EXT6_FIXED_VERSION_CORRECTION_POLICY_20260730.md` — 데이터 교정·supersession 규칙
6. `EXT6_NEW_SESSION_HANDOFF.md` — 현재 작업 상태와 재개 지점

`V1.3`, `V1.4`, `V1.5`, `V1.6` 등의 과거 파일 표기는 패키지 또는 교정 이력일 뿐 분석 방법의 권위가 아니다. 새로운 EXT6 방법 버전은 만들지 않는다. 문제가 생기면 이 V1.2 문서와 기존 V1.1 스키마 문서를 수정·보강한다.

## 3. EXT6 필수 레이어

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

위 10개 계층이 모두 존재하고 각 게이트를 통과해야 `EXT6 완료`로 판정한다. 정렬·스키마·CRC만 통과한 상태는 구조 PASS일 뿐 완료가 아니다.

## 4. 작품 실행 순서

```text
V10.1 core·대상 work state 로드
→ 권위 preflight와 baseline hash 고정
→ 원본 hash와 SceneCard ordinal 고정
→ source format adapter 판정
→ EntityRegistry/alias 직접 정규화
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
→ 최종 레코드 동결 후 감사 재계산
→ 작품 단위 Fresh Extraction
→ completion manifest
```

## 5. 실행 한도 보호와 체크포인트

검사가 과도하여 작업이 중단되지 않도록 다음 주기를 고정한다.

- 회차 완료 시: 경검사 — JSON 파싱, 장면 수, 근거 구간 내부 여부, enum, unresolved
- 8회 블록 완료 시: 강검사 — 정렬 증가·비중첩, 근거 중복, alias 충돌, 비인물 Entity, presence/focality 표본 직접 대조
- 전 회차 완료 시: 최종 강검사 1회 — RiskAudit, SelectiveAppend, FunctionalHoldout, baseline 불변성, ZIP CRC, Fresh Extraction
- 각 회차와 블록 종료 시 checkpoint를 저장하고 중단 시 마지막 완료 checkpoint 다음부터 재개한다.
- 최종 봉인 전에는 전체 DB 반복 해제·전수 해시를 수행하지 않는다.

## 6. SourceSceneAlignment 규칙

- SceneCard 수와 alignment 수가 같아야 한다.
- 원본 fragment는 증가 순서이고 겹치거나 역행하지 않는다.
- 원본 전체 SHA와 fragment SHA를 모두 저장한다.
- 허용 유형: `ONE_TO_ONE`, `MERGED_SOURCE_HEADINGS`, `LOGICAL_REHEADING`, `MERGED_SOURCE_HEADINGS_WITH_LOGICAL_REHEADING`.
- 자동 정렬 실패·헤딩 오염·탭 삽입은 수동 override로 고정하고 근거 line을 남긴다.
- V1.2 parser는 선행 탭 대사 형식과 `E/F/N/L/NA/NAR` 전달 표기를 정규화한다.
- 동일 원문 line·character evidence를 서로 다른 논리 장면에 중복 귀속하지 않는다.

### 6.1 원문 물리 순서와 immutable scene ID 분리

`scene_no`는 Stage01 장면의 immutable identity이며 원문 물리 정렬 키가 아니다. 정렬기와 검증기는 다음 두 불변식을 분리하여 처리한다.

1. **identity invariant**
   - alignment의 `scene_no` 집합은 SceneCard의 `scene_no` 전집합과 정확히 일치한다.
   - scene_no 중복·누락·재발번은 0이어야 한다.
   - Stage01 레코드 순서와 값은 수정하지 않는다.

2. **source-order invariant**
   - SourceSceneAlignment JSONL의 직렬화 순서는 원문 `source_char_offsets.start` 오름차순이다.
   - 직렬화된 원문 구간은 증가·비중첩이어야 한다.
   - scene_no가 JSONL 안에서 비단조여도 원문 물리 순서가 정확하고 identity invariant를 만족하면 정상이다.

Stage01의 scene_no 순서와 원문 물리 순서가 다르면 다음을 적용한다.

- alignment 레코드는 원문 물리 순서로 저장한다.
- 각 레코드는 원래 scene_no를 그대로 보존한다.
- 차이를 `LOGICAL_REHEADING` 또는 `MERGED_SOURCE_HEADINGS_WITH_LOGICAL_REHEADING`, `VERIFIED_MANUAL_OVERRIDE`, `alignment_note`로 명시한다.
- validator는 `source offset 증가·비중첩`과 `scene_no 전집합 유일성`을 독립 검사한다.
- scene_no 오름차순을 맞추기 위해 무관한 후행 원문에 근거를 강제 귀속하는 행위를 금지한다.
- 정렬기는 scene_no를 source-order sorting key로 사용할 수 없다.

《궁》 EP02의 `30 → 42 → 43 → 44 → 31` 원문 순서 사례가 이 규칙의 기준 회귀 테스트다.

## 7. CastPresence 규칙

- `ONSCREEN`: 장면의 물리적 인물
- `VOICE_ONLY`: E/N/L 등 음성만 존재
- `PHONE_OR_REMOTE`: F 또는 전화·원격 발화
- `ARCHIVAL_OR_MEMORY`: 회상·사진·영상·CCTV·기억
- `REFERENCED_ONLY`: 대사에서 언급되지만 장면에 존재하지 않음
- presence 의미 판정은 원본에서만 한다. SceneCard·POV는 focality 순위의 보조 신호일 뿐 존재를 제조하지 않는다.
- 발화 여부와 focality를 독립 판정한다. `SPEAKING=PRIMARY` 같은 기계적 결합을 금지한다.
- 일반명사·행동문·장소명·문장 조각을 Entity로 생성하지 않는다.

## 8. 위험도 감사

후보 신호:

- `MAJOR/DOMINANT`인데 해당 회차 CharacterArc가 없음
- 여러 회차에서 `MINOR` 이상인데 시즌 CharacterArc가 희박함
- 반복적인 직접 상호작용이 있으나 RelationshipArc가 없음
- 기존 Arc trigger_scene_no에 당사자 CastPresence가 없음
- alias 분산으로 동일 인물이 여러 identity로 갈라짐
- 원본 물리 헤딩과 SceneCard 경계의 불일치
- 빈 출연 장면에 실제 화자·행동 인물이 존재함
- `REFERENCED_ONLY`, `VOICE_ONLY`, `PHONE_OR_REMOTE`, `ARCHIVAL_OR_MEMORY`가 문맥 없이 과다 생성됨

신호는 Arc가 아니다. 후보마다 원본을 직접 다시 읽어 실제 state delta 또는 relationship delta가 있을 때만 수용한다.

## 9. 선택 보강

- 기본 mode: `SELECTIVE_APPEND`
- 기존 bytes는 exact prefix로 보존한다.
- overwrite/delete는 0이어야 한다.
- Stage01·02·04는 변경하지 않는다.
- 새 레코드는 exact V10/V10.1 Stage03 schema를 따른다.
- 기각 후보도 사유를 ledger에 저장한다.
- EXT6 evidence 패키지와 의미 보강 레코드는 분리한다.
- 자동 CANONICAL 승격을 금지한다.

## 10. Functional Holdout

- 질문·정답은 후보 레코드에서 자동 생성하지 않는다.
- baseline 고정 이전에 독립적으로 core 질문을 설계한다.
- supplemental 질문은 원본 사건에서 독립 저작한다.
- core Recall@5는 하락할 수 없다.
- supplemental Recall@5는 개선되어야 한다.
- 비대상 파일 hash와 Fresh Extraction 재현성을 함께 검사한다.

## 11. Gold anchor 판정

《비밀의숲》은 16회·1,037장면 전체 정렬, unresolved 0, CastPresence 3,763, CharacterLoad 663, EntityBridge 139, 위험 후보 55 중 22건 선택 보강, core Recall@5 1.0 유지, supplemental Recall@5 0.0→1.0을 통과했다. 이 방법과 검증 순서를 전체 rollout의 기준으로 사용한다.

## 12. 완료·실패 판정

다음 조건을 모두 만족해야 완료다.

- 10개 필수 계층 존재
- exact schema 위반 0
- SceneCard/alignment 수 일치
- source offset 중첩·역행 0
- SceneCard scene_no 전집합과 alignment scene_no 전집합의 정확한 일치
- 원문 evidence mismatch·구간 밖 evidence 0
- 장면 간 동일 evidence 재사용 0
- alias 충돌·비인물 Entity 0
- unresolved 0 또는 원문상 정당한 empty로 명시
- RiskAudit 후보별 직접 판정과 SelectiveAppendLedger 존재
- core Recall@5 비하락, supplemental Recall@5 개선
- Stage01~04 및 baseline 파일 변경 0
- ZIP CRC와 Fresh Extraction PASS

하나라도 실패하면 `QUALITY_HOLD`이며 다음 작품으로 넘어가지 않는다.

## 13. 파일 명명과 교정

- 개별 패키지: `<작품명>_EXT6_APPEND_ONLY_EVIDENCE_FIXED_<YYYYMMDD>.zip`
- 통합 DB: `DB<전체작품수>_EXT6_<완료EXT6작품수>WORKS_WINDOWS_COMPATIBLE_FIXED_<YYYYMMDD>.zip`
- 같은 날짜의 교정은 버전을 올리지 않고 SHA256과 supersession ledger로 식별한다.
- 잘못된 산출물은 삭제·덮어쓰기 대신 revoked/superseded로 기록한다.

## 14. 새 세션 재개 규칙

새 대화 세션은 아래 순서로 문서를 읽은 뒤 바로 작업한다.

1. `EXT6_SINGLE_AUTHORITY_V1_2.md`
2. `EXT6_EXACT_SCHEMA_REGISTRY_V1_1.json`
3. `SECRET_FOREST_EXT6_GOLD_ANCHOR_V1_1.md`
4. `EXT6_FIXED_VERSION_CORRECTION_POLICY_20260730.md`
5. `EXT6_NEW_SESSION_HANDOFF.md`
6. `CURRENT_EXT6_POINTER.json`
7. `EXT6_ROLLOUT_STATUS.json`
8. `EXT6_ROLLOUT_QUEUE.json`

rolling handoff의 baseline DB, 현재 작품, 마지막 checkpoint를 확인하고 완료된 작업을 다시 생성하지 않는다. 새 세션에서도 이 문서의 방법을 재해석하거나 임의 버전을 만들지 않는다.

## 15. 큐 정책

`AUTHORED_WORK_INDEX_V23.json`의 순서를 고정한다. 작품 하나가 completion manifest, V1.2 전체 계층, Functional Holdout, Fresh Extraction PASS를 얻기 전 다음 작품을 완료 상태로 올리지 않는다.
