# 드라마 분석 검증 간소화·릴리즈 동결 결정 기록

- 상태: `AUTHORITATIVE DECISION RECORD`
- 결정일: `2026-07-18`
- 적용: GPT·Claude 공동 드라마 분석
- DB 릴리즈 증가: 없음

---

## 1. 결정 배경

현재 드라마 분석 검증 체계의 상당 부분은 정상적인 창작 분석 요구에서 처음부터 설계된 것이 아니라, GPT 작업에서 다음 문제가 반복된 뒤 사후적으로 추가되었다.

- 대본을 직접 독해하지 않고 분석했다고 보고
- Stage01 일부만 존재하는데 Stage01~03 또는 전반부 완료로 보고
- 파일 저장 전 진행 상태를 과장
- 구조 PASS를 의미 품질 완료로 오인
- 세션 중단 후 완료 위치와 원본 계보 상실
- LocalEdge 자동·과밀 생성
- 미처리 PayoffCandidate를 남긴 채 Stage04 완료 선언
- ZIP·DB 편입 과정에서 파일·해시·상태 문서 드리프트

이 사고를 방지하기 위해 QuarterAudit, 블록 강검사, 다중 checkpoint, 반복 checksum, 여러 validator와 Fresh Extraction 단계가 누적되었다.

각 안전장치는 개별 사고에는 유효했으나, 모든 정상 작품에 의무 적용하면서 다음 역효과가 발생했다.

```text
직접독해·의미 저작보다 검증·증빙·패키징 비용이 커짐
→ 세션 및 실행 한도 소진
→ 분석 중단·새 대화창 이동 증가
→ 재학습·재검증 반복
→ 다시 오류 가능성 증가
```

따라서 검증 체계를 의미 저작의 필수 본체와 사고 대응용 포렌식으로 분리한다.

---

## 2. 최종 결정

### 2.1 유지하는 본체

- 원본 직접독해
- 회차 순차 처리
- Stage01~04 exact schema
- SceneCard와 Sequence의 장면 coverage
- ID·FK·enum 무결성
- 실제 변화만 CharacterArc·RelationshipArc로 기록
- LocalEdge 동일 회차·반사실 인과
- 모든 PayoffCandidate disposition
- SourceLock Core
- 작품별 단일 checkpoint
- 작품 완료 후 작품 ZIP Fresh Extraction 1회
- Provider provenance
- 사용자 승인에 의한 CANONICAL

### 2.2 기본 절차에서 제거하는 항목

- Q1~Q4마다 QuarterAudit JSON 생성
- 회차별 다수의 증빙 JSON
- 여러 checkpoint 형식
- 같은 내용을 반복하는 checksum
- 약 8회차마다 의무적인 구조·의미 강검사
- 회차·블록·전 시즌에서 중복 실행하는 validator
- 회차별 ZIP과 Fresh Extraction
- 동일 결과를 복제하는 validation registry
- 신규 작품마다 기존 DB 전체 재검증
- 작품 하나가 완료될 때마다 새 전체 DB 릴리즈 생성

### 2.3 조건부 포렌식으로 이동하는 항목

다음 상황에서만 구형 강검사 도구를 사용한다.

- 원본과 산출물의 의미 불일치
- 직접독해 누락 또는 자동 의미 생성 의심
- 동일 문장 골격 대량 반복
- LocalEdge 과밀·인접 자동 연결 의심
- GPT·Claude 동일 작품 결과 충돌
- SourceLock 해시 불일치
- 정본 교체
- 스키마 마이그레이션
- 사용자 명시 요청

---

## 3. 새 기본 실행

```text
Q1→Q4 원본 직접독해
→ 해당 회차 Stage01~03 직접 저작
→ 정본 파일 저장
→ 최소 구조검사 1회
→ 단일 checkpoint 갱신
→ 다음 회차
```

전 시즌 완료 후:

```text
모든 PayoffCandidate 검토
→ CandidateDisposition 100%
→ 실제 CrossEpisodeEdge 확정
→ FullSeriesArc
→ 작품 완료검사 1회
→ 작품 ZIP
→ Fresh Extraction 1회
→ 정본 DB 증분 편입
```

---

## 4. 검증의 역할 재정의

검증은 다음만 증명한다.

