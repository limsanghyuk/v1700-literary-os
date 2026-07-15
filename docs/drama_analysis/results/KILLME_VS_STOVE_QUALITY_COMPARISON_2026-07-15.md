# 킬미힐미·스토브리그 SeqCard 분석 품질 비교

- Document ID: `KILLME-VS-STOVE-QUALITY-COMPARISON-2026-07-15`
- Date: 2026-07-15
- Status: `EVIDENCE_BACKED_COMPARISON`
- Scope: Stage01~04 분석 품질, 현행 계약 적합성, 정본 편입 준비도
- Promotion claim: 없음
- Raw script/dialogue export: 없음

## 1. 결론

현행 Stage01~04 운영 규격과 재현 가능한 검증 증빙을 기준으로 하면 **킬미힐미가 더 우수하다**.

```text
킬미힐미 = PREFERRED_CURRENT_REFERENCE / PASS_CANDIDATE
스토브리그 = SEMANTICALLY_USEFUL / REWORK_REQUIRED
```

스토브리그의 내용 분석이 낮다는 뜻은 아니다. 스토브리그는 인물·관계망의 폭이 더 넓고 Stage01·02도 실사용 가능하다. 차이는 최신 Stage03·04 계약, SourceLock, 후보 전수 처분, 강검증 증빙에서 발생한다.

패키지의 `WORK_STAGE04_UPGRADE_STATUS.json`은 두 작품을 모두 `STAGE01_04_COMPLETE`로 기록한다. 이 상태는 파일 존재 중심의 구조 완료로 해석해야 한다. 현행 규범의 fail-closed 검증을 적용하면 두 작품의 정본 편입 준비도는 같지 않다.

## 2. 권위 기준

이번 비교는 다음 허브 문서를 우선 적용했다.

1. `docs/drama_analysis/SCHEMA_CONTRACTS_V2.md`
2. `docs/drama_analysis/DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md`
3. `docs/drama_analysis/DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md`
4. `docs/drama_analysis/DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md`
5. `docs/drama_analysis/DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md`

핵심 적용 규칙:

- Stage02 모든 장면 coverage·partition·count 검증
- LocalEdge는 동일 회차, `gap_episodes == 0`, 구체적 인과만 허용
- 회차를 넘는 연결은 Stage04 CrossEpisodeEdge에서만 관리
- PayoffCandidate는 Stage04에서 100% disposition
- SourceLock과 실제 데이터 검증이 없으면 완료·승격 주장 금지
- 정확 중복뿐 아니라 기계적 인접 연결과 반복 골격도 반게이밍 검사

## 3. 입력과 검사 범위

입력 패키지:

```text
seqcard_ko_stage04_progress_W_dream_gangnam_gyeongseong_misa_milhwe_theking_newheart_killme_whitetower_mawang_skycastle_gung_v1.zip
SHA256 79f639c8de72a8319cd183459c52c872b7987e8f0f4ba580bdc7337c8dad2972
```

검사 범위:

- Stage01: SceneCard
- Stage02: SequenceBlueprint, EpisodeArc
- Stage03: CharacterArc, RelationshipArc, LocalEdge, PayoffCandidate
- Stage04: CrossEpisodeEdge, FullSeriesArc, CandidateDisposition
- SourceLock, validation, normalization/repair/disposition ledger 존재 여부
- ID·FK·scene reference·coverage·partition·중복·텍스트 다양성

검사하지 않거나 허브에 싣지 않은 것:

- 원문 대본·대사
- `original_extracted` 내용
- 개별 SceneCard·Arc·Edge 원문 레코드
- 임베딩·벡터·API 키·모델 가중치

## 4. 전수 계량 결과

