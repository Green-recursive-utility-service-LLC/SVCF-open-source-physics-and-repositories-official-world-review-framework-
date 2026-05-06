"""
grus_constants.py
=================
Green Recursive Utility Service LLC — Audit Engine Constants
Specification: GRUS-CRX-001-v1.0
Public charter: GRUS-01

This module is the single source of truth for the GRUS audit pipeline
configuration. The audit engine imports from this module only; nothing
is hardcoded outside it.

Published by: Green Recursive Utility Service LLC
State of Texas LLC | Filed May 5, 2026
"""

# ─── LLC IDENTITY ──────────────────────────────────────────────────────
LLC_NAME = "Green Recursive Utility Service LLC"
LLC_STATE = "Texas"
LLC_FILING_DATE = "2026-05-05"
LLC_PRINCIPAL_OFFICE = "Weatherford, Texas, USA"

# ─── AUDIT PIPELINE VERSION ────────────────────────────────────────────
AUDIT_PIPELINE_VERSION = "1.0"
CERTIFICATION_STANDARD = "GRUS-STD-001-v1.0"
ENGINE_REPOSITORY = "github.com/grus-utility/grus-audit-engine"

# ─── CRYPTOGRAPHIC KEY LOCATIONS ───────────────────────────────────────
GRUS_PUBLIC_KEY_CANONICAL = "https://grus.utility/public-key"
GRUS_PUBLIC_KEY_MIRRORS = [
    "https://github.com/grus-utility/public-key",
    "https://zenodo.org/communities/grus-utility",
    "https://web.archive.org/web/grus.utility/public-key",
]

# ─── PUBLIC LEDGER LOCATIONS ───────────────────────────────────────────
LEDGER_CANONICAL_URL = "https://ledger.grus.utility"
LEDGER_GITHUB_MIRROR = "https://github.com/grus-utility/grus-ledger"
LEDGER_ZENODO_COMMUNITY = "grus-ledger"
LEDGER_INTERNET_ARCHIVE = "https://web.archive.org/web/ledger.grus.utility"

# ─── SVCF FOUNDATION REFERENCES (PRESERVED, NOT MODIFIED) ─────────────
# These are public-archive repositories. The LLC validates and certifies them
# but does not modify, relocate, or rebrand them.
SVCF_FOUNDATION_REPO = "<inaugural_certification_target_repository_url>"
SVCF_PRIORITY_ANCHOR = "rxiVerse:2602.0018"
SVCF_PRIORITY_DATE = "2025-11-16"
SVCF_FOUNDATION_DOIS = [
    "10.5281/zenodo.18604376",
    "10.5281/zenodo.18848748",
    "10.5281/zenodo.198940",
]
SVCF_CODE_RELEASE = "rxiVerse:2604.0118"
SVCF_CODE_RELEASE_DATE = "2026-04-29"
SVCF_FOUNDATIONAL_AUDIT_ID = "GRUS-AUDIT-0001"

# ─── EIGHT LOCKED CONSTANTS (SVCF FOUNDATION — IMMUTABLE) ──────────────
# Imported reference only. The audit pipeline reads these from the
# submission's svcf_constants.py and verifies they match these exact values.
EXPECTED_CONSTANTS = {
    "GAMMA": {"value": "1.0/2857.0", "type": "MEASURED",
              "source": "STAR Λ-Λ̄ vorticity, Au+Au √sNN=200 GeV, Nature 2026"},
    "B": {"value": "32.0/33.0", "type": "EXACT",
          "source": "BRST: B = (N-5)/(N-4) at N=37"},
    "BETA": {"value": "65.0/66.0", "type": "EXACT",
             "source": "Law #1: β = (B+1)/2"},
    "PSI": {"value": "sqrt(2.0) - 1.0", "type": "EXACT",
            "source": "37D → 4D S²⁴ projection integral"},
    "K_TD": {"value": "37 * 300", "type": "EXACT",
             "source": "37 × C(25,2) = 11100"},
    "K_MODE": {"value": "9", "type": "EXACT",
               "source": "St-Jean photonic Chern insulator (PRX 2026)"},
    "RHO_C": {"value": "1.01e-26", "type": "MEASURED",
              "source": "H₀=70 km/s/Mpc, Friedmann critical-density relation"},
    "ETA": {"value": "6.8e-28", "type": "MEASURED",
            "source": "CHIME FRB pulse-broadening slope"},
    "EPSILON": {"value": "ALPHA**2 = 5.3251e-5", "type": "DERIVED",
                "source": "Law #2: double-vertex EM coupling"},
}

