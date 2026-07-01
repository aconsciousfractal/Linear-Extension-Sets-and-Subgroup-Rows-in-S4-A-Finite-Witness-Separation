# Replay Boundary

The replay package verifies the finite artifacts shipped in this repository against the SHA-256 hashes recorded in `certified/replay_hashes.sha256`.

Read-only reviewer command:

```powershell
python -B scripts/replay_all.py --verify
```

Maintainer refresh command after intentional source, artifact, table, or certificate changes:

```powershell
python -B scripts/replay_all.py --update-manifest
```

The `--verify` command checks required artifact files, validates certificate statuses where available, verifies the replay hash manifest, and then runs package certification in read-only check mode. It does not rewrite `certified/replay_hashes.sha256`, `MANIFEST_SHA256.txt`, or `certified/PUBLIC_REPOSITORY_CERTIFICATION.json`.

The `--update-manifest` command rewrites `certified/replay_hashes.sha256` and refreshes package certification. It is a maintainer operation, not the reviewer replay command.

Neither replay mode regenerates atlas data or mirrors files from any external workspace. The replay command does not enumerate every subset of `S4` and does not prove any theorem beyond the finite statements explicitly tied to the packaged artifacts.