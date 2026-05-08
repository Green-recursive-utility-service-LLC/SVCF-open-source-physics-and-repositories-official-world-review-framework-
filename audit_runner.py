"""GRUS Audit Pipeline — top-level orchestrator (10 stages)
Writes CITATION_MANIFEST.yaml and grus-ledger/audits/<ID>.yaml to the
repo root so GitHub Actions artifact-upload and commit-back work cleanly.
"""
import sys, os, argparse, json, yaml
from datetime import datetime, timezone

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

def next_audit_id(ledger_dir):
    audits = os.path.join(ledger_dir, "audits")
    if not os.path.exists(audits):
        return "GRUS-AUDIT-0001"
    existing = [f.replace("GRUS-AUDIT-","").replace(".yaml","")
                for f in os.listdir(audits) if f.startswith("GRUS-AUDIT-") and f.endswith(".yaml")]
    if not existing:
        return "GRUS-AUDIT-0001"
    n = max(int(x) for x in existing if x.isdigit()) + 1
    return f"GRUS-AUDIT-{n:04d}"

def run_audit(repo_path, ledger_dir=None, dry_run=False, verbose=True,
              private_key_path=None, allow_ephemeral=False):
    repo_path = os.path.abspath(repo_path)
    if ledger_dir is None:
        ledger_dir = os.path.join(repo_path, "grus-ledger")
    ledger_dir = os.path.abspath(ledger_dir)
    audit_id = next_audit_id(ledger_dir)
    audit_date = datetime.now(timezone.utc).isoformat()

    if verbose:
        print(f"\n{'='*70}\n GRUS AUDIT PIPELINE — {audit_id}\n Repository: {repo_path}\n Ledger:     {ledger_dir}\n Audit date: {audit_date}\n{'='*70}\n")

    sr = {"audit_date": audit_date}

    if verbose: print("[Stage 1/10] Manifest parsing...", end=" ")
    r = parse_manifest(repo_path)
    if not r.passed: print(f"FAIL\n  {r.failure_reason}"); return 1
    print("PASS"); m = r.manifest
    sr["submission"] = {"title": m.get("submission_title"),
                         "contributor": {"name": m.get("contributor_name"),
                                         "type": m.get("contributor_type"),
                                         "affiliation": m.get("affiliation","")},
                         "doi": m.get("doi"),
                         "doi_timestamp": m.get("doi_timestamp")}

    if verbose: print("[Stage 2/10] Constants validation...", end=" ")
    r = validate_constants(repo_path, m)
    if not r.passed: print(f"FAIL\n  {r.failure_reason}"); return 2
    print(f"PASS ({os.path.basename(r.constants_module_path)})")

    if verbose: print("[Stage 3/10] DOI resolution...", end=" ")
    r = resolve_doi(m.get("doi",""), audit_date)
    if not r.passed: print(f"FAIL\n  {r.failure_reason}"); return 3
    print(f"PASS ({r.doi})")

    if verbose: print("[Stage 4/10] Dataset fetching...", end=" ")
    r = fetch_all_datasets(m)
    if not r.passed: print(f"FAIL\n  {r.failure_reason}"); return 4
    print(f"PASS ({len(r.datasets)} datasets)"); sr["datasets"] = r.datasets

    if verbose: print("[Stage 5/10] verify.py execution...", end=" ")
    r = execute_verify(repo_path)
    if not r.passed: print(f"FAIL\n  {r.failure_reason}\n{r.stdout}\n{r.stderr}"); return 5
    print(f"PASS ({r.runtime_seconds:.1f}s)")
    verify_stdout = r.stdout

    if verbose: print("[Stage 6/10] Residual comparison...", end=" ")
    r = compare_residuals(m, verify_stdout)
    if not r.passed: print(f"FAIL\n  {r.failure_reason}"); return 6
    print(f"PASS ({len(r.matched)} matched)")

    if verbose: print("[Stage 7/10] Closure testing...", end=" ")
    r = test_closure(repo_path, m, os.path.join(ledger_dir, "ledger_snapshot.json"))
    if not r.passed: print(f"FAIL\n  {r.failure_reason}"); return 7
    print(f"PASS (p_after={r.cumulative_p_after})")

    if verbose: print("[Stage 8/10] Falsification validation...", end=" ")
    r = validate_all_falsifications(m)
    if not r.passed: print(f"FAIL\n  {r.failure_reason}"); return 8
    print("PASS")

    if verbose: print("[Stage 9/10] Hashing...", end=" ")
    r = compute_hashes(repo_path)
    if not r.passed: print(f"FAIL\n  {r.failure_reason}"); return 9
    print("PASS"); sr["hashing"] = {"manifest_hash": r.manifest_hash,
                                     "verify_py_hash": r.verify_py_hash,
                                     "constants_py_hash": r.constants_py_hash}

    if verbose: print("[Stage 10/10] Certification issuance...", end=" ")
    r10 = issue_certification(sr, audit_id, private_key_path=private_key_path,
                               allow_ephemeral=allow_ephemeral)
    if not r10.passed: print(f"FAIL\n  {r10.failure_reason}"); return 10
    kind = "EPHEMERAL" if r10.is_ephemeral else "CANONICAL"
    print(f"VALIDATED FACT ({kind})")

    # Write CITATION_MANIFEST.yaml to repo root (stable absolute path)
    if verbose: print("\n[Citation] Cross-reference engine...", end=" ")
    cm = generate_citation_manifest(repo_path, m, {}, m.get("domain_id", f"D-{audit_id}"),
                                     m.get("doi",""), audit_id, audit_date)
    cm_path = os.path.join(repo_path, "CITATION_MANIFEST.yaml")
    write_citation_manifest(cm, cm_path)
    print(f"WRITTEN ({cm_path})")

    # Always publish to ledger directory (used to be conditional on dry_run; we
    # want every successful audit to leave a record file the workflow can commit)
    if verbose: print("[Publish] Append to public ledger...", end=" ")
    rp = publish_to_ledger(r10.record, ledger_dir)
    if rp.passed:
        print(f"PUBLISHED ({rp.ledger_entry_path})")
    else:
        print(f"FAIL ({rp.failure_reason})")

    # Write a top-level result summary file the workflow can also upload
    result_path = os.path.join(repo_path, "grus_audit_result.yaml")
    summary = {
        "audit_id": audit_id,
        "audit_date": audit_date,
        "result": "VALIDATED FACT",
        "seal_type": "ephemeral" if r10.is_ephemeral else "canonical",
        "ledger_entry": rp.ledger_entry_path if rp.passed else None,
        "citation_manifest": cm_path,
        "issued_by": "Green Recursive Utility Service LLC",
    }
    with open(result_path, "w") as f:
        yaml.safe_dump(summary, f, sort_keys=False, default_flow_style=False)
    if verbose: print(f"[Summary] Result file written ({result_path})")

    print(f"\n{'='*70}\n RESULT: VALIDATED FACT — {audit_id}\n Issued by: Green Recursive Utility Service LLC\n{'='*70}\n")
    return 0

def main():
    ap = argparse.ArgumentParser(description="GRUS Audit Engine")
    ap.add_argument("repo")
    ap.add_argument("--ledger-dir", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--private-key", default=None)
    ap.add_argument("--allow-ephemeral", action="store_true")
    args = ap.parse_args()
    sys.exit(run_audit(args.repo, args.ledger_dir, args.dry_run, not args.quiet,
                       private_key_path=args.private_key, allow_ephemeral=args.allow_ephemeral))

if __name__ == "__main__":
    main()
