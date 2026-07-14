# 드라마 분석 권위 인덱스

Document status: **AUTHORITATIVE ENTRYPOINT / V3 CANDIDATE BRANCH**  
Version: 3.0-candidate  
Updated: 2026-07-15 (Asia/Seoul)

이 디렉터리는 한국 드라마 원본을 직접 읽고 Stage01~04 분석 산출물을 만들며, 검증된 결과를 `seqcard_ko` 데이터베이스에 삽입하는 데 필요한 권위 문서군의 단일 진입점이다.

## 1. 현재 권위 우선순위

1. `SCHEMA_CONTRACTS_V2.md` — Stage01~04 exact schema·enum·ID·FK·불변식
2. `DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md` — 현재 작업 단위·8회차 블록·DB 삽입·EXT6 보류
3. `DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md` — 직접독해·내용 깊이·Stage별 저작 방식
4. `DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md` — fail-closed 강검증
5. `DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md` — SourceLock·계보·ZIP·허브 편입
6. `DRAMA_SESSION_EXECUTION_SAFETY_V1.md` — 세션 한도·원자 체크포인트·중단 복구
7. `EXT6_DEFERRED_SIDECAR_POLICY_V1.md` — EXT6 별도 보류 정책
8. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json` — 현재 데이터베이스·완료/잔여 작품
9. 최신 `docs/sessions/*drama*/README.md` — 작업 이력과 다음 진입점

과거 `docs/external/claude_drama_analysis_method_manual_stage01_04_v1.md`는 중요한 원형·역사 문서다. 최신 권위 문서와 충돌하면 위 순서를 적용한다.

## 2. 핵심 결정

```text
Stage01~04 exact schema: 기존 v2 유지
v3: 직접독해·내용 깊이·검증·세션 안전 강화
EXT6: 기존 Stage를 수정하지 않는 sidecar, 현재 기본 보류
품질 비교: 기존 작품과의 교차비교는 기본 필수 아님
Stage04: 전 작품 Stage01~03 강검증 후 수행
CANONICAL: 사용자 승인 후에만 가능
```

## 3. 현재 데이터베이스 상태

```text
작품: 49
회차: 938
SceneCard: 58,945
Stage01~04 완료: 34
업그레이드 잔여: 15
```

최신 개발자 데이터베이스:

```text
seqcard_ko_stage04_progress_W_dream_gangnam_gyeongseong_misa_milhwe_v1.zip
SHA256 fbcff3f8d184d4d36a4364fe8caca14b3591ae0c8b64b07ebccfaf2564b3ad6c
```

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 파일명·SHA·count·validation·lineage만 기록한다.

## 4. 최신 실행 단위

```text
의미 저작: quarter
원자 잠금: episode
개발자 전달 블록: 8 episodes
전 작품 중간 게이트: full Stage01~03
Stage04: full-series fan-in
최종 통합: independent work ZIP + seqcard_ko DB ZIP
```

내부 순서:

```text
EP01 Q1→Q2→Q3→Q4→Stage02→Stage03→회차 게이트→체크포인트
→ EP02 ...
→ EP08 ...
→ 8회차 블록 통합 게이트
→ 다음 블록
→ 전 작품 Stage01~03 강검증
→ Stage04
→ DB 삽입
```

한 실행에서 여러 회차를 의미 생성하지 않는다.

## 5. 절대 금지

- Python·템플릿으로 의미 필드 생성
- 키워드 조각·참조 표식·반복 골격
- 회차 요약을 CharacterArc/RelationshipArc에 복사
- LocalEdge에 회차 간 연결 저장
- 전 회차 Stage01~03 검증 전 Stage04 확정
- 이전 화 마지막 → 다음 화 첫 장면 자동 브리지
- 후보 일괄 disposition·동일 review 문장 복사
- 실제 데이터를 검사하지 않는 stub validator
- report PASS로 data FAIL을 덮기
- 사용자 승인 없이 `CANONICAL`

## 6. Source와 데이터베이스 경계

로컬/개발자용 `seqcard_ko` 데이터베이스에는 사용자가 제공한 원본을 다음 경로로 해제·정규화할 수 있다.

```text
seqcard_ko/original_extracted/<work>/<work>_<NN>.txt
```

GitHub 허브에는 raw source를 커밋하지 않는다. SourceLock·SHA·scene count·alignment·validation만 기록한다.

## 7. EXT6

EXT6은 현재 `DEFERRED_OPTIONAL_SIDECAR`다.

- 신규 분석·업그레이드 기본 범위에서 제외
- Stage01~04 완료 판정과 무관
- 기존 파일럿·계약은 별도 보존
- 명시적 승인과 1회차 독립 파일럿 후에만 재검토

자세한 규칙은 `EXT6_DEFERRED_SIDECAR_POLICY_V1.md`를 따른다.

## 8. 새 세션 5분 시작 절차

```text
1. 이 README 읽기
2. DRAMA_ANALYSIS_AUTHORITY_INDEX_V3.md 읽기
3. SCHEMA_CONTRACTS_V2.md exact keyset 로드
4. DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md 읽기
5. DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json 읽기
6. 완료 작품 제외·작품 1편 선정
7. 원본 inventory·SourceLock v2
8. 8회차 블록 계획
9. EP01 Q1 직접독해
```

## 9. 최소 개발자 보고

```text
작품 / 범위 / 각 계층 레코드 수
최종 gate / errors / warnings
독립 작품 ZIP SHA256
갱신된 전체 DB ZIP SHA256
현재 완료작·잔여작 수
다음 진입점
```

상세 판단·보강·교정은 패키지의 report·ledger·validation에 기록한다.
