# V1700 Stage128 — SharedWorld / SharedCharacter Read-Only Absorption

## 목적

Stage128은 Stage127의 MultiWork Preflight & Isolation Audit 이후 첫 흡수 단계다. 목표는 V571 계열의 SharedCharacterDB와 SharedWorldDB 개념을 직접 DB로 병합하지 않고, 읽기 전용 adapter로만 흡수하는 것이다.

## 기준선

- Baseline: Stage127 — MultiWork Preflight & Isolation Audit
- Active stage: Stage128
- 다음 단계: Stage129 — MultiWorkCIM + Cross-Work Canon Governor

## 핵심 원칙

1. SharedCharacter와 SharedWorld는 읽기 전용 projection으로만 노출한다.
2. cross-project write는 항상 0이어야 한다.
3. 원고 전문, 세계관 bible 원문, 내부 노트는 export하지 않는다.
4. cross-owner private character reuse는 same_owner, explicit_license_edge, public_domain_flag 중 하나와 author approval이 있어야 한다.
5. SharedWorld는 Stage128에서 canon source of truth가 아니다. 권위 승격은 Stage129 Canon Governor로 미룬다.
6. GitNexus는 optional sidecar이며, 없는 환경에서는 Python fallback preflight가 필수다.

## Stage128 Release Gate

- Stage127 baseline gate pass
- SharedCharacterReadOnlyAdapter pass
- SharedWorldReadOnlyAdapter pass
- LicenseBoundaryAdapter pass
- ProjectIsolationGuard pass
- CanonConflictReport pass
- unauthorized cross read/write = 0
- raw manuscript provider leakage = 0
- full text exported = false
- provider default calls = 0
- Node2 raw reveal access = 0
- repo doctor active stage recognition
- clean ZIP packaging

## 산출물

```text
release/current/stage128_read_only_absorption_report.json
release/current/stage128_release_gate_report.json
release/current/stage128_summary.json
release/current/stage128_read_only_absorption_pack/
```

## 검증 명령

```bash
python -m compileall src tools
python tools/run_stage128_read_only_absorption.py
python tools/run_stage128_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest -q tests/test_stage128_read_only_absorption.py
```
