from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HASH_MANIFEST = ROOT / "certified" / "replay_hashes.sha256"
HASHED = [
    "scripts/replay_all.py",
    "results/s4_bridge_table.json",
    "results/s4_selected_atlas.json",
    "results/s4_structural_comparison.json",
    "results/s4_structural_comparison.csv",
    "tables/s4_selected_witness_comparison.md",
    "certified/s4_bridge_table_certificate.json",
    "certified/s4_d4_v4_rows_certificate.json",
    "certified/s4_selected_atlas_expected_counts.yaml",
    "certified/s4_selected_atlas_independent_certificate.json",
    "certified/s4_selected_atlas_row_certificate.json",
    "certified/s4_structural_comparison_certificate.json",
]
CERTIFICATES = [
    "certified/s4_bridge_table_certificate.json",
    "certified/s4_d4_v4_rows_certificate.json",
    "certified/s4_selected_atlas_independent_certificate.json",
    "certified/s4_selected_atlas_row_certificate.json",
    "certified/s4_structural_comparison_certificate.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_hash_entries() -> dict[str, str]:
    entries: dict[str, str] = {}
    for rel in sorted(HASHED):
        path = ROOT / rel
        if not path.exists():
            raise FileNotFoundError(rel)
        entries[rel] = sha256(path)
    return entries


def read_hash_manifest() -> dict[str, str]:
    if not HASH_MANIFEST.exists():
        return {}
    entries: dict[str, str] = {}
    for line in HASH_MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(maxsplit=1)
        entries[rel.strip()] = digest.strip()
    return entries


def check_hash_manifest() -> dict[str, Any]:
    expected = expected_hash_entries()
    observed = read_hash_manifest()
    missing = sorted(set(expected) - set(observed))
    extra = sorted(set(observed) - set(expected))
    mismatched = [
        {"path": rel, "expected": expected[rel], "observed": observed[rel]}
        for rel in sorted(set(expected) & set(observed))
        if observed[rel] != expected[rel]
    ]
    passed = not missing and not extra and not mismatched
    return {
        "passed": passed,
        "manifest": "certified/replay_hashes.sha256",
        "missing": missing,
        "extra": extra,
        "mismatched": mismatched,
    }


def check_certificates() -> list[dict[str, object]]:
    out = []
    for rel in CERTIFICATES:
        path = ROOT / rel
        payload = json.loads(path.read_text(encoding="utf-8"))
        failed = payload.get("checks_failed", payload.get("num_failed", 0))
        passed = payload.get("status") == "passed" and failed == 0
        out.append({"path": rel, "passed": passed, "status": payload.get("status"), "failure_count": failed})
    return out


def write_hash_manifest() -> None:
    lines = [f"{digest}  {rel}" for rel, digest in expected_hash_entries().items()]
    HASH_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    HASH_MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_package_checker(*, write_mode: bool) -> subprocess.CompletedProcess[str]:
    mode = "--write" if write_mode else "--check"
    return subprocess.run(
        [sys.executable, "scripts/check_public_package.py", mode],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify or refresh the public S4 finite-witness replay boundary."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--verify", action="store_true", help="read-only replay verification mode (default)")
    mode.add_argument(
        "--update-manifest",
        action="store_true",
        help="maintainer mode: rewrite replay hash manifest and package certification",
    )
    args = parser.parse_args()

    update_mode = args.update_manifest
    certs = check_certificates()
    if not all(item["passed"] for item in certs):
        print(json.dumps({"status": "failed", "certificate_statuses": certs}, indent=2))
        return 1

    if update_mode:
        write_hash_manifest()

    hash_status = check_hash_manifest()
    if not hash_status["passed"]:
        print(
            json.dumps(
                {
                    "status": "failed",
                    "mode": "update-manifest" if update_mode else "verify",
                    "certificate_statuses": certs,
                    "hash_manifest_status": hash_status,
                },
                indent=2,
            )
        )
        return 1

    completed = run_package_checker(write_mode=update_mode)
    checker_summary: Any
    try:
        checker_summary = json.loads(completed.stdout) if completed.stdout.strip() else {}
    except json.JSONDecodeError:
        checker_summary = completed.stdout

    summary = {
        "status": "passed" if completed.returncode == 0 else "failed",
        "mode": "update-manifest" if update_mode else "verify",
        "hash_manifest": "certified/replay_hashes.sha256",
        "hash_covered_files": HASHED,
        "certificate_statuses": certs,
        "hash_manifest_status": hash_status,
        "package_certification_mode": "write" if update_mode else "check",
        "package_checker": checker_summary,
    }
    if completed.stderr.strip():
        summary["package_checker_stderr"] = completed.stderr
    print(json.dumps(summary, indent=2))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())