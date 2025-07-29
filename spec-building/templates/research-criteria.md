# Research Quality Criteria and Bounds

## Overview
This document defines quality thresholds, success criteria, and bounded scopes for research activities during spec building.

## Research Categories

### 1. Architecture Pattern Research

**Quality Criteria:**
- Proven in production at similar scale
- Active community/support (>1000 stars, recent commits)
- Clear documentation and examples
- Compatible with identified constraints
- Performance benchmarks available

**Minimum Viable Research:**
- 3 viable patterns identified
- Each pattern used in 2+ production cases
- Pros/cons documented with evidence
- Decision matrix completed

**Stop Conditions:**
- Found 3 patterns meeting all criteria
- Spent maximum 60 minutes
- Identified clear winner with no close alternatives
- User has specific preference stated

### 2. Technology Stack Research

**Quality Criteria:**
- Ecosystem maturity (stable releases, not beta)
- Team familiarity score (0-10)
- Integration compatibility confirmed
- License compatibility verified
- Long-term support available

**Minimum Viable Research:**
- Primary technology options evaluated
- Dependencies and conflicts identified
- Migration paths considered
- Total cost of ownership estimated

**Stop Conditions:**
- Stack meets all requirements
- No critical blockers found
- Time box reached (45 minutes)
- User directive received

### 3. CI/CD Tool Research

**Quality Criteria:**
- Supports required deployment targets
- Pricing within budget constraints
- Integration with existing tools
- Security compliance features
- Automation capabilities

**Minimum Viable Research:**
- 3-5 options compared
- Feature matrix completed
- Cost analysis done
- Setup complexity evaluated

**Stop Conditions:**
- Clear best fit identified
- All must-have features covered
- 45 minutes elapsed
- Platform already mandated

### 4. Library/Framework Research

**Quality Criteria:**
- API stability (semantic versioning)
- Bundle size impact (<threshold)
- Performance metrics available
- Security audit history
- Maintenance activity (last 6 months)

**Minimum Viable Research:**
- Core functionality verified
- Alternatives considered
- Integration effort estimated
- Breaking change history reviewed

**Stop Conditions:**
- Functionality requirements met
- No security concerns
- 30 minutes per library
- Already in use in codebase

## Research Quality Scoring

### Scoring Matrix (per option)
```
Fitness Score (0-10):
- Meets requirements: 0-4 points
- Integration ease: 0-2 points  
- Team experience: 0-2 points
- Future-proofing: 0-2 points

Risk Score (0-10):
- Technical debt: 0-3 points
- Vendor lock-in: 0-2 points
- Skill gap: 0-2 points
- Maintenance burden: 0-3 points

Total Score = Fitness - Risk
```

### Minimum Acceptable Scores
- Total Score ≥ 3 for consideration
- Fitness Score ≥ 6 for primary options
- Risk Score ≤ 5 for acceptance

## Research Bounds and Constraints

### Time Bounds
- Architecture research: 60 minutes max
- Tool research: 45 minutes max
- Library research: 30 minutes per library
- Total research phase: 3 hours max

### Scope Bounds
- Depth: Sufficient for informed decision
- Breadth: Cover primary options only
- Detail: Implementation-ready understanding
- Documentation: Decision-support level

### Quality Gates
1. **Minimum Options**: At least 3 viable alternatives
2. **Comparison Depth**: Standardized evaluation criteria
3. **Evidence Quality**: Links to documentation, benchmarks
4. **Decision Readiness**: Clear recommendation possible

## Research Output Templates

### Option Summary Template
```markdown
## [Option Name]

### Overview
- Brief description
- Primary use case
- Maturity level

### Evaluation
- Fitness Score: X/10
- Risk Score: Y/10
- Total Score: Z

### Pros
- Specific advantage 1
- Specific advantage 2

### Cons
- Specific limitation 1
- Specific limitation 2

### Evidence
- [Link to documentation]
- [Link to case study]
- [Link to benchmark]

### Recommendation
- When to use
- When to avoid
```

### Decision Matrix Template
```markdown
| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Requirement Fit | 30% | 8/10 | 7/10 | 9/10 |
| Ease of Use | 20% | 9/10 | 6/10 | 7/10 |
| Performance | 20% | 7/10 | 9/10 | 8/10 |
| Maintenance | 15% | 8/10 | 7/10 | 6/10 |
| Cost | 15% | 6/10 | 8/10 | 9/10 |
| **Total** | | **7.6** | **7.3** | **7.9** |

**Recommendation**: Option C based on highest weighted score
```

## Subagent Instructions Template

### Research Assignment Format
```markdown
## Research Task: [Specific Area]

### Objective
Find and evaluate options for [specific need]

### Constraints
- Must support: [list requirements]
- Must integrate with: [existing tools]
- Budget limit: [if applicable]
- Time limit: [X minutes]

### Success Criteria
- Find 3-5 viable options
- Score each option using provided matrix
- Document evidence for scores
- Create decision matrix
- Make preliminary recommendation

### Output Location
Write findings to: `.spec/research/[area]-options.md`

### Stop When
- Found 3 options meeting criteria
- Time limit reached
- Clear winner identified
- No viable options exist (document why)
```

## Anti-Patterns to Avoid

1. **Analysis Paralysis**: Researching beyond "good enough"
2. **Perfection Seeking**: Looking for perfect solution
3. **Scope Creep**: Researching unrelated areas
4. **Depth Over Breadth**: Too much detail on one option
5. **Opinion Over Evidence**: Personal preference without data

## Quality Checkpoints

Before concluding research:
- [ ] Minimum option count met?
- [ ] All options scored objectively?
- [ ] Evidence documented?
- [ ] Time bounds respected?
- [ ] Decision matrix complete?
- [ ] Recommendation justified?
- [ ] Risks identified?
- [ ] Stop conditions evaluated?