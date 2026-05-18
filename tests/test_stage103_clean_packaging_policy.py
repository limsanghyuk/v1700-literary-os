import zipfile
from pathlib import Path

from tools.package_stage103_fixed import PACKAGE_NAME, validate_zip


def test_stage103_package_policy_rejects_cache_entries(tmp_path: Path):
    bad = tmp_path / PACKAGE_NAME
    with zipfile.ZipFile(bad, "w") as zf:
        zf.writestr("src/v1700/__pycache__/bad.pyc", "")
    result = validate_zip(bad)
    assert result["status"] == "blocked"
    assert result["clean_packaging_status"] == "blocked"


def test_stage103_package_policy_accepts_posix_clean_zip(tmp_path: Path):
    good = tmp_path / PACKAGE_NAME
    with zipfile.ZipFile(good, "w") as zf:
        zf.writestr("src/v1700/stage103/__init__.py", "")
    result = validate_zip(good)
    assert result["status"] == "pass"
    assert result["zip_path_separator_status"] == "pass"
