from __future__ import annotations
import hashlib, json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT.parent / 'V1700_stage109_plugin_marketplace_architecture_FIXED.zip'
FILELIST = ROOT.parent / 'V1700_stage109_FIXED_filelist.txt'
EXCLUDE_DIRS = {'.git', '__pycache__', '.pytest_cache', '.gitnexus', '.venv'}
EXCLUDE_SUFFIXES = {'.pyc', '.tmp', '.log'}
with ZipFile(PACKAGE, 'w', ZIP_DEFLATED) as z:
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.suffix in EXCLUDE_SUFFIXES:
            continue
        arc = path.relative_to(ROOT).as_posix()
        z.write(path, arc)
with ZipFile(PACKAGE) as z:
    names = z.namelist()
    bad_sep = [n for n in names if '\\' in n]
    cache = [n for n in names if '__pycache__' in n or n.endswith('.pyc') or '.pytest_cache' in n or '.gitnexus' in n]
    env = [n for n in names if n.endswith('.env') or '/.env' in n]
    if bad_sep or cache or env:
        raise SystemExit(json.dumps({'bad_sep': bad_sep[:5], 'cache': cache[:5], 'env': env[:5]}, indent=2))
sha = hashlib.sha256(PACKAGE.read_bytes()).hexdigest()
PACKAGE.with_suffix(PACKAGE.suffix + '.sha256').write_text(sha + '\n', encoding='utf-8')
FILELIST.write_text('\n'.join(names) + '\n', encoding='utf-8')
print(json.dumps({'package': str(PACKAGE), 'sha256': sha, 'entries': len(names)}, indent=2))
