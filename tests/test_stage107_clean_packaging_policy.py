from pathlib import Path
from tools.package_stage107_fixed import package_stage107_fixed

def test_stage107_clean_packaging_policy(tmp_path):
    root = Path(__file__).resolve().parents[1]
    report = package_stage107_fixed(root, tmp_path)
    assert report['status'] == 'pass'
    assert report['backslash_path_entries'] == 0
    assert report['cache_entries'] == 0
