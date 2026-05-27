from __future__ import annotations

from pathlib import Path

from v1700.release_integrity.asset_checker import build_sha256_sums_lines, canonical_file_sha256


def test_canonical_file_sha256_normalizes_crlf_for_utf8_text(tmp_path: Path) -> None:
    lf_path = tmp_path / "sample_lf.txt"
    crlf_path = tmp_path / "sample_crlf.txt"
    lf_path.write_text("alpha\nbeta\n", encoding="utf-8", newline="\n")
    crlf_path.write_text("alpha\nbeta\n", encoding="utf-8", newline="\r\n")

    assert canonical_file_sha256(lf_path) == canonical_file_sha256(crlf_path)


def test_build_sha256_sums_lines_uses_canonical_text_hashes(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("line1\nline2\n", encoding="utf-8", newline="\r\n")
    (repo / "FILELIST.txt").write_text("README.md\n", encoding="utf-8", newline="\n")

    lines = build_sha256_sums_lines(repo, repo / "FILELIST.txt")

    assert lines == [f"{canonical_file_sha256(repo / 'README.md')}  README.md"]
