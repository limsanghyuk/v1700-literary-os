from pathlib import Path

from tools.package_stage101_fixed import package, validate_zip

ROOT = Path(__file__).resolve().parents[1]


def test_stage101_package_policy_excludes_runtime_indexes_and_cache(tmp_path):
    out = tmp_path / "stage101.zip"
    names = package(ROOT, out)
    validation = validate_zip(out)
    assert names
    assert validation["status"] == "pass"
    assert all("\\" not in name for name in names)
    assert all(not name.startswith((".git/", ".gitnexus/", ".venv/")) for name in names)
    assert all("__pycache__" not in name and not name.endswith(".pyc") and ".pytest_cache" not in name for name in names)