# ─── AUDIT PIPELINE STAGES ─────────────────────────────────────────────
PIPELINE_STAGES = [
    "manifest_parsing",
    "constants_validation",
    "doi_resolution",
    "dataset_fetching",
    "verify_execution",
    "residual_comparison",
    "closure_testing",
    "falsification_validation",
    "hashing",
    "certification_issuance",
]

# ─── DATA INTEGRITY CLAUSES ────────────────────────────────────────────
INTEGRITY_CLAUSES = {
    "clause_1_zero_free_parameters": "All constants either EXACT or MEASURED with cited source",
    "clause_2_zero_placeholders": "No undeclared or 'to be determined' values",
    "clause_3_public_data_reproducibility": "Verification reproduces against public datasets",
    "clause_4_overconstrained_closure": "Same constants close all touched domains",
    "clause_5_forward_facing_falsification": "Predictions have explicit falsification conditions",
    "clause_6_immutable_public_timestamping": "Submission deposited at public archive with DOI",
}

# ─── RESIDUAL TOLERANCE ────────────────────────────────────────────────
TOLERANCE_RELATIVE_PCT = 1.0  # residuals must match to within 1% relative
TOLERANCE_ABSOLUTE_SIGMA = 0.05  # or 0.05σ absolute, whichever is more permissive

# ─── COMPLIANCE FRAMING ────────────────────────────────────────────────
COMPLIANCE_MANDATES = {
    "EO_14303": "Restoring Gold Standard Science (May 23, 2025)",
    "OSTP_NELSON_MEMO": "Free, Immediate, and Equitable Access to Federally Funded Research (2022/2026)",
    "DATA_INTEGRITY_ACT": "Deterministic gradient validation, zero-proxy execution",
}


def print_config():
    """Print the LLC audit pipeline configuration."""
    print("=" * 70)
    print(f" {LLC_NAME}")
    print(f" Audit Pipeline Configuration v{AUDIT_PIPELINE_VERSION}")
    print("=" * 70)
    print()
    print(f" SVCF Foundation (preserved as filed):")
    print(f"   Author: {SVCF_AUTHOR}")
    print(f"   Repository: {SVCF_FOUNDATION_REPO}")
    print(f"   Priority anchor: {SVCF_PRIORITY_ANCHOR} ({SVCF_PRIORITY_DATE})")
    print(f"   Code release: {SVCF_CODE_RELEASE} ({SVCF_CODE_RELEASE_DATE})")
    print()
    print(f" LLC Audit Engine:")
    print(f"   Repository: {ENGINE_REPOSITORY}")
    print(f"   Standard: {CERTIFICATION_STANDARD}")
    print(f"   Pipeline stages: {len(PIPELINE_STAGES)}")
    print(f"   Integrity clauses: {len(INTEGRITY_CLAUSES)}")
    print()
    print(f" Compliance:")
    for k, v in COMPLIANCE_MANDATES.items():
        print(f"   {k}: {v}")
    print()
    print(f" Public ledger: {LEDGER_CANONICAL_URL}")
    print(f" Public key: {GRUS_PUBLIC_KEY_CANONICAL}")
    print()


if __name__ == "__main__":
    print_config()
