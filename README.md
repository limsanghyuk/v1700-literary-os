# V1700 Literary OS — Stage128

> **SharedWorld / SharedCharacter Read-Only Absorption**  
> Provider-Zero AI 장편 소설·드라마 시나리오 생성 시스템

[![Stage](https://img.shields.io/badge/stage-128-blue)]()
[![Version](https://img.shields.io/badge/version-1.28.0-blue)]()
[![Gate](https://img.shields.io/badge/release%20gate-20%2F20%20PASS-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()

---

## 빠른 시작

```bash
pip install -e .

# Stage128 검증
python -m compileall src tools
python tools/run_stage128_read_only_absorption.py
python tools/run_stage128_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests/test_stage128_read_only_absorption.py
```

---

## 시스템 개요

V1700 Literary OS는 Provider-Zero 원칙으로 운영되는 장편 서사 생성 플랫폼입니다. 외부 LLM 프로바이더 호출 0건 상태에서 릴리즈 게이트를 통과하는 것이 핵심 설계 원칙입니다.

Stage128은 Stage127의 MultiWork Preflight & Isolation Audit 이후 첫 흡수 단계로, V571 계열의 `SharedCharacterDB`와 `SharedWorldDB`를 **읽기 전용 adapter**로만 흡수합니다.

```
src/v1700/
├── shared_readonly_absorption/   # Stage128 핵심 — 읽기 전용 흡수 어댑터
│   ├── shared_character_adapter.py
│   ├── shared_world_adapter.py
│   ├── license_boundary.py
│   ├── project_isolation.py
│   ├── canon_conflict_report.py
│   └── contracts.py
├── multiwork_preflight/          # Stage127 MultiWork Preflight
├── stage128/                     # Stage128 러너
├── gates/                        # 릴리즈 게이트
├── cross_lineage/                # V571 lineage 흡수
├── narrative_physics/            # 서사 물리 엔진
├── nie/                          # Narrative Intelligence Engine
└── ...                           # Stage72~Stage128 전체 패키지
```

---

## Stage128 핵심 원칙

1. SharedCharacter · SharedWorld는 **읽기 전용 projection**으로만 노출
2. cross-project write는 항상 **0**
3. 원고 전문 · 세계관 bible 원문 · 내부 노트는 **export 금지**
4. cross-owner private character reuse는 `same_owner` / `explicit_license_edge` / `public_domain_flag` + author approval 필수
5. SharedWorld는 Stage128에서 canon source of truth가 아님 → Stage129 Canon Governor로 위임
6. GitNexus는 optional sidecar — 없는 환경에서는 Python fallback preflight 필수

---

## Stage128 Release Gate (20/20 PASS)

| 체크 | 상태 |
|------|------|
| Stage127 baseline gate | ✅ PASS |
| SharedCharacterReadOnlyAdapter | ✅ PASS |
| SharedWorldReadOnlyAdapter | ✅ PASS |
| LicenseBoundaryAdapter | ✅ PASS |
| ProjectIsolationGuard | ✅ PASS |
| CanonConflictReport | ✅ PASS |
| read_only_absorption_enforced | ✅ PASS |
| no_shared_db_write_enabled | ✅ PASS |
| unauthorized cross read/write = 0 | ✅ PASS |
| raw_manuscript_leakage = 0 | ✅ PASS |
| provider_zero | ✅ PASS |
| node2_boundary | ✅ PASS |
| credential_leakage = 0 | ✅ PASS |
| stage129_canon_governor_deferred | ✅ PASS |
| gitnexus_python_fallback_preflight | ✅ PASS |
| gitnexus_shape_check | ✅ PASS |
| docs_manifest | ✅ PASS |
| repo_doctor_active_stage_ready | ✅ PASS |
| clean_zip_packaging | ✅ PASS |
| secret_scan | ✅ PASS |

```json
{
  "provider_default_calls": 0,
  "live_provider_call_count_in_release_gate": 0,
  "cross_project_write": 0,
  "raw_manuscript_cross_project_leakage": 0,
  "node2_raw_reveal_access": 0,
  "credential_leakage": 0,
  "branchpoint_lineage_preserved": true
}
```

---

## 스테이지 이력 (Stage72~Stage128)

| 범위 | 주요 내용 |
|------|-----------|
| Stage72~83 | 초기 안정화, Korean Drama Composition, Blind Critic Benchmark |
| Stage84~99 | Cross-lineage Absorption, Provider Evaluation, GitNexus, Security Hardening |
| Stage100~110 | RC Preflight, Dual-Mode Evaluation, Studio Beta, Plugin Marketplace, Stable Release |
| Stage111~113 | V485 Absorption, GitNexus-Aware NIE Preflight, Physics Reward Bridge |
| Stage114~120 | AMW, CIM, RAG Fusion, Tension Curve, NIL Orchestrator, Gate25 NIE v1 |
| Stage121~126 | Absorption Candidate Registry, ASD Gate28, PNE Gate29, Cross-lineage Release |
| Stage127 | MultiWork Preflight & Isolation Audit |
| **Stage128** | **SharedWorld / SharedCharacter Read-Only Absorption ← 현재** |

---

## 다음 개발 방향

- **Stage129**: MultiWorkCIM + Cross-Work Canon Governor
- **Stage130**: MultiWork Release
- **Stage131**: GIG / Gate26 Advisory Absorption

---

## 개발 환경

```bash
pip install -e ".[dev]"  # dev 의존성 포함

# 전체 테스트
python -m pytest -q tests/

# Stage별 게이트 확인
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

---

## 무결성 확인

```bash
sha256sum -c SHA256SUMS.txt
```

상세 stage 문서 → `docs/stages/`  
매니페스트 → `manifests/`
