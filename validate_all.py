#!/usr/bin/env python3
"""
YASPEC Document Validator
========================
This script validates all YAML specification files in the project.
It's designed to be used as a pre-commit check to ensure document consistency.

Usage:
    python validate_all.py [--strict]

Options:
    --strict    Exit with error if any warnings are found
"""

import os
import sys
import glob
from validate_spec import validate, load_yaml, extract_validator_path, resolve_validator_path

def find_yaml_files(directory):
    """Find all YAML files in the given directory and its subdirectories"""
    yaml_files = []
    for ext in ['yaml', 'yml']:
        yaml_files.extend(glob.glob(f"{directory}/**/*.{ext}", recursive=True))
    return yaml_files

def validate_file(file_path, strict=False):
    """Validate a single YAML file"""
    try:
        # Skip validator files
        if file_path.endswith('spec_validator.yaml'):
            return True, []

        print(f"\nValidating: {file_path}")
        validator_path = extract_validator_path(file_path)
        
        if not validator_path:
            print(f"[SKIP] No validator_path specified in {file_path}")
            return True, []
        
        # Resolve validator path based on language
        validator_path = resolve_validator_path(validator_path, file_path)
        
        if not os.path.exists(validator_path):
            print(f"[ERROR] Validator not found: {validator_path}")
            return False, [f"Validator not found: {validator_path}"]
        
        doc = load_yaml(file_path)
        rules = load_yaml(validator_path)
        errors = validate(doc, rules)
        
        if errors:
            print("[VALIDATION FAILED]")
            for error in errors:
                print(f"- {error}")
            return False, errors
        else:
            print("[VALIDATION PASSED]")
            return True, []
            
    except Exception as e:
        print(f"[ERROR] Failed to validate {file_path}: {str(e)}")
        return False, [str(e)]

def main():
    strict = '--strict' in sys.argv
    
    # Get project root directory
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all YAML files
    yaml_files = find_yaml_files(root_dir)
    if not yaml_files:
        print("No YAML files found")
        sys.exit(0)
    
    # Validate each file
    all_passed = True
    all_errors = []
    
    print(f"Found {len(yaml_files)} YAML files to validate")
    
    for file_path in yaml_files:
        passed, errors = validate_file(file_path, strict)
        if not passed:
            all_passed = False
            all_errors.extend(errors)
    
    # Summary
    print("\n=== Validation Summary ===")
    print(f"Total files checked: {len(yaml_files)}")
    print(f"Validation {'PASSED' if all_passed else 'FAILED'}")
    if all_errors:
        print(f"Total errors found: {len(all_errors)}")
    
    # Exit with appropriate status
    if not all_passed:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