| 항목 | 킬미힐미 | 스토브리그 | 해석 |
|---|---:|---:|---|
| 회차 | 20 | 16 | 회차 수가 달라 비율 병행 |
| SceneCard | 1,285 | 1,003 | 전 회차 존재 |
| SequenceBlueprint | 193 | 155 | 전 회차 존재 |
| 시퀀스/씬 비율 | 0.1502 | 0.1545 | 둘 다 권장 0.12~0.17 |
| 장면 coverage 누락 | 0 | 0 | 둘 다 통과 |
| 장면 중복 소속 | 0 | 0 | 둘 다 통과 |
| CharacterArc/회 | 3.00 | 6.00 | 스토브리그 폭 우세 |
| RelationshipArc/회 | 2.00 | 4.69 | 스토브리그 폭 우세 |
| 서로 다른 인물 | 9 | 26 | 장르 차이 포함 |
| 서로 다른 관계쌍 | 9 | 38 | 스토브리그 앙상블 우세 |
| LocalEdge/회 | 2.00 | 44.38 | 스토브리그 과밀 |
| 바로 다음 장면 LocalEdge | 10.0% | 70.0% | 스토브리그 인접 연결 편향 |
| LocalEdge 속 회차 간 브리지 | 0 | 16 | 스토브리그 현행 규격 위반 |
| episode-qualified work_id 불일치 | 0 | 964 | 스토브리그 Stage03 정규화 필요 |
| PayoffCandidate | 60 | 83 | 스토브리그 후보량 우세 |
| CandidateDisposition | 60 | 0 | 킬미힐미만 전수 처분 |
| 미처리 후보 | 0 | 83 | 스토브리그 Stage04 차단 |
| CrossEpisodeEdge | 56 | 10 | 킬미힐미 fan-in 증빙 우세 |
| 잘못된 CrossEpisodeEdge 참조 | 0 | 0 | 둘 다 통과 |
| 중복 ID | 0 | 0 | 둘 다 통과 |
| FullSeriesArc 키/채움 | 17/100% | 17/100% | 둘 다 구조 완료 |
| SourceLock v2 | 있음 | 없음 | 킬미힐미 우세 |
| 작품별 강검증 | 있음 | 없음 | 킬미힐미 우세 |
| 정규화·수리·처분 ledger | 있음 | 없음 | 킬미힐미 우세 |

## 5. Stage별 의미 품질

### 5.1 Stage01

두 작품 모두 사용할 수 있다.

- 킬미힐미 title 고유율: 100.0%
- 킬미힐미 intent_gist 고유율: 100.0%
- 스토브리그 title 고유율: 99.7%
- 스토브리그 intent_gist 고유율: 99.9%

표본 직접검토에서 킬미힐미는 장면의 심리 변화, 인과, 후속 기능을 더 상세히 기록했다. 스토브리그는 사건·전략을 더 짧고 실무적으로 요약한다. 길이는 단독 품질 기준이 아니므로 고유율·원인/결과 구분·후속 계층 일관성과 함께 판단했다.

킬미힐미의 일부 `core2 == null`은 스키마가 허용하므로 결함으로 계산하지 않았다.

스토브리그의 원본은 명시적 장면 마커가 약한 계열로 기록되어 있는데 SourceLock v2가 없다. 따라서 Stage01 내용은 유용하지만 장면 경계와 ordinal을 동일하게 재현할 증빙은 부족하다.

### 5.2 Stage02

구조 품질은 사실상 동급이다.

- coverage 오류 0
- partition 오류 0
- scene overlap 0
- 시퀀스 밀도 둘 다 권장 범위
- SequenceBlueprint keyset 단일
- EpisodeArc keyset 단일

킬미힐미의 goal·obstacle·episode function은 평균적으로 더 길고 심리·인과 설명이 풍부하다. 스토브리그는 더 간결하지만 목표와 장애가 분리되어 있다. 이 차이는 문체·장르 차이를 포함하므로 Stage02 승패의 결정 근거로 사용하지 않았다.

### 5.3 Stage03

내용 폭은 스토브리그가 우수하다.

```text
스토브리그: 26 characters / 38 relationship pairs
킬미힐미: 9 characters / 9 relationship pairs
```

조직극·앙상블 검색에서는 스토브리그가 더 풍부한 검색 기질을 제공한다.

그러나 현행 계약 적합성과 인과 엣지 선별은 킬미힐미가 우수하다.

- 스토브리그 LocalEdge 710건 중 70%가 바로 다음 장면 연결이다.
- 회차 간 브리지 16건이 LocalEdge 파일에 남아 있다.
- CharacterArc·RelationshipArc·LocalEdge·PayoffCandidate 합계 964건이 bare work_id를 쓴다.
- 킬미힐미는 해당 오류가 모두 0이다.

스토브리그의 LocalEdge note는 고유하므로 단순 문장 복사는 아니다. 문제는 **고유한 문장으로 기계적 인접 연결을 너무 많이 서술한 것**이다. 이는 텍스트 중복 검사만으로 잡히지 않는 구조적 반게이밍 문제다.

### 5.4 Stage04

킬미힐미의 우위가 결정적이다.

킬미힐미 후보 60건의 disposition:

