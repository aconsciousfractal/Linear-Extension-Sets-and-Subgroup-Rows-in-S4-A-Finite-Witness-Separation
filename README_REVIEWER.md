# Reviewer Guide

This repository is organized so a reader can inspect the paper, finite artifacts, and package checks without external project files.

Recommended review order:

1. Build `paper/main.tex` with the commands in `REPRODUCE.md`.
2. Run `python -B scripts/replay_all.py --verify` from the repository root. Expected JSON fields include `"status": "passed"`, `"mode": "verify"`, and `"package_certification_mode": "check"`.
3. Run `python -B scripts/check_public_package.py --check`.
4. Run `python -B -m pytest -q -p no:cacheprovider tests`; expected summary: `9 passed`.
5. Compare the selected witness table in `tables/` with the proposition in Section 7 of the paper.
6. Check `docs/CLAIM_BOUNDARY.md` for nonclaims.

The finite certificates support explicit finite checks. They do not replace the proof prose in the paper. The default replay path is read-only; `--update-manifest` is a maintainer command for intentional package refreshes.