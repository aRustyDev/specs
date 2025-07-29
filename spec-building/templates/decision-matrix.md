# Unified Decision-Making Template

## Overview
This template replaces repetitive validation cycles with a structured decision framework that captures all key decisions in one pass.

## Decision Categories

### 1. Requirements Decisions

**Priority Decisions (MoSCoW)**
```markdown
| Requirement | Priority | Rationale | Dependencies |
|-------------|----------|-----------|---------------|
| [Feature A] | Must | Core business value | None |
| [Feature B] | Should | User satisfaction | Feature A |
| [Feature C] | Could | Nice to have | Feature A, B |
| [Feature D] | Won't | Out of scope | - |

**Validation**: 
- [ ] Priorities reflect business value
- [ ] Dependencies considered
- [ ] Resource constraints applied
```

**Trade-off Decisions**
```markdown
| Trade-off | Option A | Option B | Decision | Rationale |
|-----------|----------|----------|----------|-----------|
| Performance vs Cost | High perf, high cost | Adequate perf, low cost | B | Budget constraints |
| Feature vs Time | Full feature | MVP | MVP | Time to market |
| Quality vs Speed | 100% coverage | 80% coverage | 80% | Diminishing returns |

**Validation**:
- [ ] Trade-offs align with project goals
- [ ] Decisions documented with clear rationale
- [ ] Stakeholders agree with trade-offs
```

### 2. Technical Decisions

**Architecture Decisions**
```markdown
## Decision: [Architecture Pattern]

**Options Considered:**
1. Option A: [Description]
2. Option B: [Description]
3. Option C: [Description]

**Decision Matrix:**
[Include scored matrix from research]

**Decision:** Option [X]

**Rationale:**
- Primary reason
- Supporting factors
- Risk mitigation

**Consequences:**
- Positive: [List benefits]
- Negative: [List drawbacks]
- Mitigations: [How to address drawbacks]

**Validation:**
- [ ] Aligns with requirements
- [ ] Team has capability
- [ ] Risks acceptable
```

**Technology Stack Decisions**
```markdown
## Stack Components

| Layer | Technology | Alternative | Decision | Rationale |
|-------|------------|-------------|----------|-----------|
| Frontend | React | Vue | React | Team expertise |
| Backend | Node.js | Python | Node.js | JS everywhere |
| Database | PostgreSQL | MongoDB | PostgreSQL | ACID compliance |
| Cache | Redis | Memcached | Redis | Feature set |

**Integration Points:**
- [ ] All components compatible
- [ ] Version conflicts resolved
- [ ] Licenses compatible
```

### 3. Quality Decisions

**Quality Metrics**
```markdown
| Metric | Target | Minimum | Measurement |
|--------|--------|---------|-------------|
| Test Coverage | 90% | 80% | Jest coverage |
| Performance | <200ms | <500ms | p95 latency |
| Availability | 99.9% | 99% | Uptime monitoring |
| Code Quality | A | B | SonarQube |

**Validation:**
- [ ] Targets achievable
- [ ] Measurement tools available
- [ ] Costs justified
```

### 4. Risk Decisions

**Risk Assessment**
```markdown
| Risk | Probability | Impact | Mitigation | Owner | Decision |
|------|------------|--------|------------|-------|----------|
| Skill gap | Medium | High | Training plan | Team Lead | Accept with mitigation |
| Timeline | High | Medium | Phased delivery | PM | Accept |
| Integration | Low | High | Early testing | Tech Lead | Monitor |

**Validation:**
- [ ] All major risks identified
- [ ] Mitigations practical
- [ ] Ownership assigned
```

## Consolidated Validation Checklist

### Requirements Validation
- [ ] All requirements have clear acceptance criteria
- [ ] No conflicting requirements
- [ ] Scope boundaries defined
- [ ] Dependencies mapped
- [ ] Priorities agreed

### Technical Validation
- [ ] Architecture supports all requirements
- [ ] Technology choices justified
- [ ] Integration points defined
- [ ] Performance targets achievable
- [ ] Security requirements addressed

### Quality Validation
- [ ] Quality metrics defined
- [ ] Testing strategy clear
- [ ] Documentation approach agreed
- [ ] Maintenance plan considered

### Stakeholder Validation
- [ ] User stories validated
- [ ] Business value confirmed
- [ ] Resource allocation approved
- [ ] Timeline acceptable
- [ ] Success criteria agreed

## Decision Recording Template

```markdown
# Decision Record: [Date]

## Participants
- [Name, Role]
- [Name, Role]

## Decisions Made

### Requirements
1. [Decision]: [Rationale]
2. [Decision]: [Rationale]

### Technical
1. [Decision]: [Rationale]
2. [Decision]: [Rationale]

### Quality
1. [Decision]: [Rationale]

### Risks
1. [Decision]: [Rationale]

## Action Items
- [ ] [Action] - [Owner] - [Due Date]
- [ ] [Action] - [Owner] - [Due Date]

## Next Steps
- [What happens next]
- [When to revisit decisions]
```

## Efficiency Guidelines

### Single-Pass Validation
1. **Prepare**: Gather all materials before session
2. **Structure**: Use templates to guide discussion
3. **Time-box**: 2 hours maximum for all validations
4. **Decide**: Make decisions in session, not after
5. **Document**: Record decisions immediately

### Avoiding Re-validation
- Set "good enough" thresholds upfront
- Document decisions with clear rationale
- Establish change control process
- Define triggers for re-evaluation
- Trust the process

### Batch Processing
Group related decisions:
- All priorities in one discussion
- All trade-offs together
- All risks assessed at once
- Single approval session

## Change Management

### When to Revisit Decisions
- Major requirement change
- Critical new information
- Significant risk materialized
- Project phase transition

### Change Process
1. Document what changed
2. Assess impact on decisions
3. Update only affected decisions
4. Communicate changes
5. Update documentation

## Best Practices

1. **Decision, Not Discussion**: Focus on making decisions
2. **Good Enough**: Perfect is enemy of done
3. **Document Why**: Rationale more important than decision
4. **Single Source**: One place for all decisions
5. **Time Box**: Enforce time limits strictly