#!/usr/bin/env python3
"""
Generate comprehensive spec templates for new projects.

This tool creates a complete specification structure with all required
templates and documentation to ensure high-quality specs from the start.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from automation.lib.base import SpecTool
except ImportError:
    # Fallback for direct execution
    sys.path.insert(0, str(Path(__file__).parent))
    from lib.base import SpecTool

class SpecTemplateGenerator(SpecTool):
    """Generate spec templates with best practices built in."""
    
    VERSION = "3.0.0"
    DESCRIPTION = "Generate comprehensive spec templates for new projects"
    
    # Template sets available
    TEMPLATES = {
        'basic': 'Minimal spec structure for simple projects',
        'standard': 'Standard spec with all recommended sections (default)',
        'comprehensive': 'Full enterprise spec with compliance sections'
    }
    
    def create_parser(self):
        parser = super().create_parser()
        parser.add_argument('project_name', 
                          help='Name of the project')
        parser.add_argument('-o', '--output-dir', default='.',
                          help='Output directory (default: current directory)')
        parser.add_argument('-t', '--template', 
                          choices=list(self.TEMPLATES.keys()),
                          default='standard',
                          help='Template set to use')
        parser.add_argument('--list-templates', action='store_true',
                          help='List available templates and exit')
        parser.add_argument('--force', action='store_true',
                          help='Overwrite existing directory')
        return parser
        
    def get_examples(self):
        return """
Examples:
  # Create standard spec for "My API"
  %(prog)s "My API"
  
  # Use comprehensive template in specific directory
  %(prog)s "Enterprise System" -o ./specs -t comprehensive
  
  # List available templates
  %(prog)s --list-templates
"""
    
    def execute(self) -> int:
        if self.args.list_templates:
            return self.list_templates()
            
        # Validate inputs
        project_slug = self.args.project_name.lower().replace(' ', '-')
        project_dir = Path(self.args.output_dir) / project_slug
        
        if project_dir.exists() and not self.args.force:
            print(f"✗ Directory already exists: {project_dir}")
            print("  Use --force to overwrite")
            return 1
            
        # Create structure
        print(f"\n🚀 Creating {self.args.template} spec structure for: {self.args.project_name}")
        print(f"📁 Location: {project_dir.absolute()}\n")
        
        try:
            self.create_structure(project_dir)
            
            print(f"\n✅ Spec structure created successfully!")
            print(f"\n📝 Next steps:")
            print(f"  1. cd {project_dir}")
            print(f"  2. Review README.md for guidance")
            print(f"  3. Complete templates in requirements/ directory:")
            print(f"     - outcome-definition.md (define success)")
            print(f"     - acceptance-scenarios.md (test cases)")
            print(f"     - non-functional-requirements.md (quality)")
            print(f"  4. Fill out the main spec/SPEC.md")
            print(f"  5. Run validation:")
            print(f"     python3 -m automation.score-spec-quality spec/SPEC.md")
            
            return 0
            
        except Exception as e:
            print(f"\n✗ Error creating structure: {e}")
            return 1
        
    def list_templates(self) -> int:
        print("\nAvailable template sets:\n")
        for name, desc in self.TEMPLATES.items():
            default = " (default)" if name == "standard" else ""
            print(f"  {name}{default}")
            print(f"    {desc}\n")
        return 0
        
    def create_structure(self, project_dir: Path):
        """Create the project structure."""
        # Create directories
        directories = [
            project_dir / "spec",
            project_dir / "requirements",
            project_dir / "roadmap",
            project_dir / "phase-plans",
            project_dir / "review",
            project_dir / "validation"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created: {directory.name}/")
            
        # Create files based on template type
        if self.args.template == 'basic':
            self.create_basic_templates(project_dir)
        elif self.args.template == 'comprehensive':
            self.create_comprehensive_templates(project_dir)
        else:  # standard
            self.create_standard_templates(project_dir)
            
        # Always create these files
        self.create_common_files(project_dir)
        
    def create_common_files(self, project_dir: Path):
        """Create files common to all templates."""
        # Create .gitignore
        gitignore_content = """# Spec building artifacts
*.log
*.tmp
.DS_Store

