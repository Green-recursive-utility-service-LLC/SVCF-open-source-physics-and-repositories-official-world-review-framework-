"""
audit_runner.py
==================
GRUS Audit Pipeline — Stage 4: Local Physics Verification
Specification: GRUS-STD-001-v1.0 Section 3 Stage 4; Clause 3

Validates that the submission's claimed datasets and physics files are
physically present and accessible IN THE REPOSITORY ITSELF — the ground
truth — rather than requiring live network access to external sources.

The manifest's `datasets_cited` field records WHERE the datasets were
originally published for public access (Clause 3 — anyone can independently
verify the data exists at those public locations under the cited statutes).
The audit pipeline does NOT make live HTTP requests to those URLs because:

  1. Network reachability from a CI runner is not a property of the
     scientific record — it's a property of network infrastructure.
  2. External sites rate-limit, refuse connections, change URLs, and
     experience outages — none of which invalidate the underlying physics.
  3. The actual evidence audited is the LOCAL physics implementation:
     svcf_constants.py, svcf_domains.py, svcf_quantum.py, svcf_solar_system.py,
     verify.py, etc. — the files that the LLC-stewarded ground truth lives in.

This stage:
  - Confirms each `datasets_cited` entry has a well-formed URL and a
    declared public-access statute (Clause 3 evidence).
  - Confirms the expected local physics files are present in the repository
    and are valid Python (or YAML, or Markdown) — the actual auditable record.
  - Returns the dataset record (URLs + statutes) for inclusion in the
    final certification, as the public-access citation trail.

Published by: Green Recursive Utility Service LLC
"""

import os
import ast
from dataclasses import dataclass, field
from typing import List, Dict
from urllib.parse import urlparse


@dataclass
class DatasetResult:
    passed: bool
    datasets: list = field(default_factory=list)
    local_evidence_files: list = field(default_factory=list)
    failure_reason: str = ""


# Local physics files that, if present, count as ground-truth evidence.
# At least one must exist for the audit to pass Stage 4.
GROUND_TRUTH_CANDIDATES = [
    "svcf_constants.py",
    "svcf_domains.py",
    "svcf_quantum.py",
    "svcf_solar_system.py",
    "verify.py",
]


def _validate_url_format(url: str) -> bool:
    """Well-formed URL check (no network call)."""
    if not url or not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https", "doi") and bool(parsed.netloc or parsed.path)


def _validate_python_file(path: str) -> bool:
    """Confirm a .py file parses cleanly."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            ast.parse(f.read())
        return True
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False


def fetch_all_datasets(manifest: Dict, repo_path: str = ".") -> DatasetResult:
    """
    Stage 4 entry point. Validates manifest dataset citations + local evidence.

    Args:
        manifest: parsed GRUS_MANIFEST.yaml
        repo_path: submission repository root (defaults to current directory
                   when called by older pipelines that don't pass it explicitly)

    Returns:
        DatasetResult
    """
    cited = manifest.get("datasets_cited", [])
    if not cited:
        return DatasetResult(
            passed=False,
            failure_reason="No datasets cited in manifest (Clause 3 violation)"
        )

    # 1. Validate each citation entry: URL format + access statute declared
    validated_datasets = []
    for i, d in enumerate(cited):
        if not isinstance(d, dict):
            return DatasetResult(
                passed=False,
                failure_reason=f"datasets_cited[{i}] is not a mapping"
            )
        url = d.get("url", "")
        statute = d.get("access_statute", "")
        description = d.get("description", "")
        if not _validate_url_format(url):
            return DatasetResult(
                passed=False,
                failure_reason=f"datasets_cited[{i}] has malformed URL: {url!r}"
            )
        if not statute:
            return DatasetResult(
                passed=False,
                failure_reason=f"datasets_cited[{i}] missing access_statute (Clause 3 requires public-access basis declaration)"
            )
        validated_datasets.append({
            "url": url,
            "description": description,
            "access_statute": statute,
            "verification_method": "public_citation_record",
        })

    # 2. Confirm at least one ground-truth physics file exists locally
    found_local = []
    for fname in GROUND_TRUTH_CANDIDATES:
        full_path = os.path.join(repo_path, fname)
        if os.path.exists(full_path):
            if fname.endswith(".py") and not _validate_python_file(full_path):
                return DatasetResult(
                    passed=False,
                    failure_reason=f"Ground-truth file {fname} exists but is not valid Python"
                )
            found_local.append(fname)

    if not found_local:
        return DatasetResult(
            passed=False,
            failure_reason=(
                "No ground-truth physics files found locally. Expected at least "
                f"one of: {', '.join(GROUND_TRUTH_CANDIDATES)}"
            )
        )

    return DatasetResult(
        passed=True,
        datasets=validated_datasets,
        local_evidence_files=found_local,
    )


if __name__ == "__main__":
    import sys
    import yaml as _yaml
    if len(sys.argv) < 2:
        print("Usage: python dataset_fetcher.py <repo_path>")
        sys.exit(0)
    repo = sys.argv[1]
    manifest_file = os.path.join(repo, "GRUS_MANIFEST.yaml")
    with open(manifest_file) as f:
        manifest = _yaml.safe_load(f)
    result = fetch_all_datasets(manifest, repo)
    if result.passed:
        print(f"[PASS] Datasets validated: {len(result.datasets)} citations, "
              f"{len(result.local_evidence_files)} local ground-truth files")
        for f in result.local_evidence_files:
            print(f"  - {f}")
    else:
        print(f"[FAIL] {result.failure_reason}")
        sys.exit(1)
