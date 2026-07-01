from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PDF_NAME = "Linear_Extension_Sets_and_Subgroup_Rows_in_S4_A_Finite_Witness_Separation.pdf"
CERTIFICATION_REL = "certified/PUBLIC_REPOSITORY_CERTIFICATION.json"
MANIFEST_REL = "MANIFEST_SHA256.txt"
REQUIRED_STATIC = [
    ".gitattributes",
    ".gitignore",
    "LICENSE",
    "README.md",
    "README_REVIEWER.md",
    "REPRODUCE.md",
    "CITATION.cff",
    "requirements.txt",
    "paper/main.tex",
    "paper/macros.tex",
    "paper/abstract.tex",
    "paper/references.bib",
    f"paper/{PDF_NAME}",
    "paper/sections/01_introduction.tex",
    "paper/sections/02_s4_indexing_and_prefix_support.tex",
    "paper/sections/03_selected_s4_atlas.tex",
    "paper/sections/04_common_precedence_and_poset_cones.tex",
    "paper/sections/05_d4_v4_coset_rows.tex",
    "paper/sections/06_n_poset_boundary_example.tex",
    "paper/sections/07_selected_structural_comparison.tex",
    "paper/sections/08_boundaries_and_nonclaims.tex",
    "paper/sections/09_related_work.tex",
    "paper/sections/10_conclusion.tex",
    "paper/appendices/A_replay_and_schema.tex",
    "paper/appendices/B_selected_witness_tables.tex",
    "results/s4_bridge_table.json",
    "results/s4_selected_atlas.json",
    "results/s4_structural_comparison.json",
    "results/s4_structural_comparison.csv",
    "certified/s4_bridge_table_certificate.json",
    "certified/s4_d4_v4_rows_certificate.json",
    "certified/s4_selected_atlas_expected_counts.yaml",
    "certified/s4_selected_atlas_independent_certificate.json",
    "certified/s4_selected_atlas_row_certificate.json",
    "certified/s4_structural_comparison_certificate.json",
    "certified/replay_hashes.sha256",
    "tables/s4_selected_witness_comparison.md",
    "scripts/replay_all.py",
    "scripts/check_public_package.py",
    "tests/test_public_package.py",
    "tests/test_mathematical_core.py",
    "docs/CLAIM_BOUNDARY.md",
    "docs/REPLAY_BOUNDARY.md",
    "docs/SOURCE_AND_BIBLIOGRAPHY_NOTES.md",
    "docs/PUBLIC_PACKAGE_MANIFEST.md",
    ".github/workflows/replay.yml",
]
HASHED_REPLAY = [
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
TEXT_SUFFIXES = {".bib", ".cff", ".csv", ".json", ".md", ".py", ".tex", ".txt", ".yaml", ".yml"}
TEXT_NAMES = {".gitattributes", ".gitignore", "LICENSE"}
LOCAL_PATH_TOKENS = ["P:" + "\\", "C:" + "\\" + "Users" + "\\"]
NONPACKAGE_MARKERS = [
    "P" + "01",
    "P" + "02",
    "P" + "03",
    "F" + "CIG",
    "P" + "APP",
    "source" + " " + "card",
    "source" + "-" + "card",
    "public" + "-ready",
    "public" + "-promotion",
    "Prossima" + " task",
    "MASTER" + "_MAP",
    "Finite Centered" + " Incidence Geometry",
    "leg" + "acy" + "_quarantine",
]
CITE_RE = re.compile(r"\\(?:[A-Za-z]*cite[A-Za-z*]*|cite)\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]+)\}")
EXPECTED_REMOTE_SUBSTRING = "github.com/aconsciousfractal/Linear-Extension-Sets-and-Subgroup-Rows-in-S4-A-Finite-Witness-Separation"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add(checks: list[dict[str, Any]], check_id: str, expected: Any, observed: Any) -> None:
    checks.append({"id": check_id, "expected": expected, "observed": observed, "passed": expected == observed})


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES


def text_files() -> list[Path]:
    out = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or not is_text_file(path):
            continue
        out.append(path)
    return out


def citation_keys_from_tex() -> set[str]:
    keys: set[str] = set()
    for path in (ROOT / "paper").rglob("*.tex"):
        text = path.read_text(encoding="utf-8")
        for match in CITE_RE.finditer(text):
            keys.update(k.strip() for k in match.group(1).split(",") if k.strip())
    return keys


def bib_keys() -> set[str]:
    text = (ROOT / "paper" / "references.bib").read_text(encoding="utf-8")
    return set(re.findall(r"@\w+\{\s*([^,\s]+)", text))


def replay_hash_entries() -> dict[str, str]:
    path = ROOT / "certified" / "replay_hashes.sha256"
    if not path.exists():
        return {}
    entries = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(maxsplit=1)
        entries[rel.strip()] = digest.strip()
    return entries


def package_manifest_files() -> list[Path]:
    excluded_names = {MANIFEST_REL, "PUBLIC_REPOSITORY_CERTIFICATION.json"}
    excluded_suffixes = {".aux", ".bbl", ".blg", ".log", ".out", ".toc", ".fls", ".fdb_latexmk", ".gz"}
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts or ".pytest_cache" in path.parts:
            continue
        if path.name in excluded_names or path.suffix.lower() in excluded_suffixes:
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix())


