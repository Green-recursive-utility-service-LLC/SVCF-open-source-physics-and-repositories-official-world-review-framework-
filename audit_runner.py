"""
constants_validator.py
======================
GRUS Audit Pipeline — Stage 2: Constants Validation
Enforces the "Single Source of Truth" (SSOT) architecture.
"""

import os
import re
import importlib.util
from typing import List

# The symbols that must be locked and imported, never hardcoded.
PROTECTED_SYMBOLS = ["GAMMA", "B", "BETA", "PSI", "K_TD", "K_MODE", "RHO_C", "ETA"]

class ConstantsValidationResult:
    def __init__(self, passed: bool, failure_reason: str = "", constants_module_path: str = ""):
        self.passed = passed
        self.failure_reason = failure_reason
        self.constants_module_path = constants_module_path

def validate_constants(repo_path: str, manifest: dict) -> ConstantsValidationResult:
    # 1. Identify the Source of Truth
    source_file = "svcf_constants.py"
    source_path = os.path.join(repo_path, source_file)

    if not os.path.exists(source_path):
        return ConstantsValidationResult(False, f"Source of Truth '{source_file}' not found.")

    # 2. Scan for violations (hardcoded assignments in WRONG files)
    violations = []
    # Pattern looks for 'SYMBOL =' but ignores 'from ... import SYMBOL'
    assignment_pattern = re.compile(r'^\s*(?:' + '|'.join(PROTECTED_SYMBOLS) + r')\s*=', re.MULTILINE)

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py") and file != source_file:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if assignment_pattern.search(content):
                        violations.append(file)

    if violations:
        return ConstantsValidationResult(
            False, 
            f"Hardcoded SVCF foundation values detected outside {source_file} in: {', '.join(violations)}. "
            "Please use 'from svcf_constants import ...' instead."
        )

    # 3. Final Verification: Does the Source of Truth actually contain the math?
    try:
        spec = importlib.util.spec_from_file_location("svcf_constants", source_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        for symbol in PROTECTED_SYMBOLS:
            if not hasattr(module, symbol):
                return ConstantsValidationResult(False, f"Immutable constant {symbol} missing from {source_file}.")
    except Exception as e:
        return ConstantsValidationResult(False, f"Internal error loading constants: {str(e)}")

    return ConstantsValidationResult(True, constants_module_path=source_path)
