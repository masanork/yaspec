# YASPEC - YAML Automated Specification System

A comprehensive tool for managing software specifications using YAML-based structured documentation.

## Features

- YAML-based specification creation and management
- Automated validation of specification structure
- Multiple output format support (PDF, Word, HTML)
- Git-friendly format for version control
- Review process support
- Multilingual support (English/Japanese)

## Requirements

- Python 3.6+
- PyYAML

## Installation

```bash
pip install pyyaml
```

## Quick Start

1. Review `specification_guidelines.yaml` for system overview and best practices
2. Choose your language directory (`docs/en/` or `docs/ja/`)
3. Create your specification based on `docs/<lang>/spec_sample.yaml`
4. Add validator configuration to your spec file:
```yaml
# validator_path: spec_validator.yaml
```
5. Validate your specification:
```bash
python validate_spec.py docs/<lang>/your_spec.yaml
```

## Repository Structure

```
yaspec/
├── docs/
│   ├── en/                     # English documentation
│   │   ├── document_sample.yaml
│   │   └── spec_validator.yaml
│   └── ja/                     # Japanese documentation
│       ├── document_sample.yaml
│       └── spec_validator.yaml
├── specification_guidelines.yaml
├── validate_spec.py
└── README.md
```

## Getting Started

1. Clone the repository
2. Choose your preferred language directory (en/ja)
3. Review the document_sample.yaml in your language
4. Create your specification following the examples
5. Use validate_spec.py to verify your specifications

## License

Private Repository - All rights reserved
