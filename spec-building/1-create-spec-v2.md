# Spec Building Process v2.0

## Overview
A streamlined, phase-gated approach to building high-quality software specifications with clear boundaries, time boxes, and quality criteria.

## Prerequisites
- Project idea or initial requirements
- Access to stakeholders
- 10-15 hours total time commitment

## Process Phases

### Phase 1: Discovery (2-4 hours)

**Objective**: Capture and understand core requirements

1. **Context Selection**
   - Review project-contexts.md
   - Identify project type (Web App, Library, CLI, etc.)
   - Load appropriate requirement template

2. **Requirements Gathering**
   - Generate/read initial requirements documents
   - Capture user stories and use cases
   - Document quality criteria
   - Identify key stakeholders and personas

3. **Initial Validation**
   - Review requirements with user
   - Clarify ambiguities
   - Confirm project vision alignment
   - Document out-of-scope items

**Gate 1**: Discovery Complete
- [ ] 80% requirements captured
- [ ] Project type identified
- [ ] Scope boundaries defined
- [ ] User confirms understanding

### Phase 2: Analysis (1-2 hours)

**Objective**: Refine and structure requirements

1. **Requirements Decomposition**
   - Break down compound requirements
   - Extract requirements from implementation details
   - Create requirement → rationale → source traceability

2. **Prioritization**
   - Apply MoSCoW classification
   - Consider dependencies
   - Balance priority distribution

3. **Acceptance Criteria**
   - Define measurable criteria for each requirement
   - Specify test conditions
   - Document edge cases

**Gate 2**: Analysis Complete
- [ ] All requirements atomic
- [ ] Priorities assigned
- [ ] Acceptance criteria defined
- [ ] No critical ambiguities

### Phase 3: Research (2-3 hours, parallel)

**Objective**: Investigate technical options with bounded scope

1. **Research Planning**
   - Define research areas based on requirements
   - Create bounded research assignments
   - Set quality criteria and stop conditions

2. **Parallel Research Execution**
   ```
   Subagent assignments:
   - Architecture patterns (60 min max)
   - Technology stack options (45 min max)
   - Tool ecosystem (45 min max)
   - Deployment strategies (30 min max)
   ```

3. **Research Synthesis**
   - Compile findings into decision matrices
   - Score options against criteria
   - Identify recommendations

**Gate 3**: Research Complete
- [ ] 3+ options per area evaluated
- [ ] Decision matrices populated
- [ ] Quality thresholds met
- [ ] Recommendations documented

### Phase 4: Design (2-3 hours)

**Objective**: Define system architecture and components

1. **Architecture Design**
   - Select architectural pattern
   - Define component boundaries
   - Specify interfaces and contracts
   - Document data flows

2. **Technology Decisions**
   - Finalize technology stack
   - Resolve integration requirements
   - Confirm compatibility
   - Plan for extensibility

3. **Non-Functional Design**
   - Performance architecture
   - Security architecture
   - Deployment architecture
   - Monitoring approach

**Gate 4**: Design Complete
- [ ] Components well-defined
- [ ] Interfaces documented
- [ ] Technology stack finalized
- [ ] Architecture diagrams created

### Phase 5: Validation (1-2 hours)

**Objective**: Ensure completeness and stakeholder alignment

1. **Consolidated Decision Session**
   - Use decision-matrix.md template
   - Make all key decisions in single session
   - Document rationales
   - Assign ownership

2. **Scenario Validation**
   - Walk through user stories
   - Validate against use cases
   - Check edge cases
   - Confirm completeness

3. **Quality Assurance**
   - Ambiguity detection
   - Consistency checking
   - Traceability verification
   - Completeness assessment

**Gate 5**: Validation Complete
- [ ] All decisions documented
- [ ] Scenarios validated
- [ ] Quality metrics met
- [ ] Stakeholder approval

### Phase 6: Decomposition (1-2 hours)

**Objective**: Create modular specs and implementation roadmap

1. **Modularization**
   - Create component-specific spec files
   - Establish cross-references
   - Define extension points
   - Document interfaces

2. **Roadmap Creation**
   - Define implementation phases
   - Set milestones and deliverables
   - Plan incremental delivery
   - Include validation checkpoints

3. **Living Documentation Plan**
   - Define update triggers
   - Establish maintenance process
   - Plan documentation automation
   - Set review cycles

**Gate 6**: Specification Complete
- [ ] Modular structure created
- [ ] Roadmap defined
- [ ] Documentation plan established
- [ ] Ready for implementation

## Output Structure

```
project-name/
├── SPEC.md                          # High-level specification
├── .spec/
│   ├── components/                  # Component specifications
│   │   ├── frontend.md
│   │   ├── backend.md
│   │   └── infrastructure.md
│   ├── interfaces/                  # Interface definitions
│   │   ├── api.md
│   │   └── data-models.md
│   ├── decisions/                   # Decision records
│   │   ├── architecture.md
│   │   └── technology-stack.md
│   ├── research/                    # Research findings
│   │   ├── architecture-options.md
│   │   └── tool-evaluation.md
│   └── roadmap.md                   # Implementation roadmap
```

## Tooling and Automation

### Templates Used
- `templates/phase-gates.md` - Exit criteria checklists
- `templates/project-contexts.md` - Project type templates
- `templates/research-criteria.md` - Research quality bounds
- `templates/decision-matrix.md` - Decision framework

### Subagent Coordination
```yaml
research_agents:
  architecture:
    timeout: 60m
    deliverable: .spec/research/architecture-options.md
  
  tools:
    timeout: 45m
    deliverable: .spec/research/tool-evaluation.md
  
  deployment:
    timeout: 30m
    deliverable: .spec/research/deployment-strategies.md
```

## Best Practices

1. **Time Box Adherence**: Respect phase time limits
2. **Gate Discipline**: Don't proceed without meeting criteria
3. **Parallel Work**: Use subagents for research tasks
4. **Decision Velocity**: Make decisions quickly with "good enough" threshold
5. **Documentation**: Record decisions immediately
6. **Iteration Control**: Limit validation cycles
7. **Context Awareness**: Only load relevant requirements

## Common Pitfalls to Avoid

1. Analysis paralysis in research phase
2. Over-engineering for simple projects
3. Skipping gates to save time
4. Repetitive validation cycles
5. Scope creep during discovery
6. Perfect solution seeking

## Customization

This process can be scaled:
- **Minimal**: Skip formal research, use 1-hour validation
- **Standard**: Follow as described
- **Comprehensive**: Add formal methods, extended validation

Select based on:
- Project complexity
- Team size
- Risk tolerance
- Time constraints

## Success Metrics

- Total time: 10-15 hours (vs 20-30 hours)
- Validation cycles: 1-2 (vs 8+)
- Decision clarity: 100% documented
- Implementation readiness: Clear roadmap
- Stakeholder satisfaction: Single approval session