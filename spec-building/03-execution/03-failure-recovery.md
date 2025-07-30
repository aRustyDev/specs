# Failure Recovery Guide

---
Previous: [Change Management](02-change-management.md)
Related:
  - [Phase Execution Guide](01-phase-execution-guide.md) - Normal execution flow
  - [Change Management](02-change-management.md) - Managing scope changes
  - [Spec Quality Review](../01-spec-creation/03-spec-quality-review.md) - Quality standards
---

## Overview
This guide provides structured approaches for recovering from failures at any stage of the spec-to-execution pipeline. It focuses on practical recovery paths rather than blame, ensuring projects can continue despite setbacks.

## Failure Types and Recovery Strategies

### 1. Spec Creation Failures

#### 1.1 Low Quality Score (<70)
**Symptoms**: 
- Spec quality score below threshold
- Multiple missing sections
- Unclear requirements

**Immediate Actions**:
1. Don't panic - this is common for complex projects
2. Review the quality report to identify specific gaps
3. Prioritize issues by impact:
   - Missing requirements (High)
   - Unclear success criteria (High)
   - Incomplete architecture (Medium)
   - Documentation gaps (Low)

**Recovery Options**:

**Option A: Focused Improvement Sprint**
- Time: 1-2 days
- Approach:
  1. Address only blocking issues (score <70 items)
  2. Schedule stakeholder sessions for missing info
  3. Use examples from similar projects
  4. Aim for 75+ score, not perfection

**Option B: Incremental Specification**
- Time: Ongoing
- Approach:
  1. Define Phase 1 requirements only (MVP)
  2. Mark future phases as "TBD with dependencies"
  3. Proceed with partial spec (with approval)
  4. Refine spec as project progresses

**Option C: Pivot to Prototype**
- Time: 1 week
- Approach:
  1. Build proof-of-concept for unclear areas
  2. Use prototype to elicit requirements
  3. Document learnings
  4. Retry spec creation with new knowledge

#### 1.2 Stakeholder Disagreement
**Symptoms**:
- Conflicting requirements
- No consensus on priorities
- Approval deadlock

**Recovery Path**:
1. Document all viewpoints without judgment
2. Create options matrix:
   ```
   | Requirement | Stakeholder A | Stakeholder B | Impact |
   |-------------|---------------|---------------|--------|
   | Feature X   | Must Have     | Won't Have    | High   |
   ```
3. Escalate to executive sponsor with:
   - Clear options
   - Impact analysis
   - Recommendation
4. If no resolution: Proceed with documented assumption and risk

### 2. Roadmap Generation Failures

#### 2.1 Unresolvable Dependencies
**Symptoms**:
- Circular dependencies
- External blockers
- Technical impossibilities

**Recovery Options**:

**Option A: Dependency Breaking**
1. Identify minimal interface to break cycle
2. Create stub/mock for blocked dependency
3. Plan for later integration
4. Document technical debt created

**Option B: Phased Dependencies**
1. Split problematic component into phases:
   - Phase 1: Basic version (no dependency)
   - Phase 2: Full version (with dependency)
2. Adjust roadmap to accommodate
3. Update risk register

**Option C: Architecture Revision**
1. Revisit architectural decisions
2. Consider alternative patterns
3. May require spec update (controlled change)

#### 2.2 Resource Constraints
**Symptoms**:
- Timeline exceeds constraints
- Team size insufficient
- Budget overrun

**Recovery Path**:
1. Apply MoSCoW rigorously:
   - Keep all "Must Have" (or challenge classification)
   - Defer 50% of "Should Have"
   - Drop all "Could Have" for v1
2. Identify parallel work opportunities
3. Consider:
   - Outsourcing specific components
   - Using existing libraries/services
   - Simplifying architecture
4. Present options to stakeholders:
   - Original scope, extended timeline
   - Reduced scope, original timeline
   - Phased delivery approach

### 3. Phase Planning Failures

#### 3.1 Work/Review Plan Misalignment
**Symptoms**:
- Checkpoints don't match
- Different understanding of deliverables
- Timeline conflicts

**Immediate Fix**:
1. Stop all work on affected phase
2. Joint session with work planner and reviewer
3. Create unified understanding:
   ```
   Checkpoint X:
   - Worker delivers: [specific list]
   - Reviewer validates: [specific criteria]
   - Success looks like: [concrete example]
   ```
4. Update both plans simultaneously
5. Version control the change

#### 3.2 Estimation Failures
**Symptoms**:
- Phase taking 2x+ estimated time
- Blocking issues discovered mid-phase
- Team overwhelmed

**Recovery Options**:

**Option A: Phase Splitting**
1. Stop current phase at next checkpoint
2. Define "Phase Xa" as work completed
3. Create "Phase Xb" for remaining work
4. Adjust downstream phases
5. Apply learnings to future estimates

