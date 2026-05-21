# CLI Quickstart

## Entrypoint

Run the local-first runtime from the repository root:

```bash
python -m v1700.cli "A careful heir studies the ledger after midnight."
```

## JSON Output

Use `--json` to emit a `RenderedProseIR` payload:

```bash
python -m v1700.cli "A careful heir studies the ledger after midnight." --json
```

## Version

Check the documented CLI version:

```bash
python -m v1700.cli --version
```

## Safety

- Provider calls remain disabled in release-time flows.
- The CLI examples are public-safe and synthetic.
- The CLI does not unlock runtime training, LOSDB writes, or migration execution.
