# Progressive Validation Gates

## Overview
Each gate ensures specification quality through objective criteria and evidence-based validation, preventing progression until quality thresholds are met.

## Gate 0: Template Completeness
**Purpose**: Ensure comprehensive input data

### Entry Criteria
- All templates generated and provided to user
- User has indicated ready to proceed

### Validation Checklist
- [ ] **Outcome Definition**: Every section has specific, measurable content
- [ ] **User Journeys**: At least 3 detailed journeys per user type
- [ ] **Acceptance Scenarios**: Minimum 20 scenarios covering all features
- [ ] **Non-Functional Requirements**: All categories have metrics
- [ ] **Constraints**: Technical, business, and organizational documented
- [ ] **Success Metrics**: Quantifiable and time-bound

### Quality Metrics
| Template | Completeness | Specificity | Measurability |
|----------|--------------|-------------|---------------|
| Outcomes | >95% sections | No vague terms | 100% quantified |
| Journeys | All steps detailed | Actions specific | Time estimates |
| Scenarios | Pre/post/steps | Data specified | Pass/fail clear |
| Non-Functional | All applicable | Numbers not words | Test methods |

### Rejection Criteria
- Any section marked "TBD" or "[TODO]"
- Generic examples not replaced
- Unmeasurable success criteria
- Missing critical user types

**GATE DECISION**: ⬜ PASS / ⬜ FAIL

---

## Gate 1: Discovery Depth
**Purpose**: Ensure comprehensive understanding

### Validation Criteria

#### Requirement Coverage
- [ ] 100+ atomic requirements identified
- [ ] Requirements traceable to outcomes
- [ ] Edge cases explicitly documented
- [ ] Anti-requirements clearly stated

#### Scenario Completeness
```
Minimum scenarios by type:
- Happy path: 100% feature coverage
- Edge cases: 3+ per major feature  
- Error cases: 2+ per integration point
- Performance: 1+ per critical operation
```

#### Stakeholder Coverage
- [ ] All user personas have journeys
- [ ] Admin workflows documented
- [ ] API consumers considered
- [ ] Operations team needs captured

### Evidence Requirements
- User interview notes/recordings
- Competitive analysis documentation
- Industry standard references
- Existing system analysis (if applicable)

### Anti-Sycophancy Check
Run challenge session, document:
- Assumptions challenged: ___
- Conflicts identified: ___
- Scope concerns raised: ___
- Evidence of pushback: ___

**GATE DECISION**: ⬜ PASS / ⬜ FAIL

---

## Gate 2: Analysis Rigor
**Purpose**: Ensure requirements are implementable

### Decomposition Validation
- [ ] No compound requirements (AND/OR statements)
- [ ] Requirements state what, not how
- [ ] Dependencies mapped in graph/matrix
- [ ] Circular dependencies resolved

### Measurement Criteria
| Requirement Type | Has Acceptance Criteria | Testable | Measurable |
|-----------------|------------------------|----------|------------|
| Functional | 100% | 100% | 100% |
| Performance | 100% | 100% | 100% |
| Security | 100% | 95%+ | 90%+ |
| Usability | 100% | 90%+ | 80%+ |

### Priority Distribution
```
Expected distribution:
- Must Have: 30-40%
- Should Have: 30-40%  
- Could Have: 20-30%
- Won't Have: 5-10%

Red flags:
- >60% Must Have = Unrealistic
- <20% Must Have = Unclear MVP
```

### Completeness Verification
Run analysis lenses:
- [ ] CRUD complete for all entities
- [ ] State transitions fully mapped
- [ ] Error handling comprehensive
- [ ] Integration points specified
- [ ] Data flows documented

**GATE DECISION**: ⬜ PASS / ⬜ FAIL

---

## Gate 3: Research Validation
**Purpose**: Ensure decisions are evidence-based

### Research Coverage
| Area | Options Evaluated | Evidence Quality | Decision Confidence |
|------|------------------|------------------|-------------------|
| Architecture | ≥3 | High/Med/Low | >80% |
| Technology | ≥3 | High/Med/Low | >80% |
| Infrastructure | ≥3 | High/Med/Low | >80% |
| Tools | ≥3 | High/Med/Low | >80% |

### Evidence Standards
Each research finding must have:
- [ ] Primary source documentation
- [ ] Performance benchmarks/metrics
- [ ] Production usage examples
- [ ] Failure case analysis
- [ ] Total cost of ownership