# Validation reports
*-report.json
*-validation.json
validation/*.json
validation/*.html

# Review artifacts
review/*.md
!review/README.md

# Editor files
.vscode/
.idea/
*.swp
*.bak

# Python
__pycache__/
*.pyc
.pytest_cache/
"""
        (project_dir / ".gitignore").write_text(gitignore_content)
        print(f"  ✓ Created: .gitignore")
        
        # Create main README
        readme_content = f"""# {self.args.project_name} Specification

This directory contains the complete specification for the {self.args.project_name} project.

## Quick Start

1. **Complete Requirements** (requirements/)
   - Start with `outcome-definition.md` - define what success looks like
   - Fill out `acceptance-scenarios.md` - concrete test scenarios
   - Complete `non-functional-requirements.md` - performance, security, etc.

2. **Build the Spec** (spec/SPEC.md)
   - Use the requirements as input
   - Follow the template structure
   - Aim for 90+ quality score

3. **Validate Quality**
   ```bash
   python3 -m automation.score-spec-quality spec/SPEC.md
   ```

## Directory Structure

```
{project_dir.name}/
├── spec/              # Main specification
│   └── SPEC.md       # The primary spec document
├── requirements/      # Detailed requirements
│   ├── outcome-definition.md
│   ├── acceptance-scenarios.md
│   └── non-functional-requirements.md
├── roadmap/          # Implementation roadmap
├── phase-plans/      # Detailed execution plans
├── review/           # Quality reviews
└── validation/       # Validation reports
```

## Quality Standards

This spec targets a quality score of **90+** for standard approval.

### Key Quality Dimensions:
1. **Completeness** - All sections filled, no TODOs
2. **Clarity** - Unambiguous, well-structured
3. **Implementability** - Technically feasible, resourced
4. **Testability** - Clear acceptance criteria

## Validation Scripts

Run these from the parent directory:

```bash
# Check structure
python3 -m automation.validate-spec-structure spec/SPEC.md

# Score quality
python3 -m automation.score-spec-quality spec/SPEC.md

# Get improvement suggestions
python3 -m automation.suggest-spec-improvements spec/SPEC.md

# Run all validations
python3 -m automation.validate-all spec/SPEC.md
```

## Resources

- [Spec Building Guide](../01-spec-creation/README.md)
- [Quality Rubric](../templates/spec-quality-rubric.md)
- [Example Specs](../example-project/)

---
Created: {datetime.now().strftime('%Y-%m-%d')}
Template: {self.args.template}
"""
        (project_dir / "README.md").write_text(readme_content)
        print(f"  ✓ Created: README.md")
        
    def create_standard_templates(self, project_dir: Path):
        """Create standard template files."""
        # Create a simpler SPEC.md that won't have formatting issues
        spec_path = project_dir / "spec" / "SPEC.md"
        spec_path.write_text(self.get_spec_template())
        print("  ✓ Created: spec/SPEC.md")
        
        # Create requirements templates
        outcome_path = project_dir / "requirements" / "outcome-definition.md"
        outcome_path.write_text(self.get_outcome_template())
        print("  ✓ Created: requirements/outcome-definition.md")
        
        scenarios_path = project_dir / "requirements" / "acceptance-scenarios.md"
        scenarios_path.write_text(self.get_scenarios_template())
        print("  ✓ Created: requirements/acceptance-scenarios.md")
        
        nfr_path = project_dir / "requirements" / "non-functional-requirements.md"
        nfr_path.write_text(self.get_nfr_template())
        print("  ✓ Created: requirements/non-functional-requirements.md")
        
    def create_basic_templates(self, project_dir: Path):
        """Create minimal templates for simple projects."""
        spec_content = f"""# {self.args.project_name} - Specification

## Overview
[Brief description of the project and its purpose]

## Goals
- Goal 1: [Specific, measurable goal]
- Goal 2: [Another specific goal]
- Goal 3: [Another goal]

## Requirements

### Must Have
- [ ] [Critical requirement 1]
- [ ] [Critical requirement 2]
- [ ] [Critical requirement 3]

### Should Have
- [ ] [Important but not critical requirement]
- [ ] [Another important requirement]

### Nice to Have
- [ ] [Optional enhancement]

## Success Criteria
- [How we know the project succeeded]
- [Another success indicator]
- [Measurable outcome]

## Technical Approach
[High-level description of the technical solution]

## Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk description] | High/Medium/Low | High/Medium/Low | [How to handle] |

## Timeline
- Phase 1: [What] - [Duration] - [Deliverable]
- Phase 2: [What] - [Duration] - [Deliverable]

---
Created: {datetime.now().strftime('%Y-%m-%d')}
"""
        (project_dir / "spec" / "SPEC.md").write_text(spec_content)
        print("  ✓ Created: spec/SPEC.md (basic)")
        
    def create_comprehensive_templates(self, project_dir: Path):
        """Create enterprise-grade templates."""
        # Start with standard templates
        self.create_standard_templates(project_dir)
        
        # Add additional enterprise files
        security_content = f"""# Security Requirements - {self.args.project_name}

## Security Architecture

### Threat Model
- Asset Identification
- Threat Identification (STRIDE)
- Vulnerability Assessment
- Risk Rating

### Security Controls

#### Network Security
- Firewall rules
- Network segmentation
- DDoS protection
- VPN requirements

#### Application Security
- Input validation
- Output encoding
- Authentication mechanisms
- Session management
- Error handling

#### Data Security
- Encryption at rest
- Encryption in transit
- Key management
- Data classification
- Data retention

## Compliance Requirements

### Regulatory Compliance
- [ ] GDPR - General Data Protection Regulation
- [ ] CCPA - California Consumer Privacy Act
- [ ] HIPAA - Health Insurance Portability and Accountability Act
- [ ] PCI DSS - Payment Card Industry Data Security Standard
- [ ] SOX - Sarbanes-Oxley Act

### Security Standards
- [ ] ISO 27001 - Information Security Management
- [ ] NIST Cybersecurity Framework
- [ ] CIS Controls
- [ ] OWASP Top 10

## Security Testing

### Testing Schedule
- Static Application Security Testing (SAST): Every commit
- Dynamic Application Security Testing (DAST): Weekly
- Dependency Scanning: Daily
- Penetration Testing: Annually
- Security Code Review: Per release

### Security Metrics
- Mean Time to Detect (MTTD)
- Mean Time to Respond (MTTR)
- Vulnerability density
- Patch compliance rate

---
Created: {datetime.now().strftime('%Y-%m-%d')}
"""
        (project_dir / "requirements" / "security-requirements.md").write_text(security_content)
        print("  ✓ Created: requirements/security-requirements.md")
        
        # Add SLA template
        sla_content = f"""# Service Level Agreement - {self.args.project_name}

## Service Levels

### Availability SLA

| Service Tier | Availability Target | Measurement Period | Allowed Downtime |
|--------------|-------------------|-------------------|------------------|
| Production | 99.9% | Monthly | 43.2 minutes |
| Staging | 99.5% | Monthly | 3.6 hours |
| Development | 95% | Monthly | 36 hours |

### Performance SLA

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time (p95) | <200ms | 5-minute average |
| Page Load Time | <2 seconds | Real user monitoring |
| Database Query Time | <50ms | Query logs |

### Support SLA

| Priority | Response Time | Resolution Time |
|----------|--------------|-----------------|
| Critical (P1) | 15 minutes | 4 hours |
| High (P2) | 1 hour | 8 hours |
| Medium (P3) | 4 hours | 2 business days |
| Low (P4) | 1 business day | 5 business days |

## Maintenance Windows

- Scheduled: Sunday 2:00-4:00 AM UTC
- Emergency: 4-hour advance notice
- Patches: Zero-downtime deployment

## Service Credits

| Monthly Uptime | Service Credit |
|----------------|----------------|
| 99.5% - 99.9% | 10% |
| 99.0% - 99.5% | 25% |
| 95.0% - 99.0% | 50% |
| < 95.0% | 100% |

---
Created: {datetime.now().strftime('%Y-%m-%d')}
"""
        (project_dir / "requirements" / "sla.md").write_text(sla_content)
        print("  ✓ Created: requirements/sla.md")
    
    def get_spec_template(self):
        """Return the main SPEC.md template content."""
        return f"""# {self.args.project_name} - Project Specification

## Executive Summary

[Provide a 2-3 paragraph overview of the project, covering:]
- What problem this project solves
- Who benefits and how
- Expected business impact
- High-level approach

### Key Business Drivers
- **Driver 1**: [Specific business need or opportunity]
- **Driver 2**: [Market pressure or competitive advantage]
- **Driver 3**: [Efficiency or cost consideration]

### Success Criteria
| Criterion | Target | Measurement |
|-----------|--------|-------------|
| [Business Metric] | [Specific Target] | [How Measured] |
| [User Adoption] | [Target Percentage] | [Measurement Method] |
| [Performance] | [Target Value] | [Measurement Tool] |

## Stakeholders

| Role | Name | Responsibilities | Approval Authority |
|------|------|------------------|-------------------|
| Executive Sponsor | [Name] | Strategic oversight, funding | Final go/no-go |
| Product Owner | [Name] | Requirements, priorities | Feature approval |
| Technical Lead | [Name] | Architecture, technical decisions | Technical approval |
| QA Lead | [Name] | Quality standards, testing | Quality gates |
| User Representative | [Name] | User needs, UAT | User acceptance |

## Requirements

### Functional Requirements

#### FR-001: [Core Feature Name]
**Priority**: Must Have  
**Description**: The system shall [specific capability]

**Acceptance Criteria**:
- [ ] [Specific, measurable criterion]
- [ ] [Another measurable criterion]
- [ ] [Link to test scenario]

#### FR-002: [Another Feature]
**Priority**: Should Have  
**Description**: The system shall [specific capability]

**Acceptance Criteria**:
- [ ] [Specific criterion]
- [ ] [Another criterion]

### Non-Functional Requirements

#### NFR-001: Performance
**Priority**: Must Have

| Metric | Requirement | Degraded | Unacceptable |
|--------|-------------|----------|--------------|
| Response Time (95th percentile) | <200ms | 200-500ms | >500ms |
| Throughput | 1000 req/sec | 500-1000 | <500 |
| Concurrent Users | 5000 | 2500-5000 | <2500 |

#### NFR-002: Availability
**Priority**: Must Have
- Uptime: 99.9 percent (43.2 minutes downtime/month)
- RTO: 15 minutes
- RPO: 5 minutes

#### NFR-003: Security
**Priority**: Must Have
- Authentication: OAuth 2.0 / SAML 2.0
- Authorization: Role-based (RBAC)
- Encryption: TLS 1.3 in transit, AES-256 at rest

## System Architecture

### High-Level Architecture

[ASCII diagram or description of system components and their relationships]

### Technology Stack

#### Frontend
- **Framework**: [React/Vue/Angular] version X.X
- **State Management**: [Redux/Vuex/etc]
- **UI Components**: [Material/Ant/Custom]
- **Build Tool**: [Webpack/Vite/etc]

#### Backend
- **Runtime**: [Node.js/Python/Java] version X.X
- **Framework**: [Express/FastAPI/Spring]
- **API Style**: REST / GraphQL
- **Database**: [PostgreSQL/MongoDB/etc]

#### Infrastructure
- **Cloud Provider**: [AWS/Azure/GCP]
- **Containerization**: Docker
- **Orchestration**: Kubernetes / ECS
- **CI/CD**: [GitHub Actions/Jenkins/etc]

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation Strategy | Owner |
|------|-------------|--------|---------------------|-------|
| [Technical Risk] | Medium | High | [Specific mitigation actions] | Tech Lead |
| [Resource Risk] | Low | Medium | [Mitigation approach] | PM |
| [External Dependency] | High | Medium | [Fallback plan] | Product Owner |

## Implementation Approach

### Development Methodology
- **Framework**: Agile/Scrum
- **Sprint Length**: 2 weeks
- **Team Structure**: Cross-functional squads

### Quality Standards
- **Code Coverage**: >85 percent overall
- **Performance Tests**: Required for all endpoints
- **Security Scans**: Automated in CI/CD
- **Code Review**: Required for all changes

## Success Metrics

### Technical Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Page Load Time | <2 seconds | RUM data |
| API Response Time | <200ms (p95) | APM metrics |
| Error Rate | <0.1 percent | Error tracking |

### Business Metrics
| Metric | Baseline | Target | Timeline |
|--------|----------|--------|----------|
| [User Metric] | Current | +X percent | 6 months |
| [Revenue Metric] | Current | +Y amount | 12 months |

## Constraints and Assumptions

### Constraints
- **Budget**: $[Amount] total project cost
- **Timeline**: [X] months to production
- **Resources**: [X] developers, [Y] QA
- **Technology**: Must integrate with [existing system]

### Assumptions
- [Assumption about users or market]
- [Assumption about technology]
- [Assumption about resources]

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | {datetime.now().strftime('%Y-%m-%d')} | [Your Name] | Initial specification |

---
*This specification serves as the single source of truth for the {self.args.project_name} project.*
"""

    def get_outcome_template(self):
        """Return the outcome definition template."""
        return f"""# Outcome Definition - {self.args.project_name}

## Business Outcomes

### Primary Business Goal
**What business problem are we solving?**
[Describe the core business problem in 2-3 sentences]

**Why is this important now?**
[Explain urgency or opportunity]

### Success Metrics
| Metric | Current State | Target State | Measurement Method | Timeline |
|--------|---------------|--------------|-------------------|----------|
| [Metric 1] | [Current] | [Target] | [How measured] | [When] |
| [Metric 2] | [Current] | [Target] | [How measured] | [When] |

### Business Value
**Quantifiable Benefits**:
- Cost Savings: $[Amount] per [period]
- Revenue Increase: $[Amount] per [period]
- Efficiency Gain: [X] hours per [period]

## User Outcomes

### Primary User Persona
**Who they are**: [Role, background, technical level]

**Current Pain Points**:
- [Specific frustration 1]
- [Specific frustration 2]

**Desired Outcome**:
- "I want to [action] so that [benefit]"
- Success looks like: [Specific description]

## Technical Outcomes

### System Capabilities
| Capability | Current State | Target State | Business Impact |
|------------|---------------|--------------|-----------------|
| [Capability 1] | [Current] | [Target] | [Impact] |
| [Capability 2] | [Current] | [Target] | [Impact] |

## Success Scenarios

### Scenario 1: Day in the Life (Post-Implementation)
[Narrative description of improved user experience]

### Scenario 2: Business Impact (12 months)
[Narrative of business transformation]

---
*All implementation decisions should trace back to these outcomes.*
"""

    def get_scenarios_template(self):
        """Return the acceptance scenarios template."""
        return f"""# Acceptance Scenarios - {self.args.project_name}

## Core User Scenarios

### SCENARIO: CORE-001 - [Primary User Flow]
**Feature**: [Feature Name]  
**Priority**: Must Have

**Given**: [Initial context]  
**When**: [User action]  
**Then**: [Expected outcome]

**Test Data**:
```json
{{
  "input": {{
    "field1": "value1"
  }},
  "expected": {{
    "status": "success"
  }}
}}
```

**Acceptance Criteria**:
- [ ] Response time < 2 seconds
- [ ] Success message displayed
- [ ] Data persisted correctly

### SCENARIO: CORE-002 - [Error Handling]
**Feature**: [Feature Name]  
**Priority**: Must Have

**Given**: [Error condition]  
**When**: [User action]  
**Then**: [Graceful error handling]

## Edge Cases

### SCENARIO: EDGE-001 - [Edge Case Name]
**Priority**: Should Have

**Given**: [Edge condition]  
**When**: [Action]  
**Then**: [Expected handling]

## Performance Scenarios

### SCENARIO: PERF-001 - [Load Testing]
**Priority**: Must Have

**Given**: 1000 concurrent users  
**When**: All perform [action]  
**Then**: System responds within SLA

---
*These scenarios form the basis for acceptance testing.*
"""

    def get_nfr_template(self):
        """Return the NFR template."""
        return f"""# Non-Functional Requirements - {self.args.project_name}

## Performance Requirements

### Response Time
| Operation | Target | Degraded | Unacceptable |
|-----------|--------|----------|--------------|
| Page Load | <2s | 2-4s | >4s |
| API Call | <200ms | 200-500ms | >500ms |
| Search | <500ms | 500-1000ms | >1s |

### Throughput
| Metric | Target | Minimum | Peak |
|--------|--------|---------|------|
| Concurrent Users | 1000 | 500 | 2000 |
| Requests/Second | 500 | 250 | 1000 |

## Reliability Requirements

### Availability
- Core Services: 99.9 percent uptime
- API: 99.95 percent uptime
- Batch Processing: 99.5 percent uptime

### Recovery
- RTO: 15 minutes
- RPO: 5 minutes
- Backup Frequency: Every 6 hours

## Security Requirements

### Authentication
- Methods: Username/password, SSO
- MFA: Required for admin roles
- Session Timeout: 30 minutes

### Data Protection
- In Transit: TLS 1.3
- At Rest: AES-256
- PII: Encrypted and access controlled

## Usability Requirements

### Performance
- Response feedback: <100ms
- Loading indicators: After 500ms
- Error messages: Clear and actionable

### Accessibility
- WCAG 2.1 Level AA compliance
- Screen reader support
- Keyboard navigation

## Compliance Requirements

### Regulatory
- [ ] GDPR (if applicable)
- [ ] CCPA (if applicable)
- [ ] Industry-specific regulations

### Standards
- ISO 27001 alignment
- OWASP Top 10 mitigation

---
*These NFRs must be testable and monitored in production.*
"""

def main():
    tool = SpecTemplateGenerator()
    sys.exit(tool.run())

if __name__ == '__main__':
    main()