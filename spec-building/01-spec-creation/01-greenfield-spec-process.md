# Greenfield Spec Process

---
Next: [Spec Quality Review](03-spec-quality-review.md)
Related: 
  - [Repository Spec Process](02-repository-spec-process.md) - For existing codebases
  - [Spec Quality Review](03-spec-quality-review.md) - Quality assurance process
  - [Roadmap Creation](../02-planning/01-spec-to-roadmap.md) - Next step after approval
---

## Overview
A depth-first, outcome-focused approach to building extremely robust software specifications that serve as the definitive source for all downstream planning and implementation.

## Core Principles
1. **Outcome-First**: Define end states before solutions
2. **Evidence-Based**: Every decision backed by research or data
3. **Comprehensive Coverage**: No stone left unturned
4. **Anti-Sycophancy**: Challenge assumptions, seek truth
5. **Progressive Depth**: Layer detail systematically

## Prerequisites
- Project vision or problem statement
- Committed stakeholders
- 20-30 hours total commitment
- Willingness to challenge assumptions

## Phase 0: Template Preparation (1 hour)

**Objective**: Ensure all elicitation templates are ready

1. **Generate Required Templates**
   ```
   Templates to create:
   - ../templates/requirements/outcome-definition.md
   - ../templates/requirements/user-journey-detailed.md
   - ../templates/requirements/acceptance-scenarios.md
   - ../templates/requirements/non-functional-requirements.md
   - ../templates/requirements/constraints-assumptions.md
   - ../templates/requirements/success-metrics.md
   ```

2. **User Interaction**
   - Present templates with examples
   - Explain importance of each section
   - Request: "Please fill out these templates. Reply 'ready' when complete"
   - WAIT for user confirmation
   - Read and validate completeness

**Gate 0**: Templates Complete
- [ ] All templates filled with substantive content
- [ ] No sections marked "TBD" or left empty
- [ ] Examples replaced with project-specific content

## Phase 1: Deep Discovery (4-6 hours)

**Objective**: Build comprehensive understanding of desired outcomes

### 1.1 Outcome Mapping
- Read all completed templates
- Extract and categorize outcomes:
  - Business outcomes
  - User outcomes  
  - Technical outcomes
  - Quality outcomes

### 1.2 Scenario Excavation
For each user story:
- Generate 5-10 concrete scenarios
- Include happy paths, edge cases, failure modes
- Create acceptance tests for each
- Document expected behaviors