def computed_package_manifest_text() -> str:
    lines = ["# SHA-256 manifest", ""]
    for path in package_manifest_files():
        rel = path.relative_to(ROOT).as_posix()
        lines.append(f"{sha256(path)}  {rel}")
    return "\n".join(lines) + "\n"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def git_remote_public_violations() -> list[str]:
    if not (ROOT / ".git").exists():
        return []
    completed = subprocess.run(
        ["git", "remote", "-v"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return [f"git remote -v failed with exit code {completed.returncode}"]
    violations: list[str] = []
    for line in completed.stdout.splitlines():
        clean = line.strip()
        if not clean:
            continue
        normalized = clean.replace(":", "/").lower()
        if EXPECTED_REMOTE_SUBSTRING.lower() not in normalized:
            violations.append(clean)
    return sorted(violations)


def run_checks(*, check_manifest: bool, require_certification: bool) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for rel in REQUIRED_STATIC:
        add(checks, f"exists:{rel}", True, (ROOT / rel).is_file())
    if require_certification:
        add(checks, f"exists:{CERTIFICATION_REL}", True, (ROOT / CERTIFICATION_REL).is_file())

    pdf = ROOT / "paper" / PDF_NAME
    add(checks, "pdf.min_size", True, pdf.exists() and pdf.stat().st_size > 100000)

    cite = citation_keys_from_tex()
    bib = bib_keys()
    add(checks, "bibliography.citations_in_bib", [], sorted(cite - bib))
    add(checks, "bibliography.no_unused_bib", [], sorted(bib - cite))

    local_hits: list[str] = []
    marker_hits: list[str] = []
    replacement_hits: list[str] = []
    for path in text_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in LOCAL_PATH_TOKENS:
            if token in text:
                local_hits.append(f"{rel}:{token}")
        if "\ufffd" in text:
            replacement_hits.append(rel)
        lowered = text.lower()
        for token in NONPACKAGE_MARKERS:
            if token.lower() in lowered:
                marker_hits.append(f"{rel}:{token}")
    add(checks, "public.no_local_paths", [], local_hits)
    add(checks, "public.no_process_markers", [], marker_hits)
    add(checks, "public.no_replacement_chars", [], replacement_hits)

    entries = replay_hash_entries()
    add(checks, "replay_hash.coverage", sorted(HASHED_REPLAY), sorted(entries))
    hash_mismatches = []
    for rel, digest in entries.items():
        path = ROOT / rel
        if not path.exists():
            hash_mismatches.append({"path": rel, "reason": "missing"})
        elif sha256(path) != digest:
            hash_mismatches.append({"path": rel, "expected": digest, "actual": sha256(path)})
    add(checks, "replay_hash.matches", [], hash_mismatches)

    cert_failures = []
    for rel in CERTIFICATES:
        path = ROOT / rel
        if not path.exists():
            cert_failures.append({"path": rel, "reason": "missing"})
            continue
        payload = load_json(path)
        failed = payload.get("checks_failed", payload.get("num_failed", 0))
        if payload.get("status") != "passed" or failed != 0:
            cert_failures.append({"path": rel, "status": payload.get("status"), "failure_count": failed})
    add(checks, "certificates.passed", [], cert_failures)

    if require_certification and (ROOT / CERTIFICATION_REL).exists():
        certification = load_json(ROOT / CERTIFICATION_REL)
        add(checks, "certification.status", "passed", certification.get("status"))
        add(checks, "certification.failed", 0, certification.get("checks_failed"))
        add(checks, "certification.release_allowed", True, certification.get("public_release_allowed"))

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    boundary = (ROOT / "docs" / "CLAIM_BOUNDARY.md").read_text(encoding="utf-8") if (ROOT / "docs" / "CLAIM_BOUNDARY.md").exists() else ""
    reproduce = (ROOT / "REPRODUCE.md").read_text(encoding="utf-8") if (ROOT / "REPRODUCE.md").exists() else ""
    add(checks, "readme.has_build_commands", True, "pdflatex -jobname" in readme and "python -B scripts/replay_all.py --verify" in readme)
    add(checks, "reproduce.uses_read_only_check", True, "replay_all.py --verify" in reproduce and "check_public_package.py --check" in reproduce)
    add(checks, "boundary.has_nonclaims", True, "This package does not claim" in boundary)
    add(checks, "git.remote_public_ok", [], git_remote_public_violations())

    if check_manifest:
        manifest = ROOT / MANIFEST_REL
        add(checks, f"exists:{MANIFEST_REL}", True, manifest.is_file())
        observed = manifest.read_text(encoding="utf-8") if manifest.exists() else ""
        add(checks, "package_manifest.matches", computed_package_manifest_text(), observed)

    return checks


def result_from_checks(checks: list[dict[str, Any]]) -> dict[str, Any]:
    passed = all(item["passed"] for item in checks)
    return {
        "schema": "linear_extension_s4.public_repository_certification.v1.0",
        "status": "passed" if passed else "failed",
        "checks_total": len(checks),
        "checks_failed": sum(1 for item in checks if not item["passed"]),
        "public_release_allowed": passed,
        "owner_approval": True,
        "checks": checks,
    }


def write_text_lf(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_release_files(result: dict[str, Any]) -> None:
    out = ROOT / CERTIFICATION_REL
    write_text_lf(out, json.dumps(result, indent=2) + "\n")
    write_text_lf(ROOT / MANIFEST_REL, computed_package_manifest_text())


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify or refresh the public S4 finite-witness package certification.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="read-only verification mode (default)")
    mode.add_argument("--write", action="store_true", help="refresh certification and package manifest")
    args = parser.parse_args()

    write_mode = args.write
    if write_mode:
        result = result_from_checks(run_checks(check_manifest=False, require_certification=False))
        if result["status"] == "passed":
            write_release_files(result)
            result = result_from_checks(run_checks(check_manifest=True, require_certification=True))
            if result["status"] == "passed":
                write_release_files(result)
    else:
        result = result_from_checks(run_checks(check_manifest=True, require_certification=True))
    summary = {key: result[key] for key in ["status", "checks_total", "checks_failed", "public_release_allowed"]}
    summary["mode"] = "write" if write_mode else "check"
    print(json.dumps(summary, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())