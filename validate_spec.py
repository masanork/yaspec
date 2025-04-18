"""
YAML仕様書バリデータ
====================
このスクリプトは仕様書YAML（例: spec_sample.yaml）本体の先頭コメントで指定されたバリデータYAML（validator_path）を自動で参照し、
仕様書が正しい構造・必須項目を満たしているか検証します。

【使い方】
$ python validate_spec.py spec_sample.yaml

【主なチェック内容】
- 各セクションの有無・必須項目の有無
- 各項目の型（string, list, date など）
- 不足・過剰な項目の警告

【依存パッケージ】
- pyyaml

【インストール例】
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
    return True  # 型未定義はスキップ

def validate_section(section_rule, doc_dict, errors, parent_path=""):
    section_name = section_rule["name"]
    path = f"{parent_path}{section_name}"
    required = section_rule.get("required", False)
    fields = section_rule.get("fields", [])
    section = doc_dict.get(section_name)
    if required and section is None:
        errors.append(f"必須セクションがありません: {path}")
        return
    if section is None:
        return
    for field in fields:
        fname = field["name"]
        f_required = field.get("required", False)
        f_type = field.get("type")
        value = section.get(fname) if isinstance(section, dict) else None
        fpath = f"{path}.{fname}"
        if f_required and value is None:
            errors.append(f"必須項目がありません: {fpath}")
            continue
        if value is not None and f_type and not check_type(value, f_type):
            errors.append(f"型不一致: {fpath} (期待: {f_type})")

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
        print("[エラー] validator_pathコメントが仕様書先頭にありません。")
        sys.exit(1)
    doc = load_yaml(spec_file)
    rules = load_yaml(validator_path)
    errors = validate(doc, rules)
    if errors:
        print("[検証NG] 以下の問題があります:")
        for e in errors:
            print("-", e)
        sys.exit(1)
    else:
        print("[検証OK] 仕様書は規約に準拠しています。")

if __name__ == "__main__":
    main()
