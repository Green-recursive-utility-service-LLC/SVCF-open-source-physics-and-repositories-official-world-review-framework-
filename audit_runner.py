"""
audit_runner.py — GRUS Audit Pipeline Top-Level Orchestrator
Specification: GRUS-STD-001-v1.0 Section 3
Runs all ten stages in order. Halts on first failure with a structured
failure report. On full pass, issues the validated-fact certification.
Published by: Green Recursive Utility Service LLC
"""
import sys, os, argparse, json
from datetime import datetime, timezone
import yaml

# Local imports (this file lives alongside the others in grus_audit_engine/)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifest_parser import parse_manifest
from constants_validator import validate_constants
from doi_resolver import resolve_doi
from dataset_fetcher import fetch_all_datasets
from verify_executor import execute_verify
from residual_comparator import compare_residuals
from closure_tester import test_closure
from falsification_validator import validate_all_falsifications
from hasher import compute_hashes
from certifier import issue_certification
from ledger_publisher import publish_to_ledger
from cross_reference_engine import generate_citation_manifest, write_citation_manifest

def next_audit_id(ledger_dir: str = "./grus-ledger") -> str:
    audits_dir = os.path.join(ledger_dir, "audits")
    if not os.path.exists(audits_dir):
        return "GRUS-AUDIT-0001"
    existing = [f.replace("GRUS-AUDIT-", "").replace(".yaml", "")
                for f in os.listdir(audits_dir) if f.startswith("GRUS-AUDIT-")]
    if not existing:
        return "GRUS-AUDIT-0001"
    next_num = max(int(x) for x in existing if x.isdigit()) + 1
    return f"GRUS-AUDIT-{next_num:04d}"

