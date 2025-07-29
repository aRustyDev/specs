# Document Generator Implementation Guide

This guide explains how to adapt the narrative document generation system for different types of documentation beyond work plans.

## System Overview

The document generation system consists of three components:

```
JSON Config → Python Generator → Markdown Output
     ↓              ↓                    ↓
(Your Content) (Format Logic)   (Quality Validated)
```

### Key Principles

1. **Content-Driven**: All content comes from JSON config - generator only formats
2. **Algorithmic**: No AI/LLM used - purely deterministic transformation
3. **Extensible**: Easy to adapt for new document types via subclassing
4. **Quality-First**: Built-in validation ensures professional output

## How to Implement a New Document Type

### Step 1: Design Your Document Structure

First, identify the sections your document needs. For example, a Code Review Plan might have:

- Review metadata (PR number, author, scope)
- Review checklist (what to check)
- Architecture considerations
- Security review points
- Performance implications
- Approval criteria

### Step 2: Create JSON Schema

Define the structure for your configuration:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Code Review Plan Schema",
  "required": ["review", "checklist", "approval_criteria"],
  "properties": {
    "review": {
      "type": "object",
      "required": ["pr_number", "title", "scope", "reviewer"],
      "properties": {
        "pr_number": {"type": "integer"},
        "title": {"type": "string"},
        "scope": {"type": "string"},
        "reviewer": {"type": "string"}
      }
    },
    "checklist": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["category", "checks"],
        "properties": {
          "category": {"type": "string"},
          "checks": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "item": {"type": "string"},
                "how_to_verify": {"type": "string"},
                "severity": {"enum": ["critical", "important", "nice-to-have"]}
              }
            }
          }
        }
      }
    }
  }
}
```

### Step 3: Create Generator Class

Subclass the base generator and override methods:

```python
#!/usr/bin/env python3
"""
Code Review Plan Generator - Creates structured review documents
"""

from generate_phase_plan_v2 import NarrativeWorkPlanGenerator
from typing import Dict, Any

