# API Minimum

Stage143 documents a minimum API surface without enabling a live server.

## Contract

- Method: `POST`
- Path: `/v1/render-prose`
- Status: documentation-only
- Authentication: not required for this documentation contract

## Request

The request carries a prompt and requests a `RenderedProseIR`-shaped response.

See [render_request.json](/C:/AI_Codex/codex-work/gpt/github_push/v1700-literary-os_stage136/docs/user/examples/render_request.json).

## Response

The documented response shape mirrors the CLI `--json` payload.

See [render_response.json](/C:/AI_Codex/codex-work/gpt/github_push/v1700-literary-os_stage136/docs/user/examples/render_response.json).

## Safety

- No provider calls are required.
- No live HTTP service is enabled by this stage.
- No credentials are documented or exposed.
