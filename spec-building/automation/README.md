# Automation Scripts Guide

## Overview

These scripts automate validation, quality checking, and improvement suggestions for the spec-building process.

## Quick Start

### Run All Validations
```bash
python validate-all.py path/to/SPEC.md
```

This runs all validation scripts and provides a comprehensive report.

## Available Scripts

### Main Scripts

#### `generate-spec-template.py`
Creates a complete spec structure for new projects.

**Usage:**
```bash
python generate-spec-template.py "Project Name" [output-directory]
```

**Example:**
```bash
python generate-spec-template.py "Task Manager" ./projects
```

**Creates:**
- Complete directory structure
- SPEC.md template
- All requirements templates
- README with instructions

#### `validate-all.py`
Runs all validation scripts in sequence.

**Usage:**
```bash
python validate-all.py path/to/SPEC.md
```

**Runs:**
1. Structure validation
2. Link validation
3. Quality scoring
4. Requirements traceability
5. Alignment validation (if applicable)
6. Improvement suggestions

### Validation Scripts

All validation scripts are in the `validation/` subdirectory.

#### `validate-spec-structure.py`
Checks that spec has all required sections.

**Usage:**
```bash
python validation/validate-spec-structure.py path/to/SPEC.md
```

**Checks:**
- Required sections present
- Section hierarchy correct
- No placeholders (TODO, TBD, etc.)

#### `validate-spec-links.py`
Verifies all internal links are valid.

**Usage:**
```bash
python validation/validate-spec-links.py path/to/SPEC.md
```

**Checks:**
- Markdown links work
- Anchor links exist
- Reference links defined

#### `score-spec-quality.py`
Calculates quality score (0-100) across 4 dimensions.

**Usage:**
```bash
python validation/score-spec-quality.py path/to/SPEC.md
```

**Scoring Dimensions:**
- Completeness (25 points)
- Clarity (25 points)
- Implementability (25 points)
- Testability (25 points)

**Output:**
- Detailed score breakdown
- Status (ready/needs work)
- JSON report saved

#### `validate-requirements-traceability.py`
Ensures requirements trace through to implementation details.

**Usage:**
```bash
python validation/validate-requirements-traceability.py path/to/SPEC.md
```

**Checks:**
- Requirements extracted
- Architecture traces
- Acceptance scenarios
- Risk coverage

#### `validate-alignment.py`
Checks consistency across spec, roadmap, and phase plans.

**Usage:**
```bash
python validation/validate-alignment.py path/to/project-directory
```

**Checks:**
- Requirement coverage
- Timeline consistency
- Resource allocation
- Technology alignment

### Improvement Scripts

#### `improvement/suggest-spec-improvements.py`
Analyzes spec and provides specific improvement suggestions.

**Usage:**
```bash
python improvement/suggest-spec-improvements.py path/to/SPEC.md
```

**Provides:**
- High priority improvements
- Medium priority improvements  
- Quick wins
- Specific examples

## Integration with Process

### Phase 1: Spec Creation
```bash
# Generate template for new project
python generate-spec-template.py "My Project"

# After creating spec, check quality
python validation/score-spec-quality.py spec/SPEC.md

# If score < 90, get suggestions
python improvement/suggest-spec-improvements.py spec/SPEC.md
```

### Phase 2: Planning
```bash
# After creating all plans, validate alignment
python validation/validate-alignment.py .

# Check requirements are covered
python validation/validate-requirements-traceability.py spec/SPEC.md
```

### Before Major Reviews
```bash
# Run comprehensive validation
python validate-all.py spec/SPEC.md
```

## Exit Codes

All scripts use consistent exit codes:
- `0`: Success/validation passed
- `1`: Failure/validation failed
- `2`: Error in script execution

## Output Files

Scripts generate reports in the same directory as the input:
- `spec-quality-report.json`: Detailed quality scores
- `requirements-traceability.json`: Traceability matrix
- `alignment-validation-report.json`: Alignment results
- `improvement-suggestions.md`: Specific improvements
- `validation-summary.txt`: Overall summary

## Customization

### Adding New Validations
1. Create script in `validation/` directory
2. Follow naming convention: `validate-{what}.py`
3. Use consistent exit codes
4. Add to `validate-all.py` sequence

### Modifying Scoring
Edit `score-spec-quality.py` to:
- Adjust scoring weights
- Add new criteria
- Change thresholds

## Troubleshooting

### Common Issues

**"File not found"**
- Check path is correct
- Ensure you're in the right directory

**"Module not found"**
- Scripts expect Python 3.6+
- Standard library only (no pip install needed)

**Validation fails but spec looks good**
- Check for subtle issues (spaces in links, etc.)
- Review the detailed output
- Some warnings may be acceptable

### Getting Help

Each script has help:
```bash
python script-name.py --help
```

## Best Practices

1. **Run early and often** - Don't wait until the end
2. **Fix high-priority issues first** - They have biggest impact
3. **Use validate-all before reviews** - Comprehensive check
4. **Keep reports** - Track improvement over time
5. **Customize carefully** - Scripts tuned for standard process