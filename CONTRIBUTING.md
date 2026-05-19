# Contributing to V1700 Literary OS

## Branch Policy

- `main` is the verified integration branch.
- Use `stage/<stage-number>-<topic>` for new stage work.
- Use `company/<stage-number>-<topic>` when importing work from another computer.
- Do not merge a stage branch into `main` unless CI, release gates, and repo doctor pass.

## Required Local Checks

Before opening a pull request or pushing a stage release:

```bash
python -m pip install -e ".[dev]"
python -m compileall -q src tools
python -m pytest tests/ -q
python tools/run_ci_dependency_preflight.py
python tools/run_stage130_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## Version Tags

Use annotated stage tags for release points:

```bash
git tag -a v1700-stage131 -m "V1700 Stage131 <title>"
git push origin v1700-stage131
```

The release workflow publishes an integrated ZIP and SHA256 sidecar for pushed tags.

## Two-Machine Workflow

Do not move source code by ZIP as the primary workflow. Use GitHub as the source of truth:

```bash
git fetch --all --tags --prune
git checkout main
git pull --ff-only origin main
git checkout -b stage/131-gig-advisory
```

If another machine has different work, push it as a branch and compare it with `main` rather than copying files over Google Drive.
