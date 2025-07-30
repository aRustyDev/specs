#!/usr/bin/env python3
"""
Generate SPEC Template
Creates a new spec structure with all required files and sections.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def create_spec_structure(project_name: str, output_dir: str = "."):
    """Create complete spec structure for a new project"""
    
    project_dir = Path(output_dir) / project_name.lower().replace(" ", "-")
    
    print(f"🚀 Creating spec structure for: {project_name}")
    print(f"📁 Output directory: {project_dir}")
    
    # Create directory structure
    directories = [
        project_dir / "spec",
        project_dir / "spec" / ".spec",
        project_dir / "requirements",
        project_dir / "roadmap",
        project_dir / "phase-plans",
        project_dir / "review",
        project_dir / "validation"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created: {directory}")
    
    # Create main SPEC.md
    spec_content = f"""# {project_name} - Project Specification

## Executive Summary

[Provide a concise overview of the project, its purpose, and expected impact]

**Key Business Drivers**:
- [Driver 1]
- [Driver 2]
- [Driver 3]

**Success Criteria**:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

## Stakeholders

| Role | Name | Responsibilities | Approval Authority |
|------|------|------------------|-------------------|
| Executive Sponsor | [Name] | [Responsibilities] | Final go/no-go |
| Product Owner | [Name] | [Responsibilities] | Feature approval |
| Technical Lead | [Name] | [Responsibilities] | Technical decisions |
| Users Representative | [Name] | [Responsibilities] | UAT approval |

## Requirements

### Functional Requirements

#### FR-001: [Requirement Name]
**Priority**: Must Have
**Description**: [Detailed description]

**Acceptance Criteria**:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

#### FR-002: [Requirement Name]
**Priority**: Should Have
**Description**: [Detailed description]

**Acceptance Criteria**:
- [Criterion 1]
- [Criterion 2]

### Non-Functional Requirements

#### NFR-001: Performance
**Priority**: Must Have
**Metrics**:
- Response time: <[X]ms (95th percentile)
- Throughput: [X] requests/second
- Concurrent users: [X] without degradation

#### NFR-002: Availability
**Priority**: Must Have
**Metrics**:
- Uptime: [X]% ([X] minutes downtime/month)
- RTO: [X] hour
- RPO: [X] minutes

## System Architecture

### High-Level Architecture

```
[ASCII or Mermaid diagram showing system components]
```

### Technology Stack

#### Frontend
- **Framework**: [Technology choice with version]
- **State Management**: [Choice]
- **UI Library**: [Choice]
- **Build Tool**: [Choice]

#### Backend
- **Runtime**: [Technology choice with version]
- **Framework**: [Choice]
- **API Style**: [REST/GraphQL/gRPC]
- **Authentication**: [Method]

#### Infrastructure
- **Cloud Provider**: [Choice]
- **Container**: [Docker/Podman]
- **Orchestration**: [K8s/ECS/etc]
- **Database**: [Choice with version]
- **Cache**: [Choice]

### Data Model

```sql
-- Core entities
CREATE TABLE [entity] (
    id UUID PRIMARY KEY,
    -- fields
);
```

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|-------------------|
| [Risk 1] | [Low/Medium/High] | [Low/Medium/High] | [Strategy] |
| [Risk 2] | [Low/Medium/High] | [Low/Medium/High] | [Strategy] |

## Implementation Approach

### Development Methodology
- [Agile/Waterfall/Hybrid]
- Sprint length: [X] weeks
- Team structure: [Description]

### Quality Standards
- Test Coverage: >[X]% overall, >[X]% critical paths
- Code Review: [Process]
- Documentation: [Standards]

## Success Metrics

### Technical Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]

### Business Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]

## Constraints and Assumptions

### Constraints
- Budget: [Amount]
- Timeline: [Duration]
- Team: [Size and composition]
- [Other constraints]

### Assumptions
- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

## Change Log

### Version 1.0.0 - {datetime.now().strftime('%Y-%m-%d')}
- Initial specification created
- Quality Score: [TBD]

---

*This specification serves as the single source of truth for the {project_name} project.*
"""
    
    with open(project_dir / "spec" / "SPEC.md", 'w') as f:
        f.write(spec_content)
    
    # Create requirements templates
    outcome_content = """# Outcome Definition - {project_name}

## Business Outcomes

### Primary Business Goal
**What business problem are we solving?**
[Description]

### Success Metrics
| Metric | Current State | Target State | Measurement Method |
|--------|--------------|--------------|-------------------|
| [Metric 1] | [Current] | [Target] | [Method] |
| [Metric 2] | [Current] | [Target] | [Method] |

### Business Value
**Quantify the value of achieving these outcomes:**
- Cost savings: [Amount]
- Revenue increase: [Percentage/Amount]
- Efficiency gains: [Description]
- Risk reduction: [Description]

## User Outcomes

### User Personas

**Persona 1: [Name/Role]**
- Current pain points: [Description]
- Desired outcome: [Description]
- Success looks like: [Description]
- Failure looks like: [Description]

## Technical Outcomes

### System Capabilities
**What will the system be able to do that it can't today?**

| Capability | Current Limit | Target Capability | Business Impact |
|------------|---------------|-------------------|-----------------|
| [Capability 1] | [Current] | [Target] | [Impact] |
| [Capability 2] | [Current] | [Target] | [Impact] |

## Quality Outcomes

### Reliability
- Target uptime: [X]%
- Error budget: [X]%
- Recovery time: <[X] minutes
""".replace("{project_name}", project_name)
    
    with open(project_dir / "requirements" / "outcome-definition.md", 'w') as f:
        f.write(outcome_content)
    
    # Create acceptance scenarios template
    scenarios_content = """# Acceptance Scenarios - {project_name}

## Scenario: SCAN-001 - [Scenario Name]
**Feature**: [Feature name]
**User Story**: As a [user type], I want to [action] so that [outcome]

#### Preconditions
- [ ] [Condition 1]
- [ ] [Condition 2]

#### Steps
1. **Given**: [Initial context]
2. **When**: [User action]
3. **Then**: [Expected outcome]
4. **And**: [Additional outcomes]

#### Test Data
```json
{
  "input": {
    // Test input data
  },
  "expected": {
    // Expected results
  }
}
```

#### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

#### Edge Cases
- **Edge Case 1**: [Description]
  - Input: [Edge case input]
  - Expected: [How system should handle]

#### Error Scenarios
- **Error 1**: [Error type]
  - Input: [Bad input]
  - Expected: [Error handling]
""".replace("{project_name}", project_name)
    
    with open(project_dir / "requirements" / "acceptance-scenarios.md", 'w') as f:
        f.write(scenarios_content)
    
    # Create .gitignore
    gitignore_content = """# Spec building artifacts
*.log
*.tmp
.DS_Store

# Validation reports
*-report.json
*-validation.json

# Editor files
.vscode/
.idea/
*.swp
"""
    
    with open(project_dir / ".gitignore", 'w') as f:
        f.write(gitignore_content)
    
    # Create README
    readme_content = f"""# {project_name} Specification

This directory contains the complete specification for the {project_name} project.

## Structure

- `spec/` - Main specification documents
- `requirements/` - Detailed requirements and scenarios
- `roadmap/` - Implementation roadmap
- `phase-plans/` - Detailed phase execution plans
- `review/` - Quality reviews and assessments
- `validation/` - Alignment and validation reports

## Getting Started

1. Complete the templates in `requirements/` directory
2. Fill out the main `spec/SPEC.md` file
3. Run quality validation: `python validate-spec-structure.py spec/SPEC.md`
4. Score the spec: `python score-spec-quality.py spec/SPEC.md`

## Quality Standards

This spec targets a quality score of 90+ for standard approval.

Created: {datetime.now().strftime('%Y-%m-%d')}
"""
    
    with open(project_dir / "README.md", 'w') as f:
        f.write(readme_content)
    
    print(f"\n✅ Spec structure created successfully!")
    print(f"\n📝 Next steps:")
    print(f"  1. cd {project_dir}")
    print(f"  2. Complete the outcome definition in requirements/outcome-definition.md")
    print(f"  3. Fill out acceptance scenarios in requirements/acceptance-scenarios.md")
    print(f"  4. Complete the main spec in spec/SPEC.md")
    print(f"  5. Run validation scripts to check quality")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python generate-spec-template.py <project-name> [output-dir]")
        print("Example: python generate-spec-template.py 'Task Manager' ./projects")
        sys.exit(1)
    
    project_name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    create_spec_structure(project_name, output_dir)

if __name__ == "__main__":
    main()