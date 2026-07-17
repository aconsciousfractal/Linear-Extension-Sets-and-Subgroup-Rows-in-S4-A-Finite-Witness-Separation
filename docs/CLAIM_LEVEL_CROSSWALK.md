# Claim-Level Crosswalk

This crosswalk maps each claim in this repository to the official claim-level
taxonomy defined in `Gate-Disciplined-Computational-Mathematics/docs/CLAIM_LEVELS.md`;
added 2026-07-17 (ledger A-1). It is an additive labeling overlay: it does not
change, weaken, or strengthen any claim, verifier pointer, or scope caveat already
stated in `README.md`, `docs/CLAIM_BOUNDARY.md`, `docs/REPLAY_BOUNDARY.md`, or the
paper. Claim wording is quoted from `docs/CLAIM_BOUNDARY.md`.

Level codes used here (from the official taxonomy):

- `CL2` finite replay: bounded computation with a replay path.
- `CL3` certified finite result: exact finite enumeration with manifest and checker.
- `CL4` theorem import: external theorem used by reference.
- `CLM` metadata: labels, boundaries, manifests, source tags.

The weakest-sufficient rule is applied: where a finite artifact-level claim is exactly
certified but also proved in the paper, it is recorded here at the certified-finite
level (`CL3`), not promoted to an internal-theorem level. Each of the finite
certificates cited below reports `"status": "passed"` with `"checks_failed": 0`, and
the certificate `s4_bridge_table_certificate.json` scopes itself as
`finite_indexing_artifact_only_not_public_theorem`.

## Repository claims

| ID | Claim (quoted from `docs/CLAIM_BOUNDARY.md`) | Primary verifier | Level |
|---|---|---|---|
| B1 | one-line `S4` words, local prefix flags, and permutation-matrix supports are canonically bijective as indexing models | `certified/s4_bridge_table_certificate.json` (exact 24-row counts, `row_checks.all_pass`); `results/s4_bridge_table.json` | `CL3` |
| B2 | the selected data package records 226 selected artifact rows, 219 strict labeled posets giving 219 distinct poset-cone subsets, 221 exact poset-cone artifact rows, and 30 subgroups under the stated convention | `certified/s4_selected_atlas_row_certificate.json`; `certified/s4_selected_atlas_independent_certificate.json`; `certified/s4_selected_atlas_expected_counts.yaml`; `certified/s4_structural_comparison_certificate.json` (`summary.*` counts) | `CL3` |
| B3 | common-precedence closure gives an exact finite criterion for nonempty subsets that are linear-extension sets of recovered posets | `certified/s4_structural_comparison_certificate.json` (closure checks); atlas row/independent certificates | `CL3` |
| B4 | the fixed `D4` and `V4` rows are subgroup rows but not exact poset cones | `certified/s4_d4_v4_rows_certificate.json`; `certified/s4_structural_comparison_certificate.json` (`d4.exact_poset_cone`/`v4.exact_poset_cone` false, `*.subgroup_status` verified) | `CL3` |
| B5 | the fixed `D4` and `V4` subgroup rows have the corresponding left and right coset partitions by finite group theory | finite group theory (standard subgroup coset-partition theorem, used by reference); finite counts recorded in `certified/s4_structural_comparison_certificate.json` (`d4`/`v4` `left_coset_count`, `right_coset_count`) and `certified/s4_d4_v4_rows_certificate.json` | `CL4` |
| B6 | the N-poset witness is an exact poset cone but not a subgroup row | `certified/s4_structural_comparison_certificate.json` (`n_boundary.exact_poset_cone` true, `n_boundary.subgroup_status` not_subgroup) | `CL3` |
| B7 | selected witnesses show exact poset-cone status is not equivalent to subgroup-row status | `certified/s4_structural_comparison_certificate.json`; `tables/s4_selected_witness_comparison.md` | `CL3` |
| R1 | the shipped finite artifacts reproduce against the recorded SHA-256 replay manifest under the read-only reviewer command (`python -B scripts/replay_all.py --verify`) | `certified/replay_hashes.sha256`; `scripts/replay_all.py`; `MANIFEST_SHA256.txt` | `CL2` |

Notes on borderline rows:

- B1, B3, B7 are proved as finite statements in the paper but are recorded here at
  `CL3` (certified finite) rather than at an internal-theorem level, following the
  weakest-sufficient rule and the certificate's own
  `finite_indexing_artifact_only_not_public_theorem` boundary.
- B5 is labeled `CL4` because its warrant is an external standard result of finite
  group theory (a subgroup induces left and right coset partitions), used by
  reference. The specific finite coset counts for the fixed `D4` and `V4` rows are
  additionally recorded exactly in the structural-comparison certificate.
- R1 is the reproducibility/replay claim of the package, backed by a bounded
  read-only replay path, hence `CL2`.

## Boundary and non-claims (metadata, `CLM`)

The scope boundaries and explicit non-claims in `docs/CLAIM_BOUNDARY.md` and the
`boundary.*` checks in the certificates are labels on the claim surface, not results.
They are recorded as `CLM` metadata:

| ID | Non-claim / boundary (quoted from `docs/CLAIM_BOUNDARY.md`) | Level |
|---|---|---|
| M1 | classification of all subsets of `S4` (not claimed) | `CLM` |
| M2 | classification of all exact covers or tilers (not claimed) | `CLM` |
| M3 | a geometric realization theorem (not claimed) | `CLM` |
| M4 | a general `S_n` theorem (not claimed) | `CLM` |
| M5 | an independent theorem separating subgroup-row status from subgroup-coset partition status (not claimed) | `CLM` |
| M6 | that the selected artifact-row counts are a full atlas of all `S4` subsets (not claimed) | `CLM` |

## Reference

The authoritative level definitions are in
`Gate-Disciplined-Computational-Mathematics/docs/CLAIM_LEVELS.md`. This file is a
companion index for this repository only; it does not restate or replace the
authoritative table.
