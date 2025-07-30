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

**Real Example - TaskMaster Priority Matrix**
| Requirement | Priority | Rationale | Dependencies |
|-------------|----------|-----------|---------------|
| User Auth | Must | Security foundation | None |
| Task CRUD | Must | Core functionality | User Auth |
| Real-time Updates | Must | Key differentiator | Task CRUD |
| Search | Must | Usability requirement | Task CRUD |
| Slack Integration | Should | Adoption driver | Notifications |
| Mobile Apps | Could | Phase 2 candidate | Web stable |
| AI Predictions | Won't | Future enhancement | - |

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

**TaskMaster Real-time Architecture Decision Example**
```markdown
## Decision: Real-time Updates Architecture

**Options Considered:**
1. WebSockets with Socket.io - Bidirectional, mature, fallback support
2. Server-Sent Events (SSE) - Simple, one-way, HTTP-based
3. Long Polling - Compatible, inefficient, higher latency

**Decision Matrix:**
| Criteria | Weight | WebSockets | SSE | Long Polling |
|----------|--------|------------|-----|--------------|
| Latency | 30% | 10 (300ms) | 8 (500ms) | 5 (2s) |
| Scalability | 25% | 8 | 9 | 6 |
| Complexity | 20% | 6 | 9 | 10 |
| Browser Support | 15% | 9 | 7 | 10 |
| Team Experience | 10% | 8 | 5 | 9 |
| **Total Score** | | **8.15** | **7.85** | **7.25** |

**Decision:** WebSockets with Socket.io

**Rationale:**
- Best latency for real-time collaboration
- Socket.io provides automatic fallback
- Team has prior experience
- Proven at scale (Slack, Trello use it)

**Consequences:**
- Positive: Sub-second updates, reliable reconnection
- Negative: More complex than SSE, stateful connections
- Mitigations: Use Redis adapter for scaling, implement heartbeat
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