- 파일이 파싱되는가
- exact schema를 지키는가
- 장면·시퀀스 누락과 중복이 없는가
- 참조가 유효한가
- LocalEdge가 같은 회차인가
- 모든 후보가 처분되었는가
- 작품 패키지를 실제로 해제할 수 있는가

검증이 다음을 대신하지 않는다.

- 원본 직접독해
- 장면 의미 해석
- 인물 선택 해석
- 관계 변화 저작
- 인과 판단
- 장거리 plant/payoff 판단

---

## 5. SourceLock 결정

SourceLock은 폐기하지 않는다. 원본과 산출물의 계보를 보존하는 최소 안전장치이기 때문이다.

다만 작품당 SourceLock Core 한 파일만 기본으로 유지한다.

기본:

- 작품·회차
- 원본 archive와 회차 파일 SHA
- 인코딩
- 장면 번호·경계 정책
- canonical 장면 수
- direct reading attestation
- provider·model·run ID
- 완료 회차·next pointer

조건부 확장:

- 장면별 hash
- Quarter별 hash
- 원문 offset
- 판본 정렬표
- 상세 직접독해 증빙

---

## 6. GPT·Claude 공동 규격 결정

GPT와 Claude는 같은 최종 스키마와 DB 계약을 사용한다.

통일:

- Stage01~04 exact keyset
- ID·enum·FK
- SourceLock Core
- 단일 checkpoint
- LocalEdge·CrossEpisodeEdge 구분
- CandidateDisposition
- 정본 상태
- Provider provenance

통일하지 않음:

- 내부 프롬프트
- 독해 메모 형식
- 세션 분할 방식
- Provider 고유 보조 분석
- 문장 표현 스타일

Claude의 직접독해·의미 밀도·앙상블 장점과 GPT의 구조화·계보 관리 장점을 공동 정본에 보존한다.

---

## 7. EXT6 결정

EXT6는 분석 가치가 있으나 기본 Stage01~04와 동시 적용하면 소요가 과도하다.

```text
EXT6_DISABLED_BY_DEFAULT
```

다음 경우에만 실행한다.

- 사용자 명시 지시
- GPT×Claude 동일 작품 교차비교
- 연구용 고밀도 코퍼스
- 별도 실행 예산 확보

---

## 8. 릴리즈 동결 결정

- 작품 완료와 전체 DB 릴리즈 생성을 분리한다.
- 신규 작품은 작업 tree 또는 정본 DB에 증분 편입할 수 있다.
- 전체 DB ZIP, 새 Governance 번호, 새 release manifest는 사용자 명시 지시가 있을 때만 생성한다.
- 문서 변경으로 릴리즈를 올리지 않는다.
- validator 변경으로 릴리즈를 올리지 않는다.
- 작품 한 편 추가만으로 릴리즈를 올리지 않는다.
- 최신 인증 DB 릴리즈는 사용자의 다음 승인 전까지 동결한다.

---

## 9. 재발 방지

새 대화창 또는 새 모델은 다음 행동을 하지 않는다.

- 품질을 높인다는 이유로 기본 검증 단계를 임의 추가
- 과거 incident 규칙을 정상 작품의 의무로 복원
- 새 문서 버전·DB 릴리즈를 습관적으로 증가
- 직접독해 부족을 validator 수 증가로 보완
- 실제 파일 없이 진행·완료 보고

검증 규칙을 다시 기본 의무로 추가하려면 다음을 먼저 제시해야 한다.

1. 실제 발생한 사고
2. 기존 최소검사로 막을 수 없는 이유
3. 추가 비용과 실행 한도 영향
4. 조건부 포렌식으로 해결할 수 없는 이유
5. 사용자 승인

---

## 10. 현재 권위 연결

- 상세 실행: `START_HERE_NEW_DRAMA_ANALYSIS.md`
- 압축 실행: `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`
- exact schema: `SCHEMA_CONTRACTS_V2.md`
- machine policy: `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json`
- 권위 순서: `DRAMA_ANALYSIS_AUTHORITY_INDEX_V5.md`

이 결정 기록은 과거 validator와 incident 문서를 삭제하지 않는다. 다만 해당 문서의 무거운 절차를 일반 작품의 기본 실행 권위에서 제외한다.