class CodeReviewPlanGenerator(NarrativeWorkPlanGenerator):
    """
    Generates code review plans from JSON configurations.
    
    Inherits base functionality and overrides specific methods
    for review plan generation.
    """
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Override to validate review-specific sections."""
        # Load base config
        config_file = Path(config_path)
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Validate review-specific required sections
        required_sections = ['review', 'checklist', 'approval_criteria']
        
        missing = [s for s in required_sections if s not in self.config]
        if missing:
            raise ValueError(f"Missing required sections: {', '.join(missing)}")
        
        return self.config
    
    def generate_header(self) -> None:
        """Generate review-specific header."""
        review = self.config['review']
        self.add_line(f"# Code Review: PR #{review['pr_number']} - {review['title']}")
        self.add_line(f"**Reviewer**: {review['reviewer']}")
        self.add_line(f"**Scope**: {review['scope']}")
        self.add_section_break()
    
    def generate_checklist(self) -> None:
        """Generate review checklist sections."""
        self.add_line("## Review Checklist")
        self.add_section_break()
        
        for category in self.config['checklist']:
            self.add_line(f"### {category['category']}")
            self.add_section_break()
            
            for check in category['checks']:
                severity_icon = {
                    'critical': '🔴',
                    'important': '🟡', 
                    'nice-to-have': '🟢'
                }[check['severity']]
                
                self.add_line(f"- [ ] {severity_icon} {check['item']}")
                if check.get('how_to_verify'):
                    self.add_line(f"  - *How to verify*: {check['how_to_verify']}", level=1)
            
            self.add_section_break()
    
    def generate_approval_criteria(self) -> None:
        """Generate approval requirements."""
        self.add_line("## Approval Criteria")
        self.add_section_break()
        
        criteria = self.config['approval_criteria']
        self.add_line("This PR can be approved when:")
        
        for criterion in criteria['required']:
            self.add_line(f"- ✅ {criterion}")
        
        if criteria.get('optional'):
            self.add_line()
            self.add_line("Nice to have (not blocking):")
            for criterion in criteria['optional']:
                self.add_line(f"- 💡 {criterion}")
    
    def generate_plan(self, config_path: str, output_root: str = None) -> str:
        """Override to use review-specific generation order."""
        self.load_config(config_path)
        self.output_lines = []
        
        # Review-specific section order
        self.generate_header()
        self.generate_checklist()
        self.generate_architecture_review()  # Custom section
        self.generate_security_review()      # Custom section
        self.generate_performance_review()   # Custom section
        self.generate_approval_criteria()
        self.generate_footer()
        
        # Output to review-specific location
        review_number = self.config['review']['pr_number']
        output_dir = Path(output_root or '.') / 'reviews' / f'pr-{review_number}'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / 'REVIEW_PLAN.md'
        content = '\n'.join(self.output_lines)
        
        with open(output_file, 'w') as f:
            f.write(content)
        
        return str(output_file)
```

### Step 4: Create Validator (Optional)

For document-specific validation rules:

```python
from validate_workplan import WorkPlanValidator

class CodeReviewValidator(WorkPlanValidator):
    """Validates code review plans for completeness and quality."""
    
    def _check_review_specific_content(self):
        """Check review-specific requirements."""
        # Must have severity markers
        if not any(icon in self.content for icon in ['🔴', '🟡', '🟢']):
            self.issues.append(ValidationIssue(
                ValidationLevel.WARNING,
                "Review Quality",
                "No severity markers found in checklist items"
            ))
        
        # Must have approval criteria
        if "Approval Criteria" not in self.content:
            self.issues.append(ValidationIssue(
                ValidationLevel.ERROR,
                "Review Structure",
                "Missing Approval Criteria section"
            ))
    
    def validate_file(self, file_path: str) -> Tuple[bool, List[ValidationIssue]]:
        """Add review-specific checks to base validation."""
        # Run base validation
        passed, issues = super().validate_file(file_path)
        
        # Add review-specific checks
        self._check_review_specific_content()
        
        has_errors = any(i.level == ValidationLevel.ERROR for i in self.issues)
        return not has_errors, self.issues
```

### Step 5: Create Sample Configuration

Provide an example for users:

```json
{
  "review": {
    "pr_number": 123,
    "title": "Add authentication middleware",
    "scope": "Security layer implementation",
    "reviewer": "senior-dev"
  },
  "checklist": [
    {
      "category": "Code Quality",
      "checks": [
        {
          "item": "Code follows project style guidelines",
          "how_to_verify": "Run `cargo fmt --check` and `cargo clippy`",
          "severity": "important"
        },
        {
          "item": "All functions have documentation",
          "how_to_verify": "Check for /// comments on public functions",
          "severity": "important"
        }
      ]
    },
    {
      "category": "Security",
      "checks": [
        {
          "item": "No hardcoded secrets or credentials",
          "how_to_verify": "Search for password, token, key literals",
          "severity": "critical"
        },
        {
          "item": "Input validation on all user data",
          "how_to_verify": "Trace data flow from API to storage",
          "severity": "critical"
        }
      ]
    }
  ],
  "approval_criteria": {
    "required": [
      "All critical checks pass",
      "Tests provide >80% coverage",
      "No security vulnerabilities identified"
    ],
    "optional": [
      "Performance benchmarks included",
      "Documentation updates complete"
    ]
  }
}
```

### Step 6: Integration

Add commands to justfile:

```makefile
# Generate code review plan
create-review-plan pr_number:
    python3 scripts/generate_review_plan.py reviews/pr-{{pr_number}}-config.json

# Validate review plan
validate-review-plan pr_number:
    python3 scripts/validate_review.py reviews/pr-{{pr_number}}/REVIEW_PLAN.md
```

## Examples of Other Document Types

### 1. API Documentation

```python
class APIDocGenerator(NarrativeWorkPlanGenerator):
    def generate_endpoint(self, endpoint):
        self.add_line(f"### {endpoint['method']} {endpoint['path']}")
        self.add_line(f"{endpoint['description']}")
        self.add_line()
        self.add_line("**Parameters:**")
        # ... generate parameter table
        self.add_line("**Example Request:**")
        self.add_line(f"```{endpoint['example_lang']}")
        self.add_line(endpoint['example_request'])
        self.add_line("```")
```

### 2. Deployment Runbook

```python
class RunbookGenerator(NarrativeWorkPlanGenerator):
    def generate_pre_deployment_checks(self):
        self.add_line("## Pre-Deployment Checklist")
        for check in self.config['pre_deployment']:
            self.add_line(f"- [ ] {check['description']}")
            self.add_line(f"  ```bash")
            self.add_line(f"  {check['command']}")
            self.add_line(f"  ```")
```

### 3. Architecture Decision Record (ADR)

```python
class ADRGenerator(NarrativeWorkPlanGenerator):
    def generate_decision_section(self):
        self.add_line("## Decision")
        self.add_line(self.config['decision']['choice'])
        self.add_line()
        self.add_line("### Consequences")
        self.add_line("**Positive:**")
        for item in self.config['decision']['positive_consequences']:
            self.add_line(f"- {item}")
```

## Best Practices

### 1. Keep Content in Config
- Generator should only format, not create content
- All text should come from the JSON configuration
- This ensures version control and consistency

### 2. Use Inheritance
- Inherit from base generator for common functionality
- Override only what's different for your document type
- Reuse formatting helpers like `add_line()`

### 3. Validate Thoroughly
- Create document-specific validators
- Check both structure and content quality
- Ensure actionable output

### 4. Provide Examples
- Include complete example configurations
- Show both minimal and comprehensive examples
- Document all required fields

### 5. Test Your Generator
- Create unit tests for each section generator
- Test with various configurations
- Validate output quality

## Common Patterns

### Conditional Sections
```python
def generate_optional_section(self):
    if 'optional_data' not in self.config:
        return  # Skip if not present
    
    # Generate section only if data exists
    self.add_line("## Optional Section")
    # ...
```

### Lists with Details
```python
def generate_detailed_list(self):
    for item in self.config['items']:
        self.add_line(f"### {item['title']}")
        self.add_line(item['description'])
        if item.get('code_example'):
            self.add_line(f"```{item['language']}")
            self.add_line(item['code_example'])
            self.add_line("```")
        self.add_section_break()
```

### Nested Structures
```python
def generate_nested_content(self):
    for section in self.config['sections']:
        self.add_line(f"## {section['title']}")
        for subsection in section['subsections']:
            self.add_line(f"### {subsection['title']}", level=1)
            self.add_line(subsection['content'], level=1)
```

## Troubleshooting

### Issue: Output looks fragmented
**Solution**: Add narrative introductions to each section in your config

### Issue: Too many parameters to track
**Solution**: Group related parameters in config structure

### Issue: Validation too strict
**Solution**: Make some sections optional in schema

### Issue: Hard to maintain different versions
**Solution**: Use schema versioning in config files

## Summary

The document generation system is designed to be adapted for any structured document type. By following this guide, you can create generators for:

- Technical specifications
- Review documents
- Runbooks and procedures
- API documentation
- Architecture records
- Training materials
- And more...

The key is to:
1. Define your document structure
2. Create comprehensive configs
3. Implement formatting logic
4. Validate output quality

This approach ensures consistent, high-quality documentation across your organization.