def run_audit(repo_path: str, ledger_dir: str = "./grus-ledger",
              dry_run: bool = False, verbose: bool = True) -> int:
    audit_id = next_audit_id(ledger_dir)
    audit_date = datetime.now(timezone.utc).isoformat()
    if verbose:
        print(f"\n{'='*70}\n GRUS AUDIT PIPELINE — {audit_id}\n Repository: {repo_path}\n Audit date: {audit_date}\n{'='*70}\n")
    stage_results = {"audit_date": audit_date}

    # Stage 1: Manifest
    if verbose: print("[Stage 1/10] Manifest parsing...", end=" ")
    r1 = parse_manifest(repo_path)
    if not r1.passed:
        print(f"FAIL\n  Reason: {r1.failure_reason}\n  Field: {r1.failing_field}"); return 1
    print("PASS")
    manifest = r1.manifest
    stage_results["submission"] = {
        "title": manifest.get("submission_title"),
        "contributor": {"name": manifest.get("contributor_name"),
                        "type": manifest.get("contributor_type"),
                        "affiliation": manifest.get("affiliation", "")},
        "doi": manifest.get("doi"),
        "doi_timestamp": manifest.get("doi_timestamp"),
    }

    # Stage 2: Constants
    if verbose: print("[Stage 2/10] Constants validation...", end=" ")
    r2 = validate_constants(repo_path, manifest)
    if not r2.passed:
        print(f"FAIL\n  Reason: {r2.failure_reason}"); return 2
    print(f"PASS (single source: {os.path.basename(r2.constants_module_path)})")

    # Stage 3: DOI
    if verbose: print("[Stage 3/10] DOI resolution...", end=" ")
    r3 = resolve_doi(manifest.get("doi", ""), audit_date)
    if not r3.passed:
        print(f"FAIL\n  Reason: {r3.failure_reason}"); return 3
    print(f"PASS ({r3.doi})")

    # Stage 4: Datasets
    if verbose: print("[Stage 4/10] Dataset fetching...", end=" ")
    r4 = fetch_all_datasets(manifest)
    if not r4.passed:
        print(f"FAIL\n  Reason: {r4.failure_reason}"); return 4
    print(f"PASS ({len(r4.datasets)} datasets)")
    stage_results["datasets"] = r4.datasets

    # Stage 5: verify.py
    if verbose: print("[Stage 5/10] verify.py execution...", end=" ")
    r5 = execute_verify(repo_path)
    if not r5.passed:
        print(f"FAIL\n  Reason: {r5.failure_reason}"); return 5
    print(f"PASS ({r5.runtime_seconds:.1f}s)")

    # Stage 6: Residuals
    if verbose: print("[Stage 6/10] Residual comparison...", end=" ")
    r6 = compare_residuals(manifest, r5.stdout)
    if not r6.passed:
        print(f"FAIL\n  Reason: {r6.failure_reason}"); return 6
    print(f"PASS ({len(r6.matched)} matched)")
    stage_results["residual_comparison"] = {"matched": r6.matched}

    # Stage 7: Closure
    if verbose: print("[Stage 7/10] Closure testing...", end=" ")
    ledger_snapshot_path = os.path.join(ledger_dir, "ledger_snapshot.json")
    r7 = test_closure(repo_path, manifest, ledger_snapshot_path)
    if not r7.passed:
        print(f"FAIL\n  Reason: {r7.failure_reason}"); return 7
    print(f"PASS (p_after={r7.cumulative_p_after})")
    stage_results["closure"] = {"domains_closed": r7.domains_closed,
        "cumulative_p_before": r7.cumulative_p_before,
        "cumulative_p_after": r7.cumulative_p_after}

    # Stage 8: Falsification
    if verbose: print("[Stage 8/10] Falsification validation...", end=" ")
    r8 = validate_all_falsifications(manifest)
    if not r8.passed:
        print(f"FAIL\n  Reason: {r8.failure_reason}"); return 8
    print(f"PASS ({len(r8.valid_specs)} pending predictions)")
    stage_results["falsification"] = {"valid_specs": r8.valid_specs}

    # Stage 9: Hashing
    if verbose: print("[Stage 9/10] Hashing...", end=" ")
    r9 = compute_hashes(repo_path)
    if not r9.passed:
        print(f"FAIL\n  Reason: {r9.failure_reason}"); return 9
    print(f"PASS")
    stage_results["hashing"] = {"manifest_hash": r9.manifest_hash,
        "verify_py_hash": r9.verify_py_hash, "constants_py_hash": r9.constants_py_hash}

    # Stage 10: Certify
    if verbose: print("[Stage 10/10] Certification issuance...", end=" ")
    r10 = issue_certification(stage_results, audit_id)
    if not r10.passed:
        print(f"FAIL"); return 10
    print(f"VALIDATED FACT")

    # Generate citation manifest
    if verbose: print("\n[Citation] Cross-reference engine...", end=" ")
    ledger = {}
    if os.path.exists(ledger_snapshot_path):
        with open(ledger_snapshot_path) as f: ledger = json.load(f)
    cm = generate_citation_manifest(repo_path, manifest, ledger,
        domain_id=manifest.get("domain_id", f"D-{audit_id}"),
        contributor_doi=manifest.get("doi", ""),
        audit_id=audit_id, audit_date=audit_date)
    cm_path = os.path.join(repo_path, "CITATION_MANIFEST.yaml")
    write_citation_manifest(cm, cm_path)
    print(f"WRITTEN ({cm_path})")

    # Publish to ledger
    if not dry_run:
        if verbose: print("[Publish] Append to public ledger...", end=" ")
        rp = publish_to_ledger(r10.record, ledger_dir)
        if rp.passed:
            print(f"PUBLISHED\n  URL: {rp.ledger_url}")
        else:
            print(f"FAIL ({rp.failure_reason})")
    else:
        print("[Dry-run] Ledger publication skipped.")

    print(f"\n{'='*70}\n RESULT: VALIDATED FACT — {audit_id}\n Issued by: Green Recursive Utility Service LLC\n{'='*70}\n")
    return 0

def main():
    ap = argparse.ArgumentParser(description="GRUS Audit Engine")
    ap.add_argument("repo", help="Path to submission repository")
    ap.add_argument("--ledger-dir", default="./grus-ledger")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    sys.exit(run_audit(args.repo, args.ledger_dir, args.dry_run, not args.quiet))

if __name__ == "__main__":
    main()
