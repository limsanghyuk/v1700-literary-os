# 드라마 계보·패키지·핸드오프 규칙 v2

- Document ID: `DRAMA-LINEAGE-PACKAGE-HANDOFF-V2`
- Status: `AUTHORITATIVE_CANDIDATE`

## 1. 원칙

분석본을 덮어쓰지 않는다. 실패본·교정본·재저작본·정본 후보의 관계를 명시적으로 기록한다.

```text
source → run → validation → checkpoint → comparison → promotion
```

## 2. SourceLock 최소 필드

```text
schema
work_id
episodes_total
canonical_scene_count_total
source_archive
numbering_policy 또는 scene_boundary_policy
direct_reading_required
python_semantic_generation
raw_script_exported
status
episodes
current_completed_episodes
next
```

회차별:

```text
episode_no
source_filename
source_encoding
original_bytes_sha256
canonical_scene_count
quarter_ranges
scene_hashes 또는 heading_hashes
source_marker_anomaly
```

## 3. run provenance

작품별 실행은 다음 정보를 manifest에 남긴다.

```text
run_id
provider
model_id
contract_version
source_lock_sha256
episode_span
direct_reading_attested
python_semantic_generation
status
parent_run_id
supersedes
created_at
```

GPT·Claude 독립 run은 서로 다른 경로와 run_id를 사용한다. 자동 병합·평균·union으로 정본을 만들지 않는다.

## 4. 권장 디렉터리

```text
analysis_runs/<work>/<contract_version>/<provider>/<run_id>/
  PACKAGE_MANIFEST.json
  source_lock/
  quarter_audits/
  authored/
  authored_seq/
  authored_arc/
  authored_chararc/
  authored_relarc/
  authored_edges/
  authored_bridge/
  authored_cast/
  derived_character_load/
  _ext6_audit/
  validation/
  reports/
  lineage/
  SHA256SUMS.txt
```

기존 `seqcard_ko/` 배치에 편입할 때도 원래 run 경로와 SHA를 manifest에 보존한다.

## 5. 회차 체크포인트

각 회차 Q1→Q4와 강한 게이트 완료 직후 체크포인트를 만든다.

필수:

- 해당 회차 Stage01~03
- EXT6 Bridge delta, Cast, Load, Alignment, Coverage
- QuarterAudit 4건
- validation result
- SourceLock progress
- manifest/checksum

다음 회차는 체크포인트 생성 성공 후 시작한다.

## 6. 블록 체크포인트

8회 단위 또는 사용자 지정 구간 종료 시:

- 회차 체크포인트를 결합
- 누적 ID/FK/Bridge alias 검사
- unresolved scene, duplicate ID, cross-file mismatch 검사
- Stage04는 아직 생성하지 않음

## 7. quarantine

다음은 즉시 격리한다.

- Python 의미 생성
- keyword/template artifact
- 잘못된 scene boundary
- source mismatch
- Stage01 내용 FAIL
- Stage02 coverage FAIL
- 허위 Stage03/04

격리 시 보존:

```text
SourceLock
alignment
source hashes
validation report
failure reason
superseded_by 예정값
```

격리본은 후속 Stage 입력에서 제외한다.

## 8. supersession

재저작 또는 결정론적 교정본은 다음을 기록한다.

```text
old_run_id
old_sha256
new_run_id
new_sha256
reason
semantic_text_changed
correction_ledger
```

- `semantic_text_changed=false`: 계약·표기·계산 보정.
- `semantic_text_changed=true`: 원문 재독해가 필요한 새 run.

## 9. 패키지 검증

ZIP 생성 전:

1. 모든 JSON/JSONL 파싱.
2. 강한 게이트 통과.
3. raw script·secret·임시 Python 제외.
4. 파일별 SHA256 생성.
5. manifest counts와 실제 레코드 수 일치.
6. ZIP `testzip()` 또는 동등 무결성 검사.
7. ZIP 자체 SHA256 생성.

## 10. 허브 편입 절차

```text
1. 별도 branch/run 경로에 업로드
2. manifest와 검증 보고서 먼저 검토
3. exact schema validator
4. EXT6 validator
5. lineage/supersession 검토
6. 작품 전체를 한 lineage로 수용 또는 전량 보류
7. 사용자 승인 전 PASS_CANDIDATE
8. 승인 후 CANONICAL
```

SceneCard는 한 판본, Stage03/04는 다른 판본처럼 서로 다른 ordinal lineage를 혼합하지 않는다.

## 11. 개발자 핸드오프 보고서 필수 항목

- 작품/회차 범위
- 원본 SHA 및 SourceLock 상태
- 직접독해 증명
- 각 계층 레코드 수
- Gate별 결과
- 결정론적 교정 내역
- unresolved/warning
- canonical 여부
- 다음 재진입 지점
- ZIP SHA256
