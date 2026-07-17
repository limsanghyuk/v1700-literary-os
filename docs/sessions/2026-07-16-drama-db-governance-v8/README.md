# 2026-07-16 드라마 DB Governance V8 릴리스 핸드오프

- Status: `RELEASE_READY / PASS_CANDIDATE_GOVERNANCE_NORMALIZED`
- Branch: `docs/drama-analysis-authority-v3-20260714`
- Scope: tools·validation·SourceLock 거버넌스 정규화, 51작품 전수 current registry, 구조 마이그레이션, fresh extraction 실제 CLI 재실행
- CANONICAL promotion changed: `false`
- EXT6/HXT6: preserved and deferred

## 1. 최종 개발자 아티팩트

```text
artifact: seqcard_ko_developer_release_51works_50complete_governance_v8.zip
SHA256: a0249986653b330b309aded67b6c7e52aa977eecaab2f8d53ad79d36639e099a
size: 49,085,365 bytes
ZIP entries: 9,976
SHA256SUMS entries: 9,975
```

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 파일명·SHA·수량·검증·lineage·handoff만 기록한다.

외부 최종 인증서:

```text
seqcard_ko_governance_v8_final_validation.json
status: PASS
```

## 2. 데이터베이스 상태

```text
works: 51
episodes: 970
SceneCard: 60,875
analysis-layer files: 7,790
Stage01~04 complete: 50
remaining: 최강칠우 / SOURCE_HOLD_EXPERIMENTAL
validation coverage: 51/51
SourceLock coverage: 51/51
```

Source provenance:

```text
legacy SourceLock normalized: 16
direct_reading_attested true: 16
retroactive source inventory: 35
direct_reading_attested false: 35
```

35개 retroactive inventory는 원본 파일·UTF-8 저장본·해시·회차 대응을 현재 시점에 고정하지만, 과거 직접독해 attestation을 소급 창작하지 않는다.

## 3. V8 디렉터리 표준

```text
tools/current/                         현행 범용 검증기
tools/history/                         비권위 역사 검증기
validation/current/                    단일 최신 전역 결과
validation/works/{작품}/current.json   51작품 current fan-in
validation/history/                    구버전·component 증빙
seqcard_ko/source_lock/current/         51작품 current lock/inventory
seqcard_ko/source_lock/INDEX.json       51작품 SourceLock registry
upgrade_audit/structure_history/        구조 마이그레이션 계보
release_state/                          재개 가능한 상태 전이
```

## 4. 검증기 계약

`tools/current` 검증기는 package-relative `--root`를 사용한다.

```text
exit 0: PASS
exit 1: validation failure
exit 2: execution or usage failure
```

실제 실행 명령:

```bash
python tools/current/validate_encoding.py --root . --out <out>
python tools/current/validate_source_lock.py --root . --out <out>
python tools/current/validate_registry.py --root . --out <out>
python tools/current/validate_database_release.py --root . --out <out>
python tools/current/validate_release.py --root . --out <out>
python tools/current/validate_zip_portability.py --zip <artifact> --out <out>
```

모든 전역 CLI가 exit 0, PASS, errors 0, warnings 0을 반환했다.

51작품 `validation/works/{작품}/current.json`도 전수 PASS다. `최강칠우`의 PASS는 구조·레지스트리 정합성 PASS이며 작품 분류는 계속 `SOURCE_HOLD_EXPERIMENTAL`이다.

## 5. 구조 마이그레이션

현행 계약을 위반하던 회차 간 LocalEdge를 의미 문구 변경 없이 CrossEpisodeEdge로 이동했다.

```text
affected works: 8
records migrated: 114
affected local files: 97
remaining cross-episode LocalEdge: 0
meaning_text_changed: false
python_semantic_generation: false
```

대상:

```text
구르미그린달빛
내이름은김삼순
미생
배가본드
비밀의숲
스토브리그
신사의품격
커피프린스
```

계보:

```text
upgrade_audit/structure_history/cross_episode_localedge_v8/migration_report.json
upgrade_audit/structure_history/cross_episode_localedge_v8/migration_ledger.jsonl
```

## 6. 프로세스 분리 결과

### 프로세스 A — validation-only

```text
51작품 current 검증
→ SourceLock 51개 검증
→ validation registry 검증
→ database release 검증
→ validation/current/release_gate.json PASS
→ VALIDATION_PASS
```

### 프로세스 B — package-only

```text
VALIDATION_PASS 확인
→ 임시 파일 제거
→ manifest·SHA256SUMS 생성
→ ZIP 생성
→ 별도 디렉터리 fresh extraction
→ 전역 CLI와 51작품 검증 재실행
→ pre/post tree 비교
→ RELEASE_READY
```

## 7. Fresh extraction 결과

```text
encoding: PASS
source_lock: PASS
registry: PASS
database: PASS
release: PASS
zip_portability: PASS
works checked: 51
works failed: 0
SHA256 missing: 0
SHA256 mismatch: 0
filename mojibake: 0
non-ASCII path without UTF-8 flag: 0
invalid UTF-8: 0
U+FFFD files: 0
pre/post files: 9,976 / 9,976
tree missing: 0
tree extra: 0
tree hash mismatch: 0
```

## 8. 상태 전이와 ZIP 내부 상태

```text
TREE_READY
→ VALIDATION_IN_PROGRESS
→ VALIDATION_PASS
→ PACKAGE_IN_PROGRESS
→ PACKAGE_BUILT
→ FRESH_EXTRACTION_PASS
→ RELEASE_READY
```

ZIP 내부 checkpoint는 불변 아티팩트 생성 시점의 `PACKAGE_BUILT_PENDING_FRESH_EXTRACTION`을 유지한다. 외부 최종 인증서 `seqcard_ko_governance_v8_final_validation.json`과 작업 트리의 `release_state/validation_checkpoint.json`이 post-ZIP 검증과 `RELEASE_READY`를 인증한다.

## 9. 다음 세션 최소 로드

```text
1. docs/drama_analysis/README.md
2. docs/drama_analysis/DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json
3. 이 README
4. V8 ZIP/FINAL_MANIFEST.json
5. V8 ZIP/validation/INDEX.json
6. V8 ZIP/seqcard_ko/source_lock/INDEX.json
7. V8 ZIP/upgrade_audit/structure_history/cross_episode_localedge_v8/migration_report.json
8. 외부 seqcard_ko_governance_v8_final_validation.json
```

## 10. 금지 사항

- V7 또는 V6를 최신 정본 후보로 재사용하지 않는다.
- retroactive inventory 35개를 직접독해 attestation으로 승격하지 않는다.
- 최강칠우를 Stage01~04 complete 또는 CANONICAL로 표시하지 않는다.
- 사용자 명시 승인 없이 CANONICAL 작품을 추가하지 않는다.
- `tools/history` 검증기를 current release gate로 사용하지 않는다.
