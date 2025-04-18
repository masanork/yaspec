# yspec - YAML仕様書管理ツール

YAMLベースの仕様書管理ツールです。仕様書の作成、検証、変換を支援します。

## 機能

- YAML形式での仕様書作成
- バリデーションによる仕様書の検証
- 複数フォーマット（PDF, Word, HTML）への変換サポート
- Git管理との高い親和性

## 必要要件

- Python 3.6以上
- PyYAML

## インストール

```bash
pip install pyyaml
```

## 使用方法

### 仕様書の作成

1. 仕様書YAMLファイルを作成します
2. ファイルの先頭に使用するバリデータを指定します：
```yaml
# validator_path: spec_validator.yaml
```

### 仕様書の検証

```bash
python validate_spec.py your_spec.yaml
```

バリデータは仕様書ファイル内のコメントから自動的に読み取られます。

## ファイル構成

- `仕様書規約.yaml` - 仕様書作成の規約
- `spec_validator.yaml` - 仕様書のバリデーション定義
- `spec_sample.yaml` - サンプル仕様書
- `validate_spec.py` - バリデーションスクリプト
- `document_sample.yaml` - 長文対応サンプル

## ライセンス

プライベートリポジトリ - All rights reserved