**Option B: Scope Reduction**
1. Identify "good enough" version of deliverables
2. Move refinements to "Phase X.1" (enhancement phase)
3. Document technical debt
4. Continue with reduced scope

**Option C: Resource Augmentation**
1. Bring in specialist for blocking issue
2. Temporary team expansion
3. Pair programming to share knowledge
4. Accept temporary velocity loss

### 4. Mid-Phase Execution Failures

#### 4.1 Technical Blocker Discovered
**Symptoms**:
- Assumed approach doesn't work
- Performance requirements impossible
- Security vulnerability found

**Recovery Protocol**:
1. **STOP** - Don't continue down failing path
2. **Document**:
   - What was attempted
   - Why it failed
   - What was learned
3. **Assess Impact**:
   - Can requirement be relaxed?
   - Is there alternative approach?
   - What's the schedule impact?
4. **Decide Path**:
   - Fix and continue (if <2 days)
   - Workaround and document debt
   - Escalate for requirement change

#### 4.2 Quality Gate Failures
**Symptoms**:
- Tests failing at checkpoint
- Review rejection
- Performance not meeting targets

**Recovery Steps**:
1. Analyze root cause:
   - Skill gap → Training/pairing
   - Unclear requirements → Clarification session
   - Technical debt → Refactoring sprint
   - Wrong approach → Architecture review

2. Create recovery plan:
   ```
   Issue: [Specific failure]
   Root Cause: [Why it happened]
   Fix Approach: [How to resolve]
   Time Needed: [Realistic estimate]
   Prevention: [How to avoid recurrence]
   ```

3. Negotiate timeline:
   - Fix in current phase (if small)
   - Defer to debt sprint
   - Accept with documented risk

### 5. Integration Failures

#### 5.1 Component Integration Issues
**Symptoms**:
- APIs don't match spec
- Performance degradation
- Unexpected behaviors

**Recovery Approach**:
1. Create integration test suite that exposes all issues
2. Prioritize by user impact
3. Fix options:
   - Adapter pattern for mismatches
   - Performance optimization sprint
   - Behavioral documentation and training
4. Update specs to match reality (controlled)

#### 5.2 End-to-End Failures
**Symptoms**:
- System doesn't meet user needs
- Workflow breaks down
- Missing critical features

**Major Recovery Options**:

**Option A: Pivot to MVP**
1. Identify absolute minimum viable path
2. Disable/hide non-working features
3. Ship MVP for feedback
4. Plan recovery phases

**Option B: Timeline Extension**
1. Full stop and reassessment
2. Honest timeline with buffers
3. Stakeholder re-alignment
4. Consider phased launch

## Failure Prevention Strategies

### 1. Early Detection
- Daily checkpoint micro-reviews
- Automated quality gates
- Pair programming for complex parts
- Regular stakeholder demos

### 2. Risk Mitigation
- Build riskiest parts first
- Have Plan B for critical components
- Time-box research/spikes
- Document assumptions explicitly

### 3. Communication Protocols
- No-blame failure reporting
- Daily blockers discussion
- Escalation within 24 hours
- Celebrate learning from failures

## Failure Documentation Template

```markdown
## Failure Report: [Date]

### What Failed
- Phase/Component: 
- Failure Type:
- Impact Level: [Low/Medium/High/Critical]

### Timeline
- Detected: [When]
- Root Cause Found: [When]
- Recovery Started: [When]
- Resolution: [When/Ongoing]

### Root Cause Analysis
- Primary Cause:
- Contributing Factors:
- Could have been prevented by:

### Recovery Actions Taken
1. Immediate:
2. Short-term:
3. Long-term:

### Lessons Learned
- What worked:
- What didn't:
- Process improvements:

### Prevention Measures
- [ ] Process update
- [ ] Checklist addition
- [ ] Training needed
- [ ] Tool improvement
```

## Escalation Matrix

| Failure Severity | Timeline Impact | Escalate To | Timeline |
|------------------|-----------------|-------------|----------|
| Low | <1 day | Team Lead | Next standup |
| Medium | 1-3 days | Project Manager | Within 4 hours |
| High | 3-7 days | Product Owner | Within 2 hours |
| Critical | >1 week | Executive Sponsor | Immediately |

## Key Principles

1. **Fail Fast**: Detect and admit failures quickly
2. **Learn Always**: Every failure teaches something
3. **Communicate Early**: Bad news doesn't improve with age
4. **Focus on Recovery**: Solutions over blame
5. **Document Everything**: Future teams need this knowledge

## Recovery Success Metrics

Track these to improve recovery processes:
- Time to detect failure
- Time to root cause
- Time to recovery
- Recurrence rate
- Lesson implementation rate

Remember: Projects rarely fail from one big issue - they fail from many small issues handled poorly. Good recovery practices turn potential project failures into minor setbacks.