# Automation Script Improvement Plan

## Overview

The current automation scripts in `spec-building/automation/` need significant improvements to match the quality standards demonstrated in `/Users/asmith/code/public/specs/scripts/`. This plan outlines specific improvements for each script.

## Quality Standards Target

All scripts should have:
1. **Professional CLI Interface** - argparse with --help, --version, --verbose
2. **Comprehensive Documentation** - Module, class, and method docstrings
3. **Error Handling** - Try/except blocks with helpful error messages
4. **Extensible Architecture** - Classes that can be subclassed/extended
5. **Configuration Support** - JSON/YAML config file options
6. **Structured Output** - JSON export, quiet/verbose modes
7. **Type Hints** - Full type annotations for better IDE support
8. **Testing** - Unit tests for core functionality

## Script-Specific Improvements

### 1. generate-spec-template.py (Priority: HIGH)

**Current Issues:**
- No CLI argument parsing
- Templates hardcoded in strings
- No error handling
- Minimal documentation

**Improvements Needed:**

```python
# Add proper CLI
parser = argparse.ArgumentParser(
    description="Generate professional spec templates with customizable structure",
    epilog="Examples:\n  %(prog)s 'My Project' --template enterprise\n  %(prog)s 'API Service' -o ./specs --include-examples"
)

# Externalize templates
templates/
  ├── basic/
  │   ├── spec.md.jinja2
  │   └── requirements.md.jinja2
  ├── enterprise/
  │   └── ...
  └── custom/

# Add configuration support
{
  "template_set": "enterprise",
  "include_sections": ["security", "compliance", "sla"],
  "quality_target": 90,
  "output_structure": {...}
}
```

**Estimated Work**: 8-10 hours

### 2. score-spec-quality.py (Priority: HIGH)

**Current Issues:**
- Hardcoded scoring rules
- No configuration for thresholds
- Limited extensibility
- Basic output format

**Improvements Needed:**

```python
# Configurable scoring rules
{
  "scoring_dimensions": {
    "completeness": {
      "weight": 25,
      "checks": [
        {
          "name": "required_sections",
          "pattern": "...",
          "points": 10,
          "thresholds": {"excellent": 6, "good": 4, "poor": 2}
        }
      ]
    }
  }
}

# Multiple output formats
--format json|markdown|html|console

# Comparison mode
--baseline previous-score.json --show-delta
```

**Estimated Work**: 6-8 hours

### 3. validate-spec-structure.py (Priority: MEDIUM)

**Current Issues:**
- Basic validation only
- No custom rule support
- Simple output format

**Improvements Needed:**

```python
# Rule engine
class ValidationRule:
    def __init__(self, name: str, severity: Level, check: Callable):
        ...

# Custom rule loading
--rules custom-rules.yaml

# Fix suggestions
--suggest-fixes
```

**Estimated Work**: 4-6 hours

### 4. validate-alignment.py (Priority: MEDIUM)

**Current Issues:**
- Limited to basic checks
- No visualization
- Poor error messages

**Improvements Needed:**

```python
# Alignment visualization
--generate-matrix alignment-matrix.html

# Detailed traceability
--trace REQ-001 --show-path

# Gap analysis
--find-orphans --find-conflicts
```

**Estimated Work**: 6-8 hours

### 5. New Script: spec-doctor.py (Priority: LOW)

**Purpose:** Automated spec improvement tool

```python
"""
Analyzes specs and automatically improves them where possible.

Features:
- Fix common issues (formatting, structure)
- Add missing sections with templates
- Improve requirement traceability
- Generate missing diagrams
- Update cross-references
"""
```

**Estimated Work**: 10-12 hours

## Implementation Approach

### Phase 1: Core Improvements (Week 1)
1. Add CLI to all scripts using common base class
2. Externalize all hardcoded content
3. Add comprehensive error handling
4. Write documentation

### Phase 2: Advanced Features (Week 2)
1. Add configuration file support
2. Implement extensibility hooks
3. Create output formatters
4. Add comparison/delta features

### Phase 3: New Capabilities (Week 3)
1. Build spec-doctor.py
2. Add visualization features
3. Create integration tests
4. Package for distribution

## Common Base Classes

Create `automation/lib/base.py`:

```python
class SpecToolBase:
    """Base class for all spec automation tools."""
    
    def __init__(self):
        self.parser = self._create_parser()
        self.config = {}
        self.verbose = False
        
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create base argument parser with common options."""
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        parser.add_argument('--version', action='version', 
                          version=f'%(prog)s {self.VERSION}')
        parser.add_argument('-v', '--verbose', action='store_true',
                          help='Enable verbose output')
        parser.add_argument('-q', '--quiet', action='store_true',
                          help='Suppress non-error output')
        parser.add_argument('--config', type=str,
                          help='Configuration file path')
        return parser
        
    def run(self, args: List[str]) -> int:
        """Main entry point for the tool."""
        try:
            parsed_args = self.parser.parse_args(args)
            self._setup(parsed_args)
            return self._execute(parsed_args)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user", file=sys.stderr)
            return 130
        except Exception as e:
            if self.verbose:
                raise
            print(f"Error: {e}", file=sys.stderr)
            return 1
```

## Success Metrics

- All scripts score 90+ on quality assessment
- 100% have proper CLI interfaces
- 100% have comprehensive documentation
- Zero hardcoded content
- All support JSON configuration
- Test coverage >80%

## Timeline

- Week 1: Core improvements to existing scripts
- Week 2: Advanced features and extensibility
- Week 3: New tools and polish
- Week 4: Testing and documentation

Total estimated effort: 40-50 hours