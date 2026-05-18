from pathlib import Path
from zipfile import ZipFile
ROOT = Path(__file__).resolve().parents[1]

def test_stage104_clean_packaging_policy_if_package_exists():
    package = ROOT.parent / "V1700_stage104_commercial_writer_studio_beta_FIXED.zip"
    if not package.exists():
        return
    with ZipFile(package) as zf:
        names = zf.namelist()
    assert not [name for name in names if "\\" in name or "__pycache__" in name or name.endswith(".pyc") or ".pytest_cache" in name or ".gitnexus" in name]
