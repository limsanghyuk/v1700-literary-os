# 드라마 분석 권위 인덱스 v5

- Status: `AUTHORITATIVE / CURRENT POLICY REVISION`
- Updated: `2026-07-18`
- Version note: 운영 정책 갱신으로 문서·DB 릴리즈 번호를 증가시키지 않는다.

---

## 1. 새 대화창 필수 로드

1. `START_HERE_NEW_DRAMA_ANALYSIS.md`
2. `SCHEMA_CONTRACTS_V2.md`

신규 작품 선정 시 최신 DB 작품 인덱스 하나를 추가한다. 중단 재개 시 작품별 단일 checkpoint 하나만 추가한다.

압축 실행 순서가 필요하면 `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`를 사용한다.

---

## 2. 권위 우선순위

| 순위 | 영역 | 권위 문서 |
|---:|---|---|
| 1 | exact keyset·enum·ID·FK | `SCHEMA_CONTRACTS_V2.md` |
| 2 | 현재 실행·검증·릴리즈 정책 | `START_HERE_NEW_DRAMA_ANALYSIS.md` |
| 3 | 새 대화창 압축 실행 순서 | `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md` |
| 4 | 기계 판독 정책 | `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json` |
| 5 | 작품별 실행 상태 | SourceLock Core·단일 checkpoint |
| 6 | 과거 상세 저작 사례 | `DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V2.md` |
| 7 | Claude 장점 참고 | `DRAMA_CLAUDE_STAGE03_04_STRENGTH_ADOPTION_POLICY_V1.md` |
| 8 | 과거 사고·포렌식 | 관련 incident·audit 문서 |

과거 상세 문서가 QuarterAudit, 약 8회차 강검사, 반복 validator, 매 작품 새 DB 릴리즈를 기본 의무로 요구하면 현재 START_HERE 정책이 우선한다.

---

## 3. 현재 실행 권위

```text
원본 직접독해
→ 회차별 Stage01~03 직접 저작
→ 정본 저장
→ 최소 구조검사 1회
→ 단일 checkpoint
→ 다음 회차
→ 전 시즌 Stage04
→ 작품 완료검사
→ 작품 ZIP Fresh Extraction 1회
→ DB 증분 편입
```

검증은 직접독해를 대신하지 않는다. Python·템플릿 의미 생성과 여러 회차 동시 의미 생성은 금지한다.

---

## 4. 기본 검증

### 회차

- parse·exact keyset·type
- ID 중복
- SceneCard coverage
- Sequence partition·span·budget·runtime
- Arc·Edge reference
- LocalEdge same episode/gap 0
- 필수 파일 존재

결과는 작품별 단일 checkpoint에 기록한다.

### 작품 완료

- 전 회차 Stage01~03 존재
- CandidateDisposition 100%
- CrossEpisodeEdge·FullSeriesArc 무결성
- 작품 ZIP
- 작품 ZIP Fresh Extraction 1회

---

## 5. 기본 절차에서 제외

다음은 일반 작품의 기본 의무가 아니다.

- Q별 QuarterAudit
- 회차별 다수 검증 JSON
- 여러 checkpoint
- 반복 checksum
- 전반부·약 8회차 강경검사
- 회차·블록·전 시즌 중복 validator
- 회차별 ZIP·Fresh Extraction
- 중복 validation registry
- 작품마다 전체 DB 새 릴리즈

원본 불일치, 직접독해 누락 의심, 대량 템플릿 반복, LocalEdge 과밀, Provider 충돌, SourceLock 불일치, 정본 교체, 사용자 요청 시에만 포렌식으로 실행한다.

---

## 6. GPT·Claude 공동 정본

GPT와 Claude는 동일한 공통 정본 규격을 사용한다.

공통 의무:

- 원본 직접독해
- 회차 순차 처리
- exact Stage01~04 schema
- 동일 ID·enum·FK
- LocalEdge 동일 회차
- CandidateDisposition 100%
- SourceLock Core
- 단일 checkpoint
- Provider provenance

Claude의 의미 밀도·앙상블 분석과 GPT의 구조화·계보 관리 장점을 결합한다. 어느 Provider도 자동 상위가 아니며 사용자 승인 후 공동 `CANONICAL`이 된다.

---

## 7. SourceLock 권위

기본은 작품당 SourceLock Core 한 파일이다.

- 원본 archive·회차 파일 SHA
- 인코딩·번호·장면 경계 정책
- 회차별 canonical 장면 수
- direct reading attestation
- provider·model·run ID
- completed episodes·next pointer

장면별·Quarter별 상세 해시는 사고가 있는 작품만 확장한다.

---

## 8. DB 및 릴리즈 권위

- 신규 작품만 증분 편입한다.
- 기존 정본 전 작품을 매번 다시 의미검사하지 않는다.
- 작품 완료와 전체 DB 릴리즈 생성을 분리한다.
- 새 Governance 번호·전체 DB ZIP·release manifest는 사용자의 명시적 지시가 있을 때만 생성한다.
- 문서 변경, validator 변경, 신규 작품 추가만으로 릴리즈 번호를 올리지 않는다.
- 최신 인증 DB 릴리즈는 사용자 승인 전까지 동결한다.

---

## 9. EXT6

`EXT6_DISABLED_BY_DEFAULT`.

사용자의 명시적 요청, GPT×Claude 교차비교, 연구용 고밀도 코퍼스 구축에서만 별도 실행한다. EXT6 미적용은 Stage01~04 불완전이 아니다.

---

## 10. 개발자 보고

중간 보고는 사용자가 요구할 때만 최소 형식으로 한다.

```text
작품 / 완료 회차 / current pointer / 저장 Stage / 구조검사 / 차단 오류
```

실제 저장되지 않은 진행은 보고하지 않는다.

---

## 11. 문서 로드 제한

과거 대화 전체, 모든 세션 README, 모든 방법론 문서를 시작 전에 전수 조사하지 않는다. 충돌·품질 사고·계약 변경이 발생했을 때만 관련 전문 문서를 부분 조회한다.
