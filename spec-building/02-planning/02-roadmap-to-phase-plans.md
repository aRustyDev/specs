# Roadmap to Phase Plans Process

---
Previous: [Spec to Roadmap](01-spec-to-roadmap.md)
Next: [Alignment Validation](03-alignment-validation.md)
Related:
  - [Spec to Roadmap](01-spec-to-roadmap.md) - Must complete first
  - [Alignment Validation](03-alignment-validation.md) - Verify consistency
  - [Phase Execution Guide](../03-execution/01-phase-execution-guide.md) - How to execute plans
---

## Overview

This process transforms roadmap phases into detailed work and review plans that guide implementation. Each phase gets two complementary plans: a work plan for developers and a review plan for quality assurance.

## Prerequisites

### Required Inputs
- Completed ROADMAP.md with defined phases
- Phase dependencies and sequencing
- Resource allocation per phase
- Acceptance criteria from SPEC.md

### Required Templates
- `../templates/worker-plan.yml` - Work plan template
- `../templates/review-plan.yml` - Review plan template  
- `../templates/team-skills-matrix.md` - Resource matching

## Process Overview

The phase planning consists of:
1. Phase analysis and decomposition (1 hour per phase)
2. Work package creation (1-2 hours per phase)
3. Review checkpoint design (1 hour per phase)
4. Plan synchronization (30 min per phase)
5. Validation and refinement (30 min per phase)

**Total time**: 4-6 hours per phase

## Phase 1: Phase Analysis and Decomposition

### 1.1 Extract Phase Requirements
For each phase in the roadmap:
- List all requirements to be implemented
- Identify technical components involved
- Map dependencies (internal and external)
- Define success criteria

### 1.2 Risk Assessment
- Technical risks specific to this phase
- Resource risks (skills, availability)
- Integration risks with other phases
- External dependency risks

### 1.3 Complexity Analysis
Rate each requirement on:
- Technical complexity (1-5)
- Business logic complexity (1-5)
- Integration complexity (1-5)
- Testing complexity (1-5)

Use these ratings to inform work package sizing.

## Phase 2: Work Package Creation

### 2.1 Logical Grouping
Group requirements into work packages based on:
- Component boundaries
- Feature cohesion
- Developer efficiency
- Testing approach

**Ideal work package size**: 2-5 days of effort

### 2.2 Work Package Definition
For each work package, define:
```yaml
work_package:
  id: WP-{phase}-{number}
  name: Descriptive name
  deliverables:
    - Specific deliverable 1
    - Specific deliverable 2
  requirements_covered:
    - REQ-001
    - REQ-002
  dependencies:
    - Previous work package
    - External system
  estimated_effort: X days
  skills_required:
    - Frontend development
    - API design
```

### 2.3 Task Breakdown
Break each work package into tasks:
- Implementation tasks
- Testing tasks  
- Documentation tasks
- Integration tasks

Each task should be 0.5-2 days maximum.

## Phase 3: Review Checkpoint Design

### 3.1 Checkpoint Placement
Place review checkpoints at:
- Natural feature boundaries
- Integration points
- High-risk completions
- Weekly intervals (minimum)

### 3.2 Review Criteria
For each checkpoint, define:
- What must be complete
- Quality standards to verify
- Tests that must pass
- Documentation required
- Performance benchmarks

### 3.3 Review Process
Specify for each checkpoint:
- Review type (code, design, integration)
- Reviewers required (roles/expertise)
- Review duration estimate
- Feedback mechanism
- Remediation process

## Phase 4: Plan Synchronization

### 4.1 Work-Review Alignment
Ensure:
- Each work package has corresponding review
- Checkpoints align with package completion
- Dependencies are respected in both plans
- Resource allocation doesn't conflict

### 4.2 TDD Integration
For each work package:
- Define test-first requirements
- Specify test types (unit, integration, e2e)
- Set coverage targets
- Include test review in checkpoints

### 4.3 Communication Points
Define:
- Progress reporting schedule
- Stakeholder update points
- Risk escalation triggers
- Decision points

## Phase 5: Plan Documentation

### 5.1 Create Worker Plan
Using `../templates/worker-plan.yml`, document:

```yaml
phase: X
name: Phase Name
duration: X weeks
objectives:
  - Clear objective 1
  - Clear objective 2

work_packages:
  - package: WP-X-1
    title: Package Title
    duration: X days
    dependencies: []
    tasks:
      - name: Task name
        duration: X hours
        deliverable: Specific output
    
checkpoints:
  - id: CP-X-1
    after_package: WP-X-1
    review_type: code_review
    duration: X hours
```

### 5.2 Create Review Plan
Using `../templates/review-plan.yml`, document:

```yaml
phase: X
name: Phase Name

checkpoints:
  - id: CP-X-1
    trigger: Completion of WP-X-1
    scope:
      - Code quality review
      - Test coverage verification
      - Documentation check
    criteria:
      - Tests pass with >85% coverage
      - No critical security issues
      - API documentation complete
    reviewers:
      - role: Tech Lead
        focus: Architecture alignment
      - role: QA Engineer
        focus: Test adequacy
```

### 5.3 Supporting Documentation
Create:
- Detailed test plans
- Integration guides
- Rollback procedures
- Phase-specific standards

## Quality Checks

### Completeness
- [ ] All roadmap requirements mapped to work packages
- [ ] All work packages have review checkpoints
- [ ] Dependencies explicitly documented
- [ ] Resource needs identified

### Clarity
- [ ] Tasks specific and measurable
- [ ] Acceptance criteria unambiguous
- [ ] Review criteria objective
- [ ] Communication plan clear

### Feasibility
- [ ] Effort estimates validated
- [ ] Skills available when needed
- [ ] Dependencies achievable
- [ ] Timeline realistic

### Risk Management
- [ ] High-risk items have mitigation
- [ ] Review frequency matches risk
- [ ] Escalation paths defined
- [ ] Contingency plans ready

## Common Pitfalls

### Pitfall 1: Over-detailed Planning
**Issue**: Plans too prescriptive, limiting flexibility
**Solution**: Focus on outcomes, not step-by-step instructions

### Pitfall 2: Under-specified Reviews
**Issue**: Vague review criteria lead to inconsistency
**Solution**: Quantifiable, objective criteria

### Pitfall 3: Ignoring Dependencies
**Issue**: Plans assume independent work
**Solution**: Explicit dependency mapping and buffers

### Pitfall 4: Unrealistic Sizing
**Issue**: Work packages too large or small
**Solution**: Historical data calibration

## Outputs

### Required Deliverables
```
plan/
├── phase-1/
│   ├── worker-plan.yml
│   ├── review-plan.yml
│   └── supporting/
│       ├── test-plan.md
│       └── integration-guide.md
├── phase-2/
│   ├── worker-plan.yml
│   └── review-plan.yml
```

### Success Criteria
- Plans executable without clarification
- Clear path from requirements to delivery
- Review points prevent quality drift
- Realistic timeline with buffers

## Next Steps

With phase plans complete:
1. Run [Alignment Validation](03-alignment-validation.md)
2. Get stakeholder approval
3. Prepare for [Phase Execution](../03-execution/01-phase-execution-guide.md)

Remember: Good plans are living documents - update based on execution learnings.