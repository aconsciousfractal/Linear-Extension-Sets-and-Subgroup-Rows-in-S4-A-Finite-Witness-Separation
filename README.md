# Linear-Extension Sets and Subgroup Rows in S4: A Finite Witness Separation

This repository contains the LaTeX source, compiled PDF, finite artifacts, replay scripts, and reproducibility checks for a standalone finite-combinatorics paper on selected structures inside `S4`.

The paper proves a canonical indexing bridge among one-line `S4` words, local prefix flags, and permutation-matrix supports. Its main finite result is a witness separation: exact poset-cone status, equivalently being a linear-extension set of a recovered poset, is not equivalent to subgroup-row status inside the displayed `S4` layer. Coset counts are recorded only as the subgroup-induced bookkeeping used for the fixed `D4` and `V4` rows.

## Repository Layout

```text
paper/      LaTeX source and compiled PDF
results/    JSON/CSV finite artifacts
certified/  finite replay certificates and hash manifest
tables/     selected witness table
scripts/    replay and package-check scripts
tests/      public package tests
docs/       claim boundary and replay notes
```

## Build The Paper

From `paper/`:

```powershell
pdflatex -jobname=Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation main.tex
bibtex Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation
pdflatex -jobname=Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation main.tex
pdflatex -jobname=Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation main.tex
```

Expected PDF:

```text
paper/Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation.pdf
```

## Replay And Checks

The replay scripts use the Python standard library. The test suite uses `pytest`:

```powershell
python -m pip install -r requirements.txt
```

From the repository root:

```powershell
python -B scripts/replay_all.py --verify
python -B scripts/check_public_package.py --check
python -B -m pytest -q -p no:cacheprovider tests
```

Expected summaries: `replay_all.py --verify` reports JSON with `"status": "passed"`, `"mode": "verify"`, and `"package_certification_mode": "check"`; pytest reports `4 passed`. The replay command is read-only. Maintainers should use `python -B scripts/replay_all.py --update-manifest` only after intentional source, artifact, or certificate changes.

## Claim Boundary

The package supports only the finite `S4` claims stated in the paper and in `docs/CLAIM_BOUNDARY.md`. It does not claim an all-subsets classification, an all-tiler classification, a geometric realization theorem, a general `S_n` theorem, or a subgroup-row-versus-subgroup-coset separation theorem.