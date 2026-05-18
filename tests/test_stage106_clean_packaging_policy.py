import zipfile
from pathlib import Path

def test_stage106_clean_packaging_policy_if_package_exists():
    package = Path(__file__).resolve().parents[1].parent / "V1700_stage106_adaptive_author_profile_style_genome_FIXED.zip"
    if not package.exists():
        return
    with zipfile.ZipFile(package) as zf:
        names = zf.namelist()
    assert not [n for n in names if "\\" in n]
    assert not [n for n in names if "__pycache__" in n or n.endswith(".pyc") or ".pytest_cache" in n or ".gitnexus" in n]
