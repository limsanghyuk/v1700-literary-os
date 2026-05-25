# V1700 Development Workflow

> GitHub is the single source of truth.  
> This repository follows a Stage-based workflow adapted from the `literary-os` V1.1 workflow model.

## Core Principles

1. Always sync before work.
2. Store proposals, blueprints, and handoff docs in `docs/`.
3. Use dedicated branches for every Stage, repair, or workflow change.
4. Push every session that changes the repository state.
5. Treat `main`, CI, tags, and release assets as the authority chain.

## Session Start Protocol

At the start of every session:

```text
1. Check the latest main branch and relevant Stage tags on GitHub.
2. Sync the local repository and confirm the active branch.
3. Read docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md.
4. Read the relevant Stage proposal and blueprint.
5. Read the latest session note when the task continues prior work.
6. Run the mandatory predevelopment check.
7. Refresh GitNexus or record fallback status.
```

## Session End Protocol

Before ending a session:

```text
1. Save a session summary when the work changes architecture, workflow, or release state.
2. Commit the code, docs, manifests, and release evidence together when they belong to one change.
3. Push the branch.
4. Record the next required step.
```

## Branch Model

```text
main
  |- stageNNN-topic
  |- hotfix-stageNNN-topic
  `- workflow-topic
```

Examples:

- `stage161-memory-body`
- `stage149-integrity-repair`
- `workflow-v11-stage-preflight-upgrade`

## Standard Delivery Flow

```text
1. Branch from main.
2. Run mandatory predevelopment.
3. Implement and validate locally.
4. Push and wait for GitHub Actions.
5. Open or update the PR.
6. Merge after CI is green.
7. Tag from merged main.
8. Publish the GitHub Release with ZIP, .sha256, and SHA256SUMS.txt.
9. Verify release authority from a fresh clone or fresh extraction.
```

## Document Structure

```text
docs/
|- sessions/
|- workflow/
|- proposals/
|- architecture/
|- development/
|- runbooks/
`- stages/
```

## Environment Notes

Different tools may be used across environments, but the workflow must remain the same:

- sync first
- run preflight first
- keep GitHub main as the baseline
- push reviewed branch work instead of leaving local-only state

## Current Baseline

As of this workflow upgrade:

- source repository: `https://github.com/limsanghyuk/v1700-literary-os`
- active baseline: `Stage160`
- release authority: `main + Stage tag + release asset triplet`
