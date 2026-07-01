import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_NAME = "Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation.pdf"


def test_public_package_checker_passes_without_writing():
    tracked = [ROOT / "MANIFEST_SHA256.txt", ROOT / "certified" / "PUBLIC_REPOSITORY_CERTIFICATION.json"]
    before = {path: path.read_bytes() for path in tracked}
    completed = subprocess.run(
        [sys.executable, "scripts/check_public_package.py", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    after = {path: path.read_bytes() for path in tracked}
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert after == before
    cert = json.loads((ROOT / "certified" / "PUBLIC_REPOSITORY_CERTIFICATION.json").read_text(encoding="utf-8"))
    assert cert["status"] == "passed"
    assert cert["public_release_allowed"] is True
    assert cert["owner_approval"] is True


def test_public_replay_verify_passes_without_writing():
    tracked = [
        ROOT / "certified" / "replay_hashes.sha256",
        ROOT / "MANIFEST_SHA256.txt",
        ROOT / "certified" / "PUBLIC_REPOSITORY_CERTIFICATION.json",
    ]
    before = {path: path.read_bytes() for path in tracked}
    completed = subprocess.run(
        [sys.executable, "scripts/replay_all.py", "--verify"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    after = {path: path.read_bytes() for path in tracked}
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert after == before
    summary = json.loads(completed.stdout)
    assert summary["mode"] == "verify"
    assert summary["package_certification_mode"] == "check"
    assert summary["hash_manifest_status"]["passed"] is True


def test_public_claim_boundary_is_explicit():
    text = (ROOT / "docs" / "CLAIM_BOUNDARY.md").read_text(encoding="utf-8")
    assert "This package does not claim" in text
    assert "classification of all subsets" in text
    assert "general `S_n` theorem" in text
    assert "independent theorem separating subgroup-row status from subgroup-coset" in text


def test_public_pdf_name_exists_after_build():
    pdf = ROOT / "paper" / PDF_NAME
    assert pdf.exists()
    assert pdf.stat().st_size > 100000