```text
PROMOTED_CROSS_EDGE: 56
RECLASSIFIED_LOCAL_OR_ADJACENT_CAUSAL: 1
RESOLVED_WITHIN_EPISODE: 3
unresolved: 0
```

스토브리그:

```text
PayoffCandidate: 83
CandidateDisposition: 0
CrossEpisodeEdge: 10
unresolved under current evidence contract: 83
```

스토브리그의 CrossEpisodeEdge 10건은 참조·gap 산술이 정상이고 내용도 장거리 연결을 설명한다. 그러나 후보 83건 전체에 대한 승격·기각·회차 내 해소 이력이 없으므로 Stage04 전수 fan-in 완료를 증명하지 못한다.

## 6. 검증·계보 품질

킬미힐미에 존재하는 증빙:

- `source_lock/킬미힐미_SOURCE_LOCK_V2.json`
- `validation/킬미힐미_strong_validation.json`
- `upgrade_audit/킬미힐미/upgrade_summary.json`
- `candidate_disposition_ledger.jsonl`
- `stage02_normalization_ledger.json`
- `deterministic_repair_ledger.json`

강검증 결과에는 errors 0, warnings 0, source alignment 20/20 episodes, auto boundary bridge 0이 기록되어 있다.

스토브리그는 Stage01~04 파일이 모두 존재하지만 같은 수준의 작품별 SourceLock·강검증·수리·처분 묶음이 패키지에 없다. 따라서 의미 데이터는 보존하되 현재 상태에서 `CANONICAL` 또는 최신 `PASS_CANDIDATE`로 승격하면 안 된다.

## 7. 스토브리그 보강 계약

1. 16화 SourceLock v2를 생성하고 장면 경계·ordinal·hash를 잠근다.
2. Stage03 bare work_id 964건을 episode-qualified 형식으로 정규화한다.
3. LocalEdge 속 회차 간 브리지 16건을 제거하거나 CrossEpisodeEdge로 이동한다.
4. LocalEdge 710건을 원 장면과 대조해 단순 인접·순서 연결을 제거한다.
5. PayoffCandidate 83건을 전부 disposition한다.
6. CrossEpisodeEdge와 FullSeriesArc를 재종합한다.
7. 현행 강검증과 반게이밍 검증에서 errors 0을 확인한다.
8. 기존 판본과 보강 판본의 lineage·supersession을 기록한다.

보강 시 Stage01·02와 가치 있는 CharacterArc·RelationshipArc는 우선 보존하고, 의미가 바뀌는 자동 일괄변환은 금지한다.

## 8. 사용 결정

### 즉시 사용 가능

- 킬미힐미: 현행 Stage01~04 비교 기준·검색 기질·설계 참고용
- 스토브리그 Stage01·02: 장면·시퀀스 초안 및 내부 검색용
- 스토브리그 CharacterArc·RelationshipArc: 앙상블 분석 참고용, work_id 정규화 전 정본 병합 금지

### 현재 차단

- 스토브리그를 최신 Stage04 완료작으로 주장
- 스토브리그 LocalEdge 710건을 무검토 학습 신호로 사용
- 스토브리그 후보 83건을 처분 이력 없이 장거리 신호로 사용
- 두 작품의 차이를 모델 능력 차이로 단정

## 9. 최종 판정

```text
전체 분석 품질: 킬미힐미 우세
Stage01: 둘 다 양호, 킬미힐미 깊이 우세
Stage02: 동급
Stage03 의미 폭: 스토브리그 우세
Stage03 계약·인과 선별: 킬미힐미 우세
Stage04 완결성·검증·계보: 킬미힐미 명확한 우세
```

정본 편입과 향후 창작 모델의 기준 데이터에는 킬미힐미를 우선한다. 스토브리그는 폐기하지 않고 `REWORK_REQUIRED`로 보존하며, 위 보강 계약을 완료한 뒤 재평가한다.

## 10. 재현 자료

- 집계 JSON: `docs/drama_analysis/results/KILLME_VS_STOVE_QUALITY_METRICS_2026-07-15.json`
- 판정 JSON: `docs/drama_analysis/results/KILLME_VS_STOVE_QUALITY_GATE_RESULT_2026-07-15.json`
- 근거 manifest: `docs/drama_analysis/results/KILLME_VS_STOVE_EVIDENCE_MANIFEST_2026-07-15.json`
- 재현 도구: `tools/compare_seqcard_works.py`
- 세션 handoff: `docs/sessions/2026-07-15_killme_vs_stove_quality_comparison/README.md`
