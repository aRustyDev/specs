# Pre-commit Configuration Guide

## Table of Contents
1. [What is Pre-commit?](#what-is-pre-commit)
2. [Why Pre-commit is Essential](#why-pre-commit-is-essential)
3. [Installation and Setup](#installation-and-setup)
4. [Common Hooks by Language](#common-hooks-by-language)
5. [Security Scanning](#security-scanning)
6. [Code Quality Checks](#code-quality-checks)
7. [Test Execution Hooks](#test-execution-hooks)
8. [Coverage Enforcement](#coverage-enforcement)
9. [Custom Hook Creation](#custom-hook-creation)
10. [CI/CD Integration](#cicd-integration)
11. [Troubleshooting](#troubleshooting)
12. [Complete Examples](#complete-examples)

## What is Pre-commit?

Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks. It's a tool that runs checks on your code before you commit it to version control, catching issues early in the development process.

### Key Concepts
- **Hooks**: Scripts that run automatically before a commit
- **Repository**: A collection of hooks (can be local or remote)
- **Configuration**: YAML file defining which hooks to run
- **Language Support**: Works with any programming language

## Why Pre-commit is Essential

### Benefits
1. **Consistency**: Ensures all team members follow the same standards
2. **Early Detection**: Catches issues before they enter the codebase
3. **Automation**: Reduces manual review burden
4. **Security**: Prevents sensitive data from being committed
5. **Quality**: Maintains code quality automatically

### Real-world Impact
```
Without pre-commit:
- Developer commits code with syntax errors
- CI pipeline fails after 10 minutes
- Developer context switches back to fix
- Total time lost: 20-30 minutes

With pre-commit:
- Error caught in 2 seconds
- Fixed immediately
- Clean commit pushed
- Total time: 2 minutes
```

## Installation and Setup

### Step 1: Install Pre-commit

#### Using pip (Python)
```bash
pip install pre-commit
```

#### Using Homebrew (macOS)
```bash
brew install pre-commit
```

#### Using Conda
```bash
conda install -c conda-forge pre-commit
```

### Step 2: Create Configuration File

Create `.pre-commit-config.yaml` in your project root:

```yaml
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

### Step 3: Install Git Hooks

```bash
pre-commit install
```

This creates `.git/hooks/pre-commit` that will run your hooks.

### Step 4: (Optional) Run Against All Files

```bash
pre-commit run --all-files
```

## Common Hooks by Language

### Python Projects

```yaml
repos:
  # Standard pre-commit hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-ast
      - id: check-builtin-literals
      - id: check-case-conflict
      - id: check-docstring-first
      - id: check-merge-conflict
      - id: check-toml
      - id: debug-statements
      - id: name-tests-test
        args: [--pytest-test-first]

  # Black - Code formatter
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        language_version: python3.11

  # Ruff - Fast Python linter
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # mypy - Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--strict]

  # isort - Import sorting
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile, black]

  # Docstring coverage
  - repo: https://github.com/econchick/interrogate
    rev: 1.5.0
    hooks:
      - id: interrogate
        args: [--quiet, --fail-under=80]
```

### JavaScript/TypeScript Projects

```yaml
repos:
  # Standard hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-json
      - id: check-merge-conflict
      - id: no-commit-to-branch
        args: [--branch, main, --branch, master]

  # Prettier - Code formatter
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [css, javascript, jsx, ts, tsx, json, yaml, markdown]

  # ESLint - Linter
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.57.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        types: [file]
        additional_dependencies:
          - eslint@8.57.0
          - eslint-config-prettier@9.1.0
          - eslint-plugin-react@7.34.1
          - eslint-plugin-react-hooks@4.6.0
          - '@typescript-eslint/parser@7.3.1'
          - '@typescript-eslint/eslint-plugin@7.3.1'

  # TypeScript type checking
  - repo: local
    hooks:
      - id: typescript
        name: TypeScript
        entry: npx tsc --noEmit
        language: system
        pass_filenames: false
        files: \.tsx?$
```

### Go Projects

```yaml
repos:
  # Standard hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: trailing-whitespace
      - id: end-of-file-fixer

  # Go fmt
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-vet
      - id: go-imports
      - id: go-cyclo
        args: [-over=15]
      - id: go-mod-tidy
      - id: go-unit-tests
      - id: golangci-lint

  # Go security
  - repo: https://github.com/securego/gosec
    rev: v2.19.0
    hooks:
      - id: gosec
```

### Multi-language Projects

```yaml
repos:
  # Universal hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: check-symlinks
      - id: destroyed-symlinks
      - id: detect-private-key
      - id: end-of-file-fixer
      - id: fix-byte-order-marker
      - id: mixed-line-ending
      - id: trailing-whitespace

  # Markdown
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.39.0
    hooks:
      - id: markdownlint
        args: [--fix]

  # YAML
  - repo: https://github.com/adrienverge/yamllint
    rev: v1.35.1
    hooks:
      - id: yamllint
        args: [-c=.yamllint.yaml]

  # Shell scripts
  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.10.0.1
    hooks:
      - id: shellcheck

  # Dockerfile
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint-docker
```

## Security Scanning

### Detecting Secrets

```yaml
  # Detect secrets
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package.lock.json

  # Alternative: GitLeaks
  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.18.2
    hooks:
      - id: gitleaks
```

### Python Security

```yaml
  # Safety - Check for known vulnerabilities
  - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.3
    hooks:
      - id: python-safety-dependencies-check

  # Bandit - Security linter
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.8
    hooks:
      - id: bandit
        args: [-r, src/]
        exclude: tests/
```

### JavaScript Security

```yaml
  # npm audit
  - repo: local
    hooks:
      - id: npm-audit
        name: npm audit
        entry: npm audit --audit-level=moderate
        language: system
        pass_filenames: false

  # Snyk
  - repo: local
    hooks:
      - id: snyk-test
        name: Snyk Security Test
        entry: snyk test
        language: system
        pass_filenames: false
```

## Code Quality Checks

### Comprehensive Python Quality

```yaml
  # Pylint - Comprehensive linter
  - repo: https://github.com/PyCQA/pylint
    rev: v3.1.0
    hooks:
      - id: pylint
        args:
          - --max-line-length=120
          - --disable=C0111  # missing-docstring
          - --disable=R0903  # too-few-public-methods

  # flake8 - Style guide enforcement
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=120]
        additional_dependencies:
          - flake8-bugbear
          - flake8-comprehensions
          - flake8-simplify

  # pydocstyle - Docstring style checker
  - repo: https://github.com/PyCQA/pydocstyle
    rev: 6.3.0
    hooks:
      - id: pydocstyle
        args: [--convention=google]
```

### Code Complexity

```yaml
  # Radon - Complexity measurement
  - repo: https://github.com/rubik/xenon
    rev: v0.9.1
    hooks:
      - id: xenon
        args: [--max-absolute=B, --max-modules=A, --max-average=A]

  # McCabe complexity
  - repo: local
    hooks:
      - id: mccabe
        name: McCabe Complexity
        entry: python -m mccabe --min 10
        language: system
        types: [python]
```

## Test Execution Hooks

### Python Tests

```yaml
  # Pytest
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [-v, --tb=short]

  # Pytest with coverage
  - repo: local
    hooks:
      - id: pytest-cov
        name: pytest with coverage
        entry: pytest --cov=src --cov-report=term-missing --cov-fail-under=80
        language: system
        pass_filenames: false
        always_run: true
```

### JavaScript Tests

```yaml
  # Jest
  - repo: local
    hooks:
      - id: jest
        name: Jest Tests
        entry: npm test
        language: system
        pass_filenames: false
        files: \.(js|jsx|ts|tsx)$

  # Jest with coverage
  - repo: local
    hooks:
      - id: jest-coverage
        name: Jest Coverage
        entry: npm run test:coverage -- --coverage --passWithNoTests
        language: system
        pass_filenames: false
```

## Coverage Enforcement

### Python Coverage Configuration

Create `.coveragerc`:

```ini
[run]
source = src
omit = 
    */tests/*
    */test_*.py
    */__init__.py
    */conftest.py

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = htmlcov

[xml]
output = coverage.xml
```

Hook configuration:

```yaml
  - repo: local
    hooks:
      - id: coverage-check
        name: Check test coverage
        entry: bash -c 'coverage run -m pytest && coverage report --fail-under=80'
        language: system
        pass_filenames: false
        always_run: true
```

### JavaScript Coverage

```yaml
  - repo: local
    hooks:
      - id: coverage-threshold
        name: Coverage Threshold
        entry: npx jest --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80,"statements":80}}'
        language: system
        pass_filenames: false
```

## Custom Hook Creation

### Basic Custom Hook

```yaml
  - repo: local
    hooks:
      - id: check-copyright
        name: Check Copyright Headers
        entry: ./scripts/check-copyright.sh
        language: script
        types: [python]
```

`scripts/check-copyright.sh`:

```bash
#!/bin/bash
# Check for copyright headers in Python files

YEAR=$(date +%Y)
COPYRIGHT="Copyright (c) $YEAR YourCompany"

for file in "$@"; do
    if ! head -n 5 "$file" | grep -q "$COPYRIGHT"; then
        echo "Missing copyright header in: $file"
        exit 1
    fi
done
```

### Python Custom Hook

```yaml
  - repo: local
    hooks:
      - id: check-todo-format
        name: Check TODO Format
        entry: python scripts/check_todos.py
        language: python
        types: [python]
        additional_dependencies: [re]
```

`scripts/check_todos.py`:

```python
#!/usr/bin/env python3
"""Check that TODOs follow the format: TODO(username): Description"""

import re
import sys
from pathlib import Path

TODO_PATTERN = re.compile(r'#\s*TODO\([a-zA-Z0-9_]+\):\s*.+')
BAD_TODO_PATTERN = re.compile(r'#\s*TODO(?!\([a-zA-Z0-9_]+\):)')

def check_todos(filename):
    """Check TODOs in a single file."""
    errors = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if BAD_TODO_PATTERN.search(line):
                if not TODO_PATTERN.search(line):
                    errors.append(f"{filename}:{line_num}: Invalid TODO format")
    
    return errors

def main():
    """Main entry point."""
    all_errors = []
    
    for filename in sys.argv[1:]:
        errors = check_todos(filename)
        all_errors.extend(errors)
    
    if all_errors:
        for error in all_errors:
            print(error)
        print("\nExpected format: TODO(username): Description")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Advanced Hook with Configuration

```yaml
  - repo: local
    hooks:
      - id: validate-api-schema
        name: Validate API Schema
        entry: python scripts/validate_schema.py
        language: python
        files: api/.*\.yaml$
        additional_dependencies: [pyyaml, jsonschema]
        args: [--schema, schemas/openapi.json]
```

## CI/CD Integration

### GitHub Actions

`.github/workflows/pre-commit.yml`:

```yaml
name: pre-commit

on:
  pull_request:
  push:
    branches: [main]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - uses: pre-commit/action@v3.0.1
```

### GitLab CI

`.gitlab-ci.yml`:

```yaml
pre-commit:
  stage: test
  image: python:3.11
  before_script:
    - pip install pre-commit
    - pre-commit install
  script:
    - pre-commit run --all-files
  only:
    - merge_requests
    - main
```

### Jenkins

`Jenkinsfile`:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Pre-commit Checks') {
            steps {
                sh '''
                    python -m pip install pre-commit
                    pre-commit install
                    pre-commit run --all-files
                '''
            }
        }
    }
}
```

### CircleCI

`.circleci/config.yml`:

```yaml
version: 2.1

jobs:
  pre-commit:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run:
          name: Install pre-commit
          command: pip install pre-commit
      - run:
          name: Run pre-commit
          command: pre-commit run --all-files

workflows:
  version: 2
  test:
    jobs:
      - pre-commit
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Hook Fails with "command not found"

**Problem**: The hook's executable isn't available in the environment.

**Solution**:
```yaml
  - repo: local
    hooks:
      - id: my-hook
        # Specify the correct language
        language: system  # Uses system PATH
        # OR
        language: python  # Creates virtual environment
        additional_dependencies: [package-name]
```

#### 2. Hooks Running Too Slowly

**Problem**: Hooks take too long to execute.

**Solutions**:

a) Run hooks in parallel:
```bash
pre-commit run --all-files --show-diff-on-failure --jobs 4
```

b) Use faster alternatives:
```yaml
# Instead of pylint, use ruff
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.3.4
  hooks:
    - id: ruff
```

c) Limit file scope:
```yaml
- id: expensive-hook
  files: ^src/  # Only run on src directory
  exclude: ^tests/
```

#### 3. Conflicts Between Formatters

**Problem**: Multiple formatters fighting over style.

**Solution**: Order matters! Put formatters in the correct sequence:
```yaml
# Run isort before black
- id: isort
  args: [--profile, black]
- id: black
```

#### 4. Hook Modifies Files But Still Fails

**Problem**: Hook fixes issues but returns non-zero exit code.

**Solution**:
```bash
# Let pre-commit handle the modifications
pre-commit run --all-files

# Then commit the changes
git add -u
git commit -m "Apply pre-commit fixes"
```

#### 5. Different Behavior Locally vs CI

**Problem**: Hooks pass locally but fail in CI.

**Common Causes**:
- Different versions of tools
- Missing system dependencies
- Environment variables

**Solution**: Pin versions explicitly:
```yaml
- repo: https://github.com/psf/black
  rev: 24.3.0  # Pin exact version
  hooks:
    - id: black
      language_version: python3.11  # Pin Python version
```

#### 6. Skip Hooks Temporarily

**When needed** (use sparingly):
```bash
# Skip all hooks
git commit --no-verify

# Skip specific hooks
SKIP=flake8,mypy git commit

# Skip in pre-commit command
pre-commit run --all-files --skip flake8
```

### Debugging Hooks

#### Enable Verbose Output
```bash
pre-commit run --all-files --verbose
```

#### Test Specific Hook
```bash
pre-commit run <hook-id> --all-files
```

#### Check Hook Environment
```yaml
- repo: local
  hooks:
    - id: debug-env
      name: Debug Environment
      entry: bash -c 'echo "PATH=$PATH"; python --version; which python'
      language: system
      always_run: true
```

## Complete Examples

### Example 1: Python Web Application

`.pre-commit-config.yaml`:

```yaml
default_language_version:
  python: python3.11

repos:
  # Basic checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: check-ast
      - id: check-case-conflict
      - id: check-executables-have-shebangs
      - id: check-json
      - id: check-merge-conflict
      - id: check-toml
      - id: check-yaml
        args: [--unsafe]
      - id: debug-statements
      - id: detect-private-key
      - id: end-of-file-fixer
      - id: mixed-line-ending
      - id: name-tests-test
        args: [--pytest-test-first]
      - id: requirements-txt-fixer
      - id: trailing-whitespace

  # Security
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.8
    hooks:
      - id: bandit
        args: [-r, src/, --skip, B101]

  # Code formatting
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile, black, --line-length, 120]

  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        args: [--line-length, 120]

  # Linting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.4
    hooks:
      - id: ruff
        args: [--fix, --line-length, 120]

  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length, 120, --extend-ignore, E203]
        additional_dependencies:
          - flake8-bugbear
          - flake8-comprehensions
          - flake8-simplify
          - flake8-annotations

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: 
          - types-requests
          - types-python-dateutil
          - sqlalchemy[mypy]
        args: [--strict, --ignore-missing-imports]

  # Documentation
  - repo: https://github.com/PyCQA/pydocstyle
    rev: 6.3.0
    hooks:
      - id: pydocstyle
        args: [--convention, google, --add-ignore, D107]

  # Tests
  - repo: local
    hooks:
      - id: pytest
        name: Run tests
        entry: pytest -v --tb=short
        language: system
        pass_filenames: false
        always_run: true

      - id: pytest-coverage
        name: Check coverage
        entry: pytest --cov=src --cov-report=term-missing --cov-fail-under=85
        language: system
        pass_filenames: false
        always_run: true

  # Database migrations
  - repo: local
    hooks:
      - id: check-migrations
        name: Check migrations
        entry: python manage.py makemigrations --check --dry-run
        language: system
        pass_filenames: false
        types: [python]

  # Custom business logic
  - repo: local
    hooks:
      - id: check-api-versions
        name: API Version Check
        entry: python scripts/check_api_versions.py
        language: python
        files: api/.*\.py$
```

### Example 2: Node.js Full-Stack Application

`.pre-commit-config.yaml`:

```yaml
repos:
  # Basic checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: [--maxkb=2000]
      - id: check-case-conflict
      - id: check-json
      - id: check-merge-conflict
      - id: check-yaml
      - id: detect-private-key
      - id: end-of-file-fixer
        exclude: \.(jpg|jpeg|png|gif|svg|ico)$
      - id: mixed-line-ending
      - id: trailing-whitespace
        exclude: \.(md|markdown)$

  # Security
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets

  # Prettier
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [css, scss, javascript, jsx, ts, tsx, json, yaml, markdown]
        args: [--write]
        additional_dependencies:
          - prettier@3.2.5
          - prettier-plugin-tailwindcss@0.5.11

  # ESLint
  - repo: local
    hooks:
      - id: eslint
        name: ESLint
        entry: npx eslint --fix
        language: system
        types: [file]
        files: \.(js|jsx|ts|tsx)$
        exclude: (node_modules|build|dist|coverage)/

  # TypeScript
  - repo: local
    hooks:
      - id: typescript
        name: TypeScript Check
        entry: npx tsc --noEmit
        language: system
        pass_filenames: false
        files: \.(ts|tsx)$

  # CSS/SCSS Linting
  - repo: local
    hooks:
      - id: stylelint
        name: Stylelint
        entry: npx stylelint --fix
        language: system
        types: [file]
        files: \.(css|scss|sass)$

  # Tests
  - repo: local
    hooks:
      - id: jest
        name: Jest Tests
        entry: npm test -- --passWithNoTests --findRelatedTests
        language: system
        types: [file]
        files: \.(js|jsx|ts|tsx)$
        exclude: \.(test|spec)\.(js|jsx|ts|tsx)$

      - id: jest-coverage
        name: Jest Coverage
        entry: npm run test:coverage -- --passWithNoTests
        language: system
        pass_filenames: false
        always_run: true

  # Audit
  - repo: local
    hooks:
      - id: npm-audit
        name: NPM Audit
        entry: npm audit --audit-level=high
        language: system
        pass_filenames: false

  # Build check
  - repo: local
    hooks:
      - id: build-check
        name: Build Check
        entry: npm run build
        language: system
        pass_filenames: false
        stages: [manual]  # Only run when explicitly requested

  # Documentation
  - repo: local
    hooks:
      - id: jsdoc
        name: JSDoc Check
        entry: npx jsdoc -c jsdoc.json --verbose --pedantic
        language: system
        types: [file]
        files: \.(js|jsx|ts|tsx)$
        exclude: \.(test|spec)\.(js|jsx|ts|tsx)$

  # Package.json
  - repo: local
    hooks:
      - id: package-json-sorted
        name: Sort package.json
        entry: npx sort-package-json
        language: system
        files: package\.json$
```

### Example 3: Go Microservice

`.pre-commit-config.yaml`:

```yaml
repos:
  # Basic checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: [--maxkb=5000]
      - id: check-case-conflict
      - id: check-json
      - id: check-merge-conflict
      - id: check-yaml
      - id: detect-private-key
      - id: end-of-file-fixer
      - id: mixed-line-ending
      - id: trailing-whitespace

  # Go specific
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-imports
      - id: go-vet
      - id: go-cyclo
        args: [-over=15]
      - id: go-mod-tidy
      - id: go-unit-tests
      - id: golangci-lint
        args: [--timeout=5m]

  # Go security
  - repo: https://github.com/securego/gosec
    rev: v2.19.0
    hooks:
      - id: gosec
        args: ['-fmt=json', '-out=gosec-report.json', '-stdout']

  # Go documentation
  - repo: local
    hooks:
      - id: go-doc
        name: Go Documentation
        entry: bash -c 'go doc -all ./... | grep -E "^(func|type|const|var)" | wc -l | xargs test 0 -lt'
        language: system
        pass_filenames: false

  # Build checks
  - repo: local
    hooks:
      - id: go-build
        name: Go Build
        entry: go build -v ./...
        language: system
        pass_filenames: false

      - id: go-generate
        name: Go Generate
        entry: go generate ./...
        language: system
        pass_filenames: false

  # Test coverage
  - repo: local
    hooks:
      - id: go-coverage
        name: Go Coverage
        entry: bash -c 'go test -race -coverprofile=coverage.out -covermode=atomic ./... && go tool cover -func=coverage.out | grep total | awk "{print $3}" | sed "s/%//" | awk "{exit ($1 < 80)}"'
        language: system
        pass_filenames: false

  # Protocol Buffers
  - repo: local
    hooks:
      - id: protobuf-lint
        name: Protocol Buffer Lint
        entry: buf lint
        language: system
        files: \.proto$

      - id: protobuf-format
        name: Protocol Buffer Format
        entry: buf format -w
        language: system
        files: \.proto$

  # Docker
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint-docker

  # Kubernetes
  - repo: local
    hooks:
      - id: kubeval
        name: Validate Kubernetes configs
        entry: kubeval
        language: system
        files: (deployment|service|configmap|secret)\.ya?ml$

  # Makefile
  - repo: https://github.com/mrtazz/checkmake
    rev: 0.2.2
    hooks:
      - id: checkmake
```

### Example 4: Multi-Language Monorepo

`.pre-commit-config.yaml`:

```yaml
# Global settings
default_language_version:
  python: python3.11
  node: 18.19.0

exclude: |
  (?x)^(
    .*/migrations/.*|
    .*/vendor/.*|
    .*/node_modules/.*|
    .*/\.next/.*|
    .*/build/.*|
    .*/dist/.*
  )$

repos:
  # Universal checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: [--maxkb=2000]
      - id: check-case-conflict
      - id: check-executables-have-shebangs
      - id: check-json
      - id: check-merge-conflict
      - id: check-symlinks
      - id: check-toml
      - id: check-xml
      - id: check-yaml
        args: [--unsafe]
      - id: detect-private-key
      - id: destroyed-symlinks
      - id: end-of-file-fixer
      - id: fix-byte-order-marker
      - id: mixed-line-ending
        args: [--fix=lf]
      - id: no-commit-to-branch
        args: [--branch, main, --branch, master, --branch, production]
      - id: trailing-whitespace

  # Security (all languages)
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.18.2
    hooks:
      - id: gitleaks

  # Markdown
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.39.0
    hooks:
      - id: markdownlint
        args: [--fix, --config, .markdownlint.json]

  # YAML
  - repo: https://github.com/adrienverge/yamllint
    rev: v1.35.1
    hooks:
      - id: yamllint
        args: [-c, .yamllint.yaml]

  # Shell scripts
  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.10.0.1
    hooks:
      - id: shellcheck
        args: [--severity=warning]

  - repo: https://github.com/openstack/bashate
    rev: 2.1.1
    hooks:
      - id: bashate
        args: [--ignore=E006,E040]

  # Python (backend services)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.4
    hooks:
      - id: ruff
        args: [--fix]
        files: ^(backend|scripts|tools)/.*\.py$
      - id: ruff-format
        files: ^(backend|scripts|tools)/.*\.py$

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        files: ^backend/.*\.py$
        additional_dependencies: [types-all]

  # JavaScript/TypeScript (frontend)
  - repo: local
    hooks:
      - id: frontend-prettier
        name: Frontend Prettier
        entry: bash -c 'cd frontend && npx prettier --write'
        language: system
        files: ^frontend/.*\.(js|jsx|ts|tsx|css|scss|json)$

      - id: frontend-eslint
        name: Frontend ESLint
        entry: bash -c 'cd frontend && npx eslint --fix'
        language: system
        files: ^frontend/.*\.(js|jsx|ts|tsx)$

      - id: frontend-typescript
        name: Frontend TypeScript
        entry: bash -c 'cd frontend && npx tsc --noEmit'
        language: system
        pass_filenames: false
        files: ^frontend/.*\.(ts|tsx)$

  # Go (services)
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
        files: ^services/.*\.go$
      - id: go-imports
        files: ^services/.*\.go$
      - id: go-vet
        files: ^services/.*\.go$
      - id: golangci-lint
        files: ^services/.*\.go$

  # Docker
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint-docker

  # Terraform
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.88.0
    hooks:
      - id: terraform_fmt
        files: ^infrastructure/.*\.tf$
      - id: terraform_validate
        files: ^infrastructure/.*\.tf$
      - id: terraform_tflint
        files: ^infrastructure/.*\.tf$

  # SQL
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.0.5
    hooks:
      - id: sqlfluff-lint
        files: \.(sql|dml|ddl)$
      - id: sqlfluff-fix
        files: \.(sql|dml|ddl)$

  # Custom monorepo checks
  - repo: local
    hooks:
      - id: check-cross-dependencies
        name: Check Cross Dependencies
        entry: python scripts/check_cross_dependencies.py
        language: python
        pass_filenames: false
        always_run: true

      - id: validate-service-contracts
        name: Validate Service Contracts
        entry: python scripts/validate_contracts.py
        language: python
        files: (api|contracts)/.*\.(yaml|json)$

      - id: monorepo-build
        name: Monorepo Build Check
        entry: make build-all
        language: system
        pass_filenames: false
        stages: [manual]
```

## Best Practices

1. **Start Small**: Begin with basic hooks and gradually add more
2. **Pin Versions**: Always specify exact versions for reproducibility
3. **Order Matters**: Put formatters before linters
4. **Use exclude**: Don't run hooks on generated or vendor files
5. **CI Integration**: Always run pre-commit in CI
6. **Team Agreement**: Discuss and agree on hooks with your team
7. **Regular Updates**: Keep hooks updated with `pre-commit autoupdate`
8. **Documentation**: Document any custom hooks or configurations
9. **Performance**: Monitor hook execution time and optimize
10. **Staged Files**: By default, pre-commit only runs on staged files

## Conclusion

Pre-commit is a powerful tool that can significantly improve code quality and team productivity. Start with the basics, gradually add more checks, and customize to fit your team's needs. Remember that the goal is to catch issues early, not to make development painful.

For more information:
- Official docs: https://pre-commit.com
- Hook repository: https://pre-commit.com/hooks.html
- Community hooks: https://github.com/pre-commit/pre-commit-hooks