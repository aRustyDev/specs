# Alignment Validation Process

---
Previous: [Roadmap to Phase Plans](02-roadmap-to-phase-plans.md)
Next: [Phase Execution Guide](../03-execution/01-phase-execution-guide.md)
Related:
  - [Spec to Roadmap](01-spec-to-roadmap.md) - Creates roadmap
  - [Roadmap to Phase Plans](02-roadmap-to-phase-plans.md) - Creates phase plans
  - [Phase Execution Guide](../03-execution/01-phase-execution-guide.md) - Next step
---

## Overview
This framework ensures consistency and traceability across the entire spec-to-execution pipeline. It validates that requirements flow correctly from specifications through roadmaps to implementation plans.

## Validation Checkpoints

### 1. Spec → Roadmap Alignment

#### Coverage Validation
Every requirement in the spec must be mapped to at least one roadmap phase.

**Validation Matrix**:
| Spec Section | Requirement ID | Roadmap Phase | Status |
|--------------|----------------|---------------|--------|
| Authentication | REQ-AUTH-001 | Phase 1 | ✓ Mapped |
| User Management | REQ-USER-001 | Phase 2 | ✓ Mapped |
| Payments | REQ-PAY-001 | Phase 3 | ✓ Mapped |
| Performance | NFR-PERF-001 | Phase 1,4,6 | ✓ Mapped |

**Orphan Detection**:
```markdown
## Unmapped Requirements
- [ ] REQ-XXX-001: [Description] - No phase assigned
- [ ] NFR-XXX-001: [Description] - No phase assigned
```

#### Dependency Validation
Dependencies identified in spec must be respected in roadmap sequencing.

**Dependency Check**:
```markdown
## Dependency Violations
- [ ] Phase 3 requires Auth Service (Phase 1) - ✓ Satisfied
- [ ] Phase 2 requires Database (Phase 1) - ✓ Satisfied
- [ ] Phase 4 requires Payment Gateway (Phase 3) - ✓ Satisfied
```

### 2. Roadmap → Phase Plans Alignment

#### Phase Completeness
Each roadmap phase must have corresponding work and review plans.

**Plan Coverage**:
| Phase | Work Plan | Review Plan | Checkpoints Aligned | Resources Matched |
|-------|-----------|-------------|-------------------|-------------------|
| Phase 1 | ✓ Exists | ✓ Exists | ✓ 3/3 match | ✓ Yes |
| Phase 2 | ✓ Exists | ✓ Exists | ✓ 4/4 match | ✓ Yes |
| Phase 3 | ✓ Exists | ⚠ Missing | - | - |

#### Deliverable Mapping
Phase deliverables in roadmap must match plan outputs.

**Deliverable Validation**:
```markdown
## Phase 1 Deliverables
Roadmap Promise:
- [ ] Authentication Service
- [ ] User Database Schema
- [ ] API Gateway Setup

Work Plan Outputs:
- [ ] Authentication Service ✓
- [ ] User Database Schema ✓
- [ ] API Gateway Setup ✓
- [ ] Monitoring Setup (Extra - not in roadmap)
```

### 3. Worker ↔ Review Plan Alignment

#### Checkpoint Synchronization
Every worker checkpoint must have corresponding review checkpoint.

**Checkpoint Matrix**:
| Worker Checkpoint | Review Checkpoint | Focus Match | Timing Match |
|-------------------|-------------------|-------------|--------------|
| WC-1: Foundation | RC-1: Foundation | ✓ Yes | ✓ Yes |
| WC-2: Core Features | RC-2: Core Features | ✓ Yes | ✓ Yes |
| WC-3: Integration | RC-3: Integration | ✓ Yes | ✓ Yes |

#### Quality Criteria Alignment
Review criteria must validate work plan requirements.

**Criteria Mapping**:
```markdown
## Work Requirement → Review Validation
- TDD Required → Review checks test-first evidence
- 80% Coverage → Review runs coverage report
- Performance <200ms → Review runs performance tests
- Security Standards → Review runs security scan
```

### 4. Cross-Plan Consistency

#### Shared Resources
Resources allocated across phases must not conflict.

**Resource Conflict Check**:
| Resource | Phase 1 | Phase 2 | Phase 3 | Conflict? |
|----------|---------|---------|---------|-----------|
| Senior Dev | 100% | 50% | 0% | ✓ No |
| Junior Dev | 50% | 100% | 100% | ✓ No |
| DBA | 20% | 20% | 60% | ⚠ Overlap OK |

#### Timeline Validation
Phase timelines must align with roadmap schedule.

