# Codex 드라마 직접독해 멀티 에이전트 실험 계획

## 0. 목적

이 문서는 Codex/로컬 실행기에서 `결혼못하는남자` 및 이후 한국 드라마 코퍼스를 직접독해 방식으로 분석하기 위한 실험 설계다.

ChatGPT 단일 대화에서 발생한 EP05~06 batch 실패의 원인은 의미 저작 범위를 확장하면서 template generation으로 붕괴된 것이다. Codex 실험은 이를 피하기 위해 **멀티 에이전트 역할 분리 + 회차별 lock + supervisor verification**을 강제한다.

## 1. 실행 구조

```text
Orchestrator
  ├─ Inventory / SourceLock Builder          # 로컬 Python, no_raw only
  ├─ WriterAgent-01                          # EP01~EP02 또는 단일 EP
  ├─ WriterAgent-02                          # EP03~EP04 또는 단일 EP
  ├─ ...
  ├─ VerifierAgent                           # 구조/내용/반복성 검증
  ├─ SupervisorAgent                         # 허위 PASS, 누락, desync 차단
  └─ ReleaseGate                             # manifest/SHA/package/report
```

## 2. 역할 계약

### Orchestrator

- ZIP/HWP/TXT/DOC/PDF inventory 생성
- 회차 파일 매핑
- scene boundary 후보 생성
- `source_lock.no_raw.json` 생성
- writer packet 생성
- agent 결과 수집
- 실패 회차 재파견

### WriterAgent

- 1회차 또는 최대 2회차만 담당
- 원문을 직접 읽고 Stage1 의미 필드 저작
- Stage2 hint를 장면 작성 중 병행 생성
- keyword 기반 자동 문장 생성 금지
- 다른 회차와 문장 skeleton 공유 금지

### VerifierAgent

- Stage1 필드 독립성 검사
- Stage2 18필드 검사
- 16기능 taxonomy 검사
- coverage missing/overlap 검사
- `core_mix` provenance 검사
- repeated ngram/skeleton 검사
- visible EPxx-yyy marker 검사
- raw script export 검사

### SupervisorAgent

- WriterAgent report를 그대로 믿지 않음
- 산출물 파일을 직접 열어 독립 audit 수행
- false PASS 발견 시 quarantine 및 재파견
- batch expansion이 의미 필드 생성으로 변질되는지 감시

## 3. 입력/출력 정책

Allowed input to agent:

```text
- 제한된 회차 source packet
- scene boundary 후보
- source sha/span
- prior episode canonical summaries, if approved
```

Forbidden output:

```text
- raw script text
- verbatim dialogue
- full scene excerpt
- source paragraph copy
- hidden prompt/log with original text
```

Allowed output:

```text
- Stage1 SceneCard semantic metadata
- Stage2 SequenceBlueprint
- EpisodeArc / Synopsis
- validation report
- manifest / SHA256
```

## 4. 실행 모드

| Mode | Writer Agents | Verifier | Supervisor | 용도 |
|---|---:|---:|---:|---|
| Economy | 1 | 1 | 1 | 단일 회차 품질 확보 |
| Standard | 4 | 1 | 1 | 16부작 작품 1개 |
| Burst | 8 | 1~2 | 1 | Claude식 wave 처리 |

Codex/ChatGPT 한도 문제가 있으므로 처음부터 Burst를 기본값으로 쓰지 않는다.

## 5. EP05~06 실패 방지 불변식

```text
I1: batch는 검증·포장 단위이지 의미 저작 단위가 아니다.
I2: EPn이 PASS/LOCK되기 전 EPn+1 Stage1 작성 금지.
I3: 2회차 담당 agent도 내부적으로 EPn→EPn+1 순서로 읽는다.
I4: Python은 추출·정렬·검증·패키징만 한다.
I5: Python이 scene_action/information_delta/decision/function/hook을 생성하면 FAIL.
I6: visible EPxx-yyy reference marker가 의미 필드에 있으면 FAIL.
I7: repeated skeleton phrase가 threshold를 넘으면 FAIL.
I8: Supervisor는 writer report가 아니라 파일 내용을 기준으로 판정한다.
```

## 6. Codex 실험 단계

### Phase A — Source Inventory

- `한국드라마04.zip` inventory
- nested ZIP/HWP/TXT/DOC/PDF mapping
- `결혼못하는남자` 16부작 source map 생성
- no raw export check

### Phase B — Single Episode Replication

- EP05 단독 분석
- EP01~04 패턴과 비교
- release gate 통과 확인

### Phase C — True 2-Episode Agent Test

- WriterAgent-A: EP05 완료 후 EP06 진행
- VerifierAgent: 두 회차 독립 검증
- SupervisorAgent: false PASS 차단
- batch packaging은 마지막에만 수행

### Phase D — 8-Agent Wave Test

- 8 agents × 2 episodes = 16부작 wave
- 각 agent는 제한된 source packet만 사용
- supervisor가 전체 episode ledger 검증

### Phase E — Corpus Expansion

- 1개 작품 완주 후 다른 작품으로 확장
- wave별 artifact manifest와 failure ledger 축적

## 7. 산출물 구조

```text
release/current/drama_close_reading/<work_id>/
  epXX/
    source_lock.no_raw.json
    stage1_scene_cards.jsonl
    stage2_sequence_blueprint.json
    synopsis.md
    validation.json
    MANIFEST.json
  batch/
    ep01_16_episode_ledger.json
    series_arc_candidate.json
    wave_validation_report.json
```

## 8. 한도 절약 전략

- 원문 extraction/scene split/hash는 로컬 Python
- 모델 호출은 의미 저작/고급 검증에만 사용
- 실패 시 전체 회차 재작성 금지, scene/Q/sequence 단위 repair
- full context 투입 금지, Q packet 단위 투입
- raw text를 허브나 provider log에 저장하지 않음

## 9. 성공 기준

```text
EP-level:
- scene_count locked
- Stage1 complete
- Stage2 coverage PASS
- content depth threshold PASS
- repeated skeleton PASS
- raw_script_exported=false

Work-level:
- all episodes PASS
- no quarantined episode in canonical ledger
- SeriesArc generated from episode turns
- release manifest + SHA256 complete
```

## 10. 결론

Codex 실험은 ChatGPT 단일 대화의 역할 시뮬레이션이 아니라, 실제 파일 기반 orchestration과 독립 verifier/supervisor 구조를 갖춰야 한다. 36작품급 분석은 이 구조 없이는 안정적으로 불가능하다.
