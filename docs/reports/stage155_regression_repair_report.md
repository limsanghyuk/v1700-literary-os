# Stage155 Regression Repair Report

Full regression review found that the Stage155 release ZIP included `.pytest_cache` entries.

Repair applied:

- Removed `.pytest_cache` from the release package.
- Rebuilt `FILELIST.txt` without runtime cache entries.
- Rebuilt `SHA256SUMS.txt` using normalized text hashing compatible with the release asset checker.

The Stage155 execution contract logic and release gate logic were not changed.