**Timeline Check**:
```markdown
## Timeline Alignment
Roadmap Total: 12 weeks
- Phase 1: 3 weeks (Roadmap) vs 3 weeks (Plan) ✓
- Phase 2: 4 weeks (Roadmap) vs 5 weeks (Plan) ✗
- Phase 3: 3 weeks (Roadmap) vs 3 weeks (Plan) ✓
- Buffer: 2 weeks (Roadmap) vs 1 week (Total) ⚠
```

## Validation Process

### Step 1: Automated Validation
Run validation scripts to check basic alignment:

```bash
# Check spec coverage
python validate-spec-roadmap.py

# Validate phase plans exist
python validate-roadmap-plans.py

# Check checkpoint alignment
python validate-plan-alignment.py
```

### Step 2: Manual Review
Review complex relationships that require judgment:

1. **Requirement Interpretation**
   - Does phase truly satisfy requirement?
   - Are success criteria preserved?
   - Is scope creep occurring?

2. **Dependency Logic**
   - Are soft dependencies considered?
   - Is parallelization opportunity missed?
   - Are critical paths identified?

3. **Resource Realism**
   - Are estimates padded appropriately?
   - Is context switching accounted for?
   - Are skill requirements matched?

### Step 3: Gap Resolution
For each identified gap:

```markdown
## Gap: [Description]
**Type**: Coverage / Dependency / Resource / Timeline
**Severity**: Blocking / Major / Minor
**Location**: [Spec section] → [Roadmap phase] → [Plan section]

**Resolution Options**:
1. Update [document] to include [missing element]
2. Adjust [timeline/resource] to accommodate
3. Accept gap with mitigation: [strategy]

**Decision**: Option X
**Rationale**: [Why this resolution]
**Owner**: [Who implements]
**Due Date**: [When]
```

## Validation Metrics

### Coverage Metrics
- Requirement Coverage: X% of spec requirements in roadmap
- Phase Coverage: X% of roadmap phases have plans
- Checkpoint Coverage: X% of work checkpoints have reviews

### Consistency Metrics
- Dependency Violations: X found
- Resource Conflicts: X found
- Timeline Mismatches: X found
- Deliverable Gaps: X found

### Quality Metrics
- Traceability Complete: X% of elements traceable
- Cross-references Valid: X% working
- Documentation Current: Last validated [date]

## Continuous Validation

### Triggers for Revalidation
1. Spec updates → Full pipeline validation
2. Roadmap changes → Downstream validation
3. Plan modifications → Peer plan validation
4. Resource changes → Conflict recheck

### Validation Frequency
- Daily: Automated basic checks
- Weekly: Team alignment review
- Phase End: Comprehensive validation
- Release: Final validation

## Validation Report Template

```markdown
# Alignment Validation Report
**Date**: [Date]
**Validator**: [Name]
**Scope**: [Full pipeline / Partial]

## Executive Summary
Overall alignment score: X%
Blocking issues: X
Major issues: X
Minor issues: X

## Detailed Findings

### Spec → Roadmap
- Coverage: X%
- Gaps: [List]
- Recommendations: [List]

### Roadmap → Plans
- Coverage: X%
- Gaps: [List]
- Recommendations: [List]

### Worker ↔ Review
- Checkpoint alignment: X%
- Criteria alignment: X%
- Recommendations: [List]

### Cross-Plan
- Resource conflicts: X
- Timeline issues: X
- Recommendations: [List]

## Action Items
1. [High Priority Action] - Owner - Due Date
2. [Medium Priority Action] - Owner - Due Date
3. [Low Priority Action] - Owner - Due Date

## Sign-off
- Technical Lead: _______ Date: _______
- Project Manager: _______ Date: _______
- Quality Lead: _______ Date: _______
```

## Best Practices

1. **Validate Early**: Don't wait until plans are complete
2. **Automate Basics**: Use scripts for repetitive checks
3. **Document Decisions**: Record why gaps are acceptable
4. **Version Together**: Keep documents in sync
5. **Review Regularly**: Alignment drifts over time

## Tools and Scripts

### Validation Scripts
Located in `scripts/validation/`:
- `validate-spec-roadmap.py`: Checks requirement coverage
- `validate-roadmap-plans.py`: Verifies plan existence
- `validate-plan-alignment.py`: Compares checkpoints
- `generate-validation-report.py`: Creates full report

### Helper Functions
```python
def check_requirement_coverage(spec_file, roadmap_file):
    """Verify all spec requirements appear in roadmap"""
    
def validate_dependencies(roadmap_file):
    """Check phase sequencing respects dependencies"""
    
def compare_checkpoints(work_plan, review_plan):
    """Ensure checkpoint alignment between plans"""
    
def detect_resource_conflicts(all_plans):
    """Find resource allocation conflicts"""
```

## Next Steps

1. Implement validation scripts
2. Create CI/CD integration
3. Train team on validation process
4. Establish validation rhythm
5. Track metrics over time