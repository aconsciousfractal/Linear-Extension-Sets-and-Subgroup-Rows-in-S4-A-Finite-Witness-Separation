# Reproduce

Run commands from the repository root unless stated otherwise.

## Build The Paper

```powershell
cd paper
pdflatex -jobname=Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation main.tex
bibtex Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation
pdflatex -jobname=Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation main.tex
pdflatex -jobname=Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation main.tex
cd ..
```

## Replay And Check The Package

```powershell
python -B scripts/replay_all.py --verify
python -B scripts/check_public_package.py --check
python -B -m pytest -q -p no:cacheprovider tests
```

Expected summaries: `replay_all.py --verify` reports JSON with `"status": "passed"`, `"mode": "verify"`, and `"package_certification_mode": "check"`; pytest reports `9 passed`.

The replay command in `--verify` mode checks certificate status, verifies `certified/replay_hashes.sha256`, and runs package certification in read-only check mode. It does not rewrite the replay hash manifest, package manifest, or release certification. Use `python -B scripts/replay_all.py --update-manifest` only when intentionally refreshing the replay hash manifest and public package certification after source, artifact, table, or certificate changes.

The package checker is read-only by default and verifies required files, bibliography consistency, hash coverage, certificate status, manifest consistency, claim-boundary wording, absence of local absolute paths, and absence of non-package process markers in repository text files. Use `python -B scripts/check_public_package.py --write` only when intentionally refreshing release certification after artifact changes. The pytest command uses `-B` and disables the pytest cache provider so routine review does not leave Python bytecode or `.pytest_cache` files behind.