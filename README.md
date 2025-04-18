# yspec - YAML Specification Management System

A comprehensive tool for managing software specifications using YAML-based structured documentation.

## Features

- YAML-based specification creation and management
- Automated validation of specification structure
- Multiple output format support (PDF, Word, HTML)
- Git-friendly format for version control
- Review process support

## Requirements

- Python 3.6+
- PyYAML

## Installation

```bash
pip install pyyaml
```

## Quick Start

1. Review `specification_guidelines.yaml` for system overview and best practices
2. Create your specification based on `spec_sample.yaml`
3. Add validator configuration to your spec file:
```yaml
# validator_path: spec_validator.yaml
```
4. Validate your specification:
```bash
python validate_spec.py your_spec.yaml
```

## Repository Structure

- `specification_guidelines.yaml` - Project overview and guidelines
- `spec_validator.yaml` - Validation rules definition
- `spec_sample.yaml` - Example specification
- `validate_spec.py` - Validation script
- `document_sample.yaml` - Long-form document example

## Getting Started

1. Clone the repository
2. Review `specification_guidelines.yaml` for complete documentation
3. Follow the examples in `spec_sample.yaml`
4. Use `validate_spec.py` to verify your specifications

## License

Private Repository - All rights reserved
