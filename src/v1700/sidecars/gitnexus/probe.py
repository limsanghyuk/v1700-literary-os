from __future__ import annotations

from pathlib import Path
import shutil

from v1700.sidecars.gitnexus.contracts import GitNexusProbeResult


def probe_gitnexus() -> GitNexusProbeResult:
    for command in ("gitnexus", "gitnexus.cmd"):
        resolved = shutil.which(command)
        if resolved:
            return GitNexusProbeResult(installed=True, command=resolved)

    npm_global_bin = Path.home() / "AppData" / "Roaming" / "npm" / "gitnexus.cmd"
    if npm_global_bin.exists():
        return GitNexusProbeResult(installed=True, command=str(npm_global_bin))

    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if npx:
        return GitNexusProbeResult(
            installed=False,
            command=f"{npx} -y gitnexus@latest",
            error="gitnexus binary not installed; npx path is available for optional use",
        )
    return GitNexusProbeResult(
        installed=False,
        command=None,
        error="gitnexus not installed; python fallback will be used",
    )