### Decision Matrix Validation
- [ ] All criteria weighted appropriately
- [ ] Scoring methodology documented
- [ ] Sensitivity analysis performed
- [ ] Minority opinions recorded

### Knowledge Gap Assessment
- Critical gaps identified: ___
- Mitigation strategies defined: ___
- Acceptable risk level confirmed: ⬜

**GATE DECISION**: ⬜ PASS / ⬜ FAIL

---

## Gate 4: Architecture Completeness
**Purpose**: Ensure implementation-ready design

### Component Specification
Each component must define:
- [ ] Single responsibility clearly stated
- [ ] All interfaces (API contracts)
- [ ] Data models/schemas
- [ ] Error responses
- [ ] Performance bounds
- [ ] Security controls

### Integration Validation
```yaml
For each integration:
  protocol: Specified (HTTP/gRPC/etc)
  format: Defined (JSON/Protobuf/etc)
  errors: All cases handled
  retry: Strategy defined
  timeout: Limits set
  fallback: Behavior specified
```

### Quality Architecture
Verify architectural support for:
- [ ] Performance requirements achievable
- [ ] Security requirements implementable
- [ ] Scalability path clear
- [ ] Reliability mechanisms in place
- [ ] Monitoring/observability built-in

### Architectural Risks
- Single points of failure: ___
- Bottlenecks identified: ___
- Technical debt created: ___
- Mitigation plans: ⬜

**GATE DECISION**: ⬜ PASS / ⬜ FAIL

---

## Gate 5: Validation Completeness
**Purpose**: Ensure spec is production-ready

### Scenario Trace Success
- [ ] 100% user journeys traceable
- [ ] All edge cases handled
- [ ] Performance scenarios valid
- [ ] Security scenarios pass
- [ ] Error scenarios recoverable

### Stakeholder Sign-off
| Stakeholder | Concerns Raised | Resolved | Approved |
|-------------|----------------|----------|----------|
| Product Owner | | ⬜ | ⬜ |
| Tech Lead | | ⬜ | ⬜ |
| Security | | ⬜ | ⬜ |
| Operations | | ⬜ | ⬜ |
| QA Lead | | ⬜ | ⬜ |

### Risk Register Complete
- [ ] All risks have probability + impact
- [ ] Mitigation strategies defined
- [ ] Owners assigned
- [ ] Triggers identified
- [ ] No unacceptable risks

### Formal Verification (where applicable)
- State machines verified: ⬜
- Invariants checked: ⬜
- Properties proven: ⬜
- Edge cases covered: ⬜

**GATE DECISION**: ⬜ PASS / ⬜ FAIL

---

## Gate 6: Specification Quality
**Purpose**: Ensure spec is maintainable and complete

### Documentation Quality
- [ ] No ambiguous language
- [ ] All acronyms defined
- [ ] Examples for complex concepts
- [ ] Diagrams where helpful
- [ ] Cross-references working

### Completeness Check
```
Required sections present:
□ Executive summary
□ Outcomes/objectives  
□ Requirements (categorized)
□ Architecture/design
□ Component specifications
□ Interface definitions
□ Decision rationale
□ Risk analysis
□ Implementation roadmap
□ Success metrics
```

### Traceability Verification
- Outcome → Requirements: ⬜ Complete
- Requirements → Components: ⬜ Complete  
- Components → Interfaces: ⬜ Complete
- Decisions → Evidence: ⬜ Complete

### Future-Proofing
- [ ] Extension points documented
- [ ] Deprecation paths defined
- [ ] Version strategy clear
- [ ] Migration guides outlined

### Final Quality Metrics
- Spec completeness: ___% 
- Cross-reference accuracy: ___%
- Decision evidence coverage: ___%
- Risk mitigation coverage: ___%

**GATE DECISION**: ⬜ PASS / ⬜ FAIL

---

## Gate Failure Protocol

### When a Gate Fails
1. Document specific failures
2. Create remediation plan
3. Estimate additional time needed
4. Get stakeholder approval for extension
5. Re-execute only failed sections
6. Re-validate at same gate

### Bypassing Gates
Gates can only be bypassed with:
- Documented justification
- Risk acceptance by stakeholders
- Compensating controls defined
- Executive approval

### Quality Metrics Tracking
Track for process improvement:
- First-pass gate success rate
- Average remediation time
- Common failure patterns
- Process bottlenecks

## Continuous Improvement
After each spec completion:
- Conduct retrospective
- Update gate criteria based on lessons
- Refine templates
- Adjust time estimates
- Share learnings