### 1.3 Constraint Analysis
- Technical constraints (must use X, can't use Y)
- Business constraints (budget, timeline, compliance)
- Organizational constraints (team size, skills)
- External constraints (regulations, dependencies)

### 1.4 Anti-Sycophancy Check
**Challenge Session**: Present findings and actively challenge:
- "What could go wrong with this approach?"
- "What are we assuming that might not be true?"
- "What requirements conflict with each other?"
- "What's the hardest part we're glossing over?"

**Gate 1**: Discovery Complete
- [ ] 100+ specific requirements identified
- [ ] All major scenarios documented
- [ ] Constraints comprehensively mapped
- [ ] Assumptions explicitly challenged
- [ ] User confirms nothing major missed

## Phase 2: Forensic Analysis (3-4 hours)

**Objective**: Decompose and structure requirements with surgical precision

### 2.1 Requirement Surgery
For each requirement:
- Decompose until atomic
- Classify by type (functional, quality, constraint)
- Identify dependencies
- Define measurable acceptance criteria
- Assign criticality score (1-10)

### 2.2 Outcome Traceability
Create bi-directional mapping:
- Requirement → Outcome(s) it serves
- Outcome → Requirements that deliver it
- Identify orphan requirements (no outcome)
- Identify unrealized outcomes (no requirements)

### 2.3 Conflict Resolution
- Identify conflicting requirements
- Document trade-off options
- Get user decisions on conflicts
- Record rationale for future reference

### 2.4 Completeness Analysis
Use multiple lenses:
- CRUD analysis for all entities
- State transition coverage
- Error handling for all operations  
- Performance requirements for all features
- Security requirements for all data

**Gate 2**: Analysis Complete
- [ ] Zero compound requirements remain
- [ ] 100% requirements have acceptance criteria
- [ ] All conflicts resolved with documented rationale
- [ ] Completeness verified through multiple lenses
- [ ] Criticality scores assigned and validated

## Phase 3: Exhaustive Research (4-6 hours parallel)

**Objective**: Build comprehensive knowledge base for informed decisions

### 3.1 Research Planning
Create focused research missions:
```yaml
architecture_research:
  goal: Find proven patterns for our specific constraints
  deliverables:
    - 5+ architecture options with case studies
    - Performance benchmarks for each
    - Scalability limits documented
    - Failure modes analyzed
  
technology_research:
  goal: Evaluate full technology ecosystem
  deliverables:
    - Primary technology deep dive
    - All integration points mapped
    - Alternative stacks compared
    - Migration paths identified

domain_research:
  goal: Understand industry best practices
  deliverables:
    - Competitor analysis
    - Industry standards applicable
    - Regulatory requirements
    - Future trends impact
```

### 3.2 Evidence Collection
For each research finding:
- Source credibility score
- Recency/relevance check  
- Multiple source validation
- Practical applicability assessment

### 3.3 Research Synthesis
- Create decision matrices with weighted criteria
- Document assumptions in each option
- Identify knowledge gaps
- Prepare fallback options

**Gate 3**: Research Complete
- [ ] All research questions answered with evidence
- [ ] Multiple viable options for each decision
- [ ] Knowledge gaps documented with mitigation
- [ ] Decision matrices complete with weightings
- [ ] No critical unknowns remaining

## Phase 4: Architectural Deep Dive (4-5 hours)

**Objective**: Design comprehensive system architecture

### 4.1 Component Design
For each component:
- Define exact responsibilities
- Specify all interfaces (in/out)
- Document data flows
- Identify failure modes
- Design error handling
- Plan observability

### 4.2 Integration Architecture  
- Map all integration points
- Define protocols and formats
- Specify error handling
- Plan for versioning
- Design circuit breakers
- Document SLAs

### 4.3 Quality Architecture
- Performance architecture (caching, optimization)
- Security architecture (auth, encryption, audit)
- Reliability architecture (redundancy, recovery)
- Scalability architecture (horizontal, vertical)
- Maintainability architecture (modularity, documentation)

### 4.4 Future-Proofing
- Identify extension points
- Plan for likely changes
- Design for backwards compatibility
- Create deprecation strategies

**Gate 4**: Architecture Complete
- [ ] Every component fully specified
- [ ] All interfaces documented with examples
- [ ] Quality attributes architected, not hoped for
- [ ] Future changes accommodated
- [ ] No architectural unknowns

## Phase 5: Rigorous Validation (3-4 hours)

**Objective**: Verify completeness and correctness

### 5.1 Scenario Validation
- Walk through every user journey
- Trace through the architecture
- Verify all requirements covered
- Check edge cases handled
- Validate performance under load

### 5.2 Stakeholder Validation
Role-play each stakeholder:
- End users (multiple personas)
- Operators/Admins
- Developers
- Security team
- Business stakeholders

For each: "What would concern you about this spec?"

### 5.3 Formal Methods (where applicable)
- State machine verification
- Invariant checking
- Property-based testing design
- Formal protocol verification

### 5.4 Risk Assessment
- Technical risks with mitigation
- Business risks with contingencies  
- Timeline risks with buffers
- Quality risks with controls

**Gate 5**: Validation Complete
- [ ] All scenarios successfully traced
- [ ] Each stakeholder's concerns addressed
- [ ] Formal verification where applicable
- [ ] Risk register complete with mitigations
- [ ] No validation failures

## Phase 6: Specification Compilation (2-3 hours)

**Objective**: Create comprehensive, navigable specification

### 6.1 Modular Organization
```
project-name/
├── SPEC.md                          # Executive summary & navigation
├── .spec/
│   ├── outcomes/                    # What success looks like
│   │   ├── business-outcomes.md
│   │   ├── user-outcomes.md
│   │   └── technical-outcomes.md
│   ├── requirements/                # What must be built
│   │   ├── functional/
│   │   ├── non-functional/
│   │   └── constraints/
│   ├── architecture/                # How it fits together
│   │   ├── components/
│   │   ├── interfaces/
│   │   ├── data-flows/
│   │   └── deployment/
│   ├── decisions/                   # Why choices were made
│   │   ├── architecture-decisions.md
│   │   ├── technology-decisions.md
│   │   └── trade-offs.md
│   ├── validation/                  # How we know it's right
│   │   ├── test-scenarios/
│   │   ├── acceptance-criteria/
│   │   └── success-metrics.md
│   └── roadmap/                     # How to build it
│       ├── phases.md
│       ├── milestones.md
│       └── dependencies.md
```

### 6.2 Cross-References
- Every requirement links to outcomes
- Every component links to requirements  
- Every decision links to evidence
- Every risk links to mitigation

### 6.3 Living Documentation Plan
- Update triggers defined
- Validation procedures
- Review cycles
- Deprecation process

**Gate 6**: Specification Complete
- [ ] All sections populated with detail
- [ ] Cross-references verified
- [ ] Navigation clear and logical
- [ ] No broken links or missing sections
- [ ] Ready for implementation planning

## Anti-Sycophancy Mechanisms

### 1. Evidence Requirements
- No decision without data
- Multiple sources required
- Conflicting views documented
- Assumptions explicitly stated

### 2. Challenge Protocols
```
At each gate:
- "What are we missing?"
- "What could break this?"
- "What would a skeptic say?"
- "Where are we being optimistic?"
```

### 3. Red Team Reviews
- Designate devil's advocate role
- Actively seek failure modes
- Question every assumption
- Document dissenting views

### 4. Measurement Over Opinion
- Quantify where possible
- Define success metrics
- Create falsifiable claims
- Plan measurement approach

## Quality Controls

### Prevent Agent Panic
1. **Clear Boundaries**: Each phase has defined scope
2. **Progressive Detail**: Build depth incrementally
3. **Parallel Work**: Distribute cognitive load
4. **Time Boxes**: With explicit extension process
5. **Success Criteria**: Know when "done"

### Ensure Thoroughness
1. **Templates**: Force comprehensive thinking
2. **Checklists**: Catch missed items
3. **Multiple Passes**: Different lenses each time
4. **Cross-Validation**: Requirements ↔ Outcomes
5. **Formal Gates**: Can't skip steps

### Maintain Focus
1. **Outcome Orientation**: Always trace to value
2. **Criticality Scoring**: Prioritize effort
3. **Scope Control**: Document out-of-scope
4. **Decision Records**: Avoid re-litigation
5. **Structured Output**: Standard organization

## Success Metrics for Spec Quality

A spec built with this process should:
- Answer any implementation question without ambiguity
- Survive technical deep dives without major gaps
- Enable accurate effort estimation (±20%)
- Allow parallel implementation teams
- Reduce implementation surprises by 90%
- Serve as single source of truth for 6+ months

## Time Investment ROI

While this process requires 20-30 hours upfront:
- Saves 100+ hours of implementation rework
- Reduces requirement changes by 80%
- Enables accurate planning and estimation
- Allows confident architectural decisions
- Provides clear success criteria

The spec becomes the foundation for:
- Detailed implementation plans
- Test strategies
- Documentation
- Training materials
- Future enhancements