# 드라마 분석 권위 진입점

- Document status: `AUTHORITATIVE / V5 / CURRENT POLICY REVISION`
- Updated: `2026-07-18`
- 버전 정책: 문서·DB 릴리즈 번호를 자동 증가시키지 않는다.

이 디렉터리는 GPT·Claude 공동 한국 드라마 원본 직접독해, Stage01~04 저작, 정본 데이터, SourceLock, 최소 검증, DB 증분 편입의 단일 진입점이다.

---

## 1. 새 대화창 필수 로드

새 대화창은 다음만 읽고 즉시 실행한다.

1. `START_HERE_NEW_DRAMA_ANALYSIS.md`
2. `SCHEMA_CONTRACTS_V2.md`
3. 신규 작품 선정 시 최신 DB 작품 인덱스 1개
4. 중단 작업 재개 시 작품별 단일 `checkpoint.json`

압축 실행 요약이 필요하면 `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`를 사용한다.

과거 대화 전체, 모든 세션 README, 모든 방법론 문서를 시작 전에 전수 조사하지 않는다.

---

## 2. 현재 권위 우선순위

1. `SCHEMA_CONTRACTS_V2.md` — exact keyset·enum·ID·FK
2. `START_HERE_NEW_DRAMA_ANALYSIS.md` — 현재 실행·검증·릴리즈 정책
3. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md` — 즉시 실행 요약
4. `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json` — machine-readable 정책
5. 작품별 SourceLock·checkpoint
6. 과거 detailed playbook·incident 문서

과거 문서가 QuarterAudit, 블록 강검사, 반복 validator, 매 작품 새 DB 릴리즈를 기본 의무로 요구하면 현재 START_HERE 정책이 우선한다.

---

## 3. 본 작업

```text
원본 대본 직접독해
→ 회차별 Stage01~03 직접 저작
→ 정본 파일 저장
→ 최소 구조검사
→ 단일 checkpoint
→ 다음 회차
→ 전 시즌 완료 후 Stage04
→ 작품 완료검사·작품 ZIP Fresh Extraction 1회
→ 정본 DB 증분 편입
```

- Python·템플릿 의미 생성 금지
- 여러 회차 동시 의미 생성 금지
- 파일이 없으면 완료 보고 금지
- 검증은 직접독해를 대신하지 않음

---

## 4. 회차 표준 파이프라인

```text
EP01 Q1→Q4 직접독해
→ SceneCard / EpisodeMeta
→ SequenceBlueprint / EpisodeArc
→ CharacterArc / RelationshipArc
→ LocalEdge / PayoffCandidate
→ 정본 저장
→ 최소 구조검사
→ checkpoint next 갱신
→ EP02
```

Q1~Q4는 독해 분할 단위이며 Quarter별 상세 감사 파일은 기본적으로 만들지 않는다.

---

## 5. 최소 검증 정책

### 회차

한 번만 확인한다.

- parse·exact keyset·자료형
- ID 중복
- SceneCard coverage
- Sequence partition·span·budget·runtime
- Arc·Edge 참조
- LocalEdge same episode/gap 0
- 필수 파일 존재

결과는 작품별 단일 checkpoint에 기록한다.

### 작품 완료 후

한 번만 확인한다.

- 전 회차 Stage01~03 존재
- CandidateDisposition 100%
- CrossEpisodeEdge·FullSeriesArc 무결성
- 작품 ZIP
- 작품 ZIP Fresh Extraction 1회

### 조건부 포렌식

다음 상황에서만 구형 강검사·QuarterAudit·반복 분석 검사를 사용한다.

- 원본 불일치
- 직접독해 누락 또는 자동 생성 의심
- 대량 템플릿 반복
- LocalEdge 과밀·자동 연결
- Provider 충돌
- SourceLock 해시 불일치
- 정본 교체·스키마 마이그레이션
- 사용자 요청

---

## 6. 기본에서 제거된 운영 과부하

- Quarter마다 상세 감사 파일
- 회차마다 다수의 증빙 JSON
- 여러 종류의 checkpoint
- 반복 checksum
- 전반부·8회차 의무 강검사
- 작품별·블록별·전 시즌별 중복 validator
- 여러 단계 ZIP 전후 검증
- 동일 정보의 validation registry 중복 기록
- 작품 한 편마다 전체 DB 새 릴리즈 생성

이 항목은 폐기된 것이 아니라 사고 대응용으로 보존한다.

---

## 7. GPT·Claude 공동 규격

공통:

- 원본 직접독해
- 회차 순차 처리
- exact Stage01~04 schema
- 동일 ID·enum·FK
- LocalEdge 동일 회차
- PayoffCandidate disposition 100%
- SourceLock Core
- 단일 checkpoint
- Provider provenance

Claude의 의미 밀도·앙상블 독해와 GPT의 구조화·계보 관리 장점을 결합한다. 어느 Provider도 자동 상위 권위를 갖지 않는다. 사용자 승인으로 공동 `CANONICAL`이 된다.

---

## 8. Stage03~04 선택성

- 실제 변화가 있는 인물·관계만 Arc로 기록
- LocalEdge는 반사실 인과를 통과한 동일 회차 연결만 허용
- 번호 인접성·같은 시퀀스·유사 감정은 인과 근거가 아님
- 회차 간 연결은 Stage04 CrossEpisodeEdge에서만 확정
- 모든 PayoffCandidate를 개별 disposition
- 자동 회차 경계 브리지 금지
- 고정 Arc·Edge·Candidate 수량 금지

---

## 9. SourceLock

작품당 SourceLock Core 한 파일을 유지한다.

필수:

- 작품·회차·원본 archive SHA
- 인코딩·번호·장면 경계 정책
- 회차별 원본 파일 SHA·canonical 장면 수
- direct reading attestation
- provider·model·run ID
- 완료 회차와 next pointer

장면별 해시와 Quarter별 증빙은 문제 작품에만 확장한다.

---

## 10. DB 편입과 릴리즈 동결

- 신규 작품만 증분 편입한다.
- 기존 정본 전 작품을 매번 재검증하지 않는다.
- 작품 완료와 전체 DB 릴리즈 생성을 분리한다.
- 전체 DB ZIP·새 Governance 번호·새 release manifest는 사용자가 명시적으로 요청할 때만 만든다.
- 문서 수정, validator 수정, 작품 한 편 추가만으로 릴리즈 번호를 올리지 않는다.
- 최신 인증 DB 릴리즈는 사용자 승인 전까지 동결한다.

---

## 11. EXT6

```text
DEFAULT: EXT6_DISABLED
```

EXT6는 사용자의 명시적 지시, 교차비교, 연구 코퍼스 구축 등 별도 작업에서만 적용한다. EXT6 미적용은 Stage01~04 불완전이 아니다.

---

## 12. 개발자 보고

사용자가 중간 보고를 요구하지 않으면 최소 보고만 한다.

```text
작품
완료 회차
현재 pointer
저장 Stage
구조검사 상태
차단 오류
```

실제 저장되지 않은 진행을 완료 또는 진행 중으로 보고하지 않는다.

---

## 13. 주요 문서

| 영역 | 문서 |
|---|---|
| 새 대화창 전체 온보딩 | `START_HERE_NEW_DRAMA_ANALYSIS.md` |
| 압축 실행 순서 | `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md` |
| exact schema | `SCHEMA_CONTRACTS_V2.md` |
| 기계 판독 정책 | `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json` |
| 상세 신규 작품 사례 | `DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V2.md` |
| Claude 장점 참고 | `DRAMA_CLAUDE_STAGE03_04_STRENGTH_ADOPTION_POLICY_V1.md` |
| 과거 사고·감사 | 필요할 때만 해당 incident 문서 |

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 artifact name, SHA256, counts, lineage, handoff만 기록한다.
