# Spec Building Phase Gates

## Overview
Each phase has defined entry criteria, exit criteria, and time boxes to ensure efficient progress while maintaining quality.

## Phase 1: Discovery (2-4 hours)

### Entry Criteria
- Initial project description or idea
- Access to stakeholders or requirements documents
- Templates available (user-story, use-case, quality-criteria)

### Exit Criteria
- [ ] Core requirements documented in structured format
- [ ] User stories captured for main personas
- [ ] Initial scope boundaries defined
- [ ] 80% confidence that major requirements are identified
- [ ] User confirms understanding of project vision

### Quality Metrics
- Requirements coverage: >80% of known scope
- Ambiguity score: <20% of requirements need clarification
- Stakeholder alignment: Confirmed by user

### Time Box
- Minimum: 2 hours (simple projects)
- Maximum: 4 hours (complex projects)
- Extension requires explicit justification

## Phase 2: Analysis (1-2 hours)

### Entry Criteria
- Completed discovery phase
- Raw requirements documented
- User available for clarification

### Exit Criteria
- [ ] All compound requirements decomposed
- [ ] Requirements prioritized (MoSCoW)
- [ ] Acceptance criteria defined for each requirement
- [ ] Traceability matrix created (requirement → rationale → source)
- [ ] No critical ambiguities remaining

### Quality Metrics
- Decomposition completeness: 100% of compound requirements split
- Acceptance criteria: 100% of requirements have measurable criteria
- Priority distribution: Reasonable balance (not all "Must have")

### Time Box
- Minimum: 1 hour
- Maximum: 2 hours
- Focus on critical path items if time-constrained

## Phase 3: Research (2-3 hours parallel)

### Entry Criteria
- Analyzed requirements available
- Research scope defined
- Success criteria established

### Exit Criteria
- [ ] Minimum 3 viable options per research area
- [ ] Pros/cons documented for each option
- [ ] Options meet defined quality thresholds
- [ ] Decision matrix populated
- [ ] No critical unknowns remaining

### Quality Metrics
- Option quality: All options meet minimum viability criteria
- Comparison depth: Standardized evaluation across options
- Coverage: All critical technical decisions have research

### Time Box
- Maximum: 3 hours total (can be parallelized)
- Individual research tasks: 30-60 minutes each
- Hard stop when quality threshold met

## Phase 4: Design (2-3 hours)

### Entry Criteria
- Research completed
- Technical decisions made
- Architecture patterns selected

### Exit Criteria
- [ ] Component boundaries defined
- [ ] Interface specifications documented
- [ ] Technology stack finalized
- [ ] Deployment architecture specified
- [ ] Security and performance requirements integrated

### Quality Metrics
- Component independence: Low coupling score
- Interface completeness: All integration points defined
- Architecture fitness: Meets all non-functional requirements

### Time Box
- Minimum: 2 hours
- Maximum: 3 hours
- Iterative refinement within time box

## Phase 5: Validation (1-2 hours)

### Entry Criteria
- Design phase complete
- Spec document drafted
- Validation criteria defined

### Exit Criteria
- [ ] MoSCoW prioritization validated
- [ ] Trade-offs documented and accepted
- [ ] Ambiguities resolved to acceptable level
- [ ] Stakeholder scenarios validated
- [ ] Quality metrics defined

### Quality Metrics
- Validation coverage: All critical paths tested
- Ambiguity level: <5% of spec requires clarification
- Stakeholder satisfaction: Confirmed acceptance

### Time Box
- Minimum: 1 hour
- Maximum: 2 hours
- Batch validations for efficiency

## Phase 6: Decomposition (1-2 hours)

### Entry Criteria
- Validated spec available
- Modularization strategy defined
- File structure planned

### Exit Criteria
- [ ] Spec modularized into logical components
- [ ] Cross-references established
- [ ] Extension points documented
- [ ] Roadmap created with clear phases
- [ ] Living documentation plan defined

### Quality Metrics
- Module cohesion: High internal cohesion
- Documentation coverage: All modules documented
- Roadmap clarity: Phases have clear deliverables

### Time Box
- Minimum: 1 hour
- Maximum: 2 hours
- Focus on logical boundaries

## Gate Decision Framework

### Go Decision
- All exit criteria met
- Quality metrics within acceptable range
- No blocking issues identified
- User approval received (where required)

### Conditional Go
- Minor criteria missed but documented
- Mitigation plan in place
- Risk accepted by user
- Clear path to resolution

### No Go
- Critical exit criteria not met
- Quality metrics below threshold
- Blocking issues without mitigation
- User explicitly requests revision

## Time Box Management

### Extension Triggers
- Unexpected complexity discovered
- Critical requirement changes
- Technical blocker encountered
- User requests additional scope

### Extension Process
1. Document reason for extension
2. Define new time box (max +50%)
3. Get user approval
4. Set hard stop regardless

### Efficiency Tips
- Parallelize where possible
- Batch similar activities
- Use templates and checklists
- Focus on critical path first
- Document decisions immediately