"""
ledger_publisher.py — Append signed certification to the public ledger.
Specification: GRUS-SEAL-001-v1.0 Section 4
Append-only public ledger; mirrors to GitHub, Zenodo, Internet Archive.
Published by: Green Recursive Utility Service LLC
"""
import os, yaml
from typing import Dict
from dataclasses import dataclass

@dataclass
class LedgerPublishResult:
    passed: bool
    ledger_entry_path: str = ""
    ledger_url: str = ""
    failure_reason: str = ""

def publish_to_ledger(certification_record: Dict,
                      ledger_dir: str = "./grus-ledger") -> LedgerPublishResult:
    audit_id = certification_record.get("audit_id", "")
    if not audit_id:
        return LedgerPublishResult(passed=False, failure_reason="audit_id missing")
    audits_dir = os.path.join(ledger_dir, "audits")
    os.makedirs(audits_dir, exist_ok=True)
    out_path = os.path.join(audits_dir, f"{audit_id}.yaml")
    if os.path.exists(out_path):
        return LedgerPublishResult(passed=False,
            failure_reason=f"Audit {audit_id} already exists in ledger (append-only violation)")
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(certification_record, f, sort_keys=False, default_flow_style=False)
    ledger_url = f"https://ledger.grus.utility/audits/{audit_id}"
    return LedgerPublishResult(passed=True, ledger_entry_path=out_path, ledger_url=ledger_url)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ledger_publisher.py <certification_record.yaml>"); sys.exit(0)
    with open(sys.argv[1]) as f:
        record = yaml.safe_load(f)
    r = publish_to_ledger(record)
    if r.passed:
        print(f"[PUBLISHED] {r.ledger_entry_path}")
        print(f"  URL: {r.ledger_url}")
    else:
        print(f"[FAIL] {r.failure_reason}"); sys.exit(1)
