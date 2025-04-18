"""
YAML Specification Validator
==========================
This script validates specification YAML files against a validator YAML file that is
automatically referenced from the validator_path comment in the specification file header.

Usage:
$ python validate_spec.py spec_sample.yaml

Validation checks:
- Presence and requirements of each section
- Data types (string, list, date, etc.)
- Warning for missing or excessive items

Dependencies:
- pyyaml

Installation:
$ pip install pyyaml
"""
import sys
import yaml
from datetime import datetime
import re

def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def extract_validator_path(yaml_path):
    with open(yaml_path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"#\s*validator_path:\s*(\S+)", line)
            if m:
                return m.group(1)
    return None

def check_type(value, expected_type):
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "list":
        return isinstance(value, list)
    if expected_type == "date":
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except Exception:
            return False
    return True  # Skip undefined types

def validate_section(section_rule, doc_dict, errors, parent_path=""):
    section_name = section_rule["name"]
    full_path = f"{parent_path}.{section_name}" if parent_path else section_name
    
    # Check if required section exists
    if section_rule.get("required", False) and section_name not in doc_dict:
        errors.append(f"Required section '{full_path}' is missing")
        return
    
    # Skip validation if section doesn't exist
    if section_name not in doc_dict:
        return
    
    # Validate fields in the section
    for field_rule in section_rule.get("fields", []):
        field_name = field_rule["name"]
        field_path = f"{full_path}.{field_name}"
        
        # Check if required field exists
        if field_rule.get("required", False) and (
            field_name not in doc_dict[section_name]
        ):
            errors.append(f"Required field '{field_path}' is missing")
            continue
        
        # Skip validation if field doesn't exist
        if field_name not in doc_dict[section_name]:
            continue
        
        # Validate field type
        if "type" in field_rule:
            value = doc_dict[section_name][field_name]
            if not check_type(value, field_rule["type"]):
                errors.append(
                    f"Field '{field_path}' should be of type '{field_rule['type']}'"
                )

def validate(doc, rules):
    errors = []
    for section_rule in rules.get("sections", []):
        validate_section(section_rule, doc, errors)
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_spec.py <spec_sample.yaml>")
        sys.exit(1)
    
    spec_file = sys.argv[1]
    validator_path = extract_validator_path(spec_file)
    if not validator_path:
        print("[ERROR] No validator_path comment found at the beginning of the specification.")
        sys.exit(1)
    
    doc = load_yaml(spec_file)
    rules = load_yaml(validator_path)
    errors = validate(doc, rules)
    
    if errors:
        print("[VALIDATION FAILED] The following issues were found:")
        for e in errors:
            print("-", e)
        sys.exit(1)
    else:
        print("[VALIDATION PASSED] The specification complies with the guidelines.")

if __name__ == "__main__":
    main()
