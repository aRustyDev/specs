# Spec Quality Scoring Rubric

## Overview
This rubric provides objective criteria for evaluating specification quality across four key dimensions. Each dimension is worth 25 points for a total possible score of 100.

## Scoring Instructions
1. Review each criterion within a dimension
2. Assign points based on evidence, not opinion
3. Document specific examples for scores <5
4. Sum dimension scores for total quality score

## Example Scoring - TaskMaster Project
The TaskMaster spec received an overall score of 92/100:
- Completeness: 25/25 (all sections present and thorough)
- Clarity: 23/25 (minor deductions for missing diagrams)
- Measurability: 24/25 (baseline metrics could be more detailed)
- Feasibility: 20/20 (realistic scope and approach)

## Dimension 1: Completeness (25 points)

### Core Sections (10 points)
- **10 points**: All required sections present with substantial content
- **7-9 points**: All sections present, some lack depth
- **4-6 points**: 1-2 sections missing or placeholder content
- **1-3 points**: Multiple sections missing
- **0 points**: Major sections empty/missing

Required sections checklist:
- [ ] Executive Summary
- [ ] Outcomes (Business, User, Technical, Quality)
- [ ] Requirements (Functional and Non-functional)
- [ ] Architecture Design
- [ ] Component Specifications
- [ ] Interface Definitions
- [ ] Risk Analysis
- [ ] Success Metrics
- [ ] Implementation Approach

### Requirements Coverage (8 points)
- **8 points**: >95% of identified scope covered
- **6-7 points**: 85-94% coverage
- **4-5 points**: 70-84% coverage
- **2-3 points**: 50-69% coverage
- **0-1 points**: <50% coverage

Coverage includes:
- All user personas addressed
- All user journeys documented
- Edge cases identified
- Error scenarios defined
- Integration points specified

### Cross-References (4 points)
- **4 points**: All references valid and bidirectional
- **3 points**: >90% references working
- **2 points**: 75-90% references working
- **1 point**: 50-74% references working
- **0 points**: <50% references working

### Placeholder Check (3 points)
- **3 points**: Zero TODOs, TBDs, or [PLACEHOLDER]
- **2 points**: 1-3 placeholders in non-critical areas
- **1 point**: 4-6 placeholders or 1-2 in critical areas
- **0 points**: >6 placeholders or >2 in critical areas

**Completeness Score: ___/25**

## Dimension 2: Clarity (25 points)

### Language Precision (8 points)
- **8 points**: Crystal clear, zero ambiguity
- **6-7 points**: Mostly clear, minor ambiguities
- **4-5 points**: Some sections unclear
- **2-3 points**: Frequent ambiguity
- **0-1 points**: Pervasive unclear language

Clarity indicators:
- Specific vs vague terms
- Quantified vs qualitative
- Active vs passive voice
- Defined vs assumed knowledge

### Consistency (7 points)
- **7 points**: Perfect terminology consistency
- **5-6 points**: Minor inconsistencies
- **3-4 points**: Notable inconsistencies
- **1-2 points**: Frequent inconsistencies
- **0 points**: No consistency

Check for:
- Term definitions
- Naming conventions
- Format standards
- Reference styles

### Structure & Flow (6 points)
- **6 points**: Logical flow, easy navigation
- **4-5 points**: Good structure, minor issues
- **2-3 points**: Adequate structure
- **1 point**: Poor organization
- **0 points**: No clear structure

### Visual Aids (4 points)
- **4 points**: Excellent diagrams where needed
- **3 points**: Good diagrams, could use more
- **2 points**: Some diagrams, need improvement
- **1 point**: Few/poor diagrams
- **0 points**: No visual aids where needed

**Clarity Score: ___/25**

## Dimension 3: Implementability (25 points)

### Technical Feasibility (10 points)
- **10 points**: All solutions proven feasible
- **7-9 points**: Mostly feasible, minor concerns
- **4-6 points**: Some feasibility questions
- **1-3 points**: Major feasibility issues
- **0 points**: Not implementable as specified

Assess:
- Technology maturity
- Team capabilities
- Infrastructure requirements
- Integration complexity

### Resource Realism (6 points)
- **6 points**: Resources well-matched to scope
- **4-5 points**: Mostly realistic
- **2-3 points**: Some unrealistic expectations
- **1 point**: Major resource gaps
- **0 points**: Completely unrealistic

Consider:
- Time estimates
- Team size/skills
- Budget constraints
- External dependencies

### Dependency Management (5 points)
- **5 points**: All dependencies identified/managed
- **4 points**: Most dependencies clear
- **2-3 points**: Some dependencies missed
- **1 point**: Major dependencies unclear
- **0 points**: Dependencies ignored

### Risk Mitigation (4 points)
- **4 points**: All risks have mitigations
- **3 points**: Most risks addressed
- **2 points**: Some risks addressed
- **1 point**: Few risks addressed
- **0 points**: No risk mitigation

**Implementability Score: ___/25**

## Dimension 4: Testability (25 points)

### Success Criteria (10 points)
- **10 points**: All measurable and specific
- **7-9 points**: Mostly measurable
- **4-6 points**: Mix of measurable/vague
- **1-3 points**: Mostly vague
- **0 points**: No measurable criteria

Examples of good criteria:
- "Response time <200ms for 95% of requests"
- "Support 10,000 concurrent users"
- "99.9% uptime excluding maintenance"

### Acceptance Scenarios (8 points)
- **8 points**: Comprehensive scenarios with data
- **6-7 points**: Good coverage, some gaps
- **4-5 points**: Basic scenarios only
- **2-3 points**: Few scenarios
- **0-1 points**: No/minimal scenarios

Scenario quality:
- Specific test data
- Expected outcomes
- Edge cases
- Error conditions

### Validation Methods (4 points)
- **4 points**: Clear validation for all requirements
- **3 points**: Most requirements validatable
- **2 points**: Some validation methods
- **1 point**: Few validation methods
- **0 points**: No validation approach

### Quality Metrics (3 points)
- **3 points**: Comprehensive metrics defined
- **2 points**: Good metrics coverage
- **1 point**: Basic metrics only
- **0 points**: No quality metrics

**Testability Score: ___/25**

## Total Quality Score Calculation

| Dimension | Score | Weight |
|-----------|-------|--------|
| Completeness | ___/25 | 25% |
| Clarity | ___/25 | 25% |
| Implementability | ___/25 | 25% |
| Testability | ___/25 | 25% |
| **TOTAL** | **___/100** | **100%** |

## Quality Thresholds

- **95-100**: Exceptional - Ready for immediate use
- **90-94**: High Quality - Standard approval
- **85-89**: Good - Conditional approval with documented gaps
- **80-84**: Acceptable - Extended approval with controls
- **75-79**: Marginal - Significant improvements required
- **<75**: Unacceptable - Major revision needed

## Score Interpretation Guide

### Exceptional (95-100)
- Spec can serve as reference for other projects
- Minimal risk of implementation issues
- Clear enough for outsourced development

### High Quality (90-94)
- Ready for roadmap creation
- Low risk of misunderstandings
- Standard approval process

### Good (85-89)
- Conditional approval with documented gaps
- Requires mitigation plan
- Some clarifications needed during implementation

### Acceptable (80-84)
- Extended approval with controls
- Plan for clarification sessions
- Higher risk requiring active management

### Marginal (75-79)
- Requires improvement before proceeding
- High risk of implementation problems
- Likely to cause delays and rework

### Unacceptable (<75)
- Do not proceed to implementation
- Major gaps must be addressed
- High probability of project failure

## Documentation Requirements

For any score <5 in a category, document:
1. Specific examples of deficiencies
2. Impact on implementation
3. Recommended improvements
4. Effort estimate to fix

## Review Frequency

- Initial assessment: After spec completion
- Iteration assessment: After each improvement cycle
- Final assessment: Before roadmap creation
- Maintenance assessment: Quarterly for living specs

## Detailed Scoring Example - TaskMaster Project

### Dimension 1: Completeness (25/25)
- **Core Sections (10/10)**: All sections present with rich detail
  - ✓ Executive summary with clear business case
  - ✓ Comprehensive outcomes across all dimensions
  - ✓ 6 functional + 5 non-functional requirements
  - ✓ Detailed architecture with diagram
  - ✓ Complete risk analysis with mitigations
- **Requirements Coverage (8/8)**: 100% coverage
  - ✓ 3 detailed personas (Sarah, Alex, Maria)
  - ✓ 8 acceptance scenarios with test data
  - ✓ Edge cases and error scenarios included
- **Cross-References (4/4)**: Perfect alignment
  - ✓ Requirements → Architecture mapping
  - ✓ Personas → Requirements traceability
- **Placeholder Check (3/3)**: Zero placeholders found

### Dimension 2: Clarity (23/25)
- **Language Precision (8/8)**: Exceptionally clear
  - Quantified metrics ($30k/month savings)
  - Specific technical choices with rationale
  - Active voice throughout
- **Consistency (7/7)**: Perfect terminology
  - Consistent use of "TaskMaster"
  - Standard format for all requirements
- **Structure & Flow (6/6)**: Logical progression
  - Business → User → Technical flow
  - Easy navigation with clear headers
- **Visual Aids (2/4)**: Minor gap identified
  - ✓ Good architecture diagram
  - ✗ Missing user journey visualization (-1)
  - ✗ Could use sequence diagram for real-time (-1)

### Dimension 3: Implementability (20/20)
- **Technical Feasibility (10/10)**: Highly feasible
  - Proven tech stack (React, Node.js, PostgreSQL)
  - Team has required skills
  - Realistic performance targets
- **Resource Realism (6/6)**: Well-matched
  - 4-month timeline with buffers
  - 5-developer team appropriate
  - $250k budget realistic
- **Dependency Management (5/5)**: Clear dependencies
  - External: Slack API, AWS services
  - Internal: Phased approach manages complexity
- **Risk Mitigation (4/4)**: All risks addressed
  - 5 risks with probability and mitigation
  - Realistic mitigation strategies

### Dimension 4: Testability (24/25)
- **Measurable Requirements (10/10)**: All quantified
  - Response times: <2s page load
  - Uptime: 99.9%
  - User adoption: 90% in 30 days
- **Test Scenarios (8/8)**: Comprehensive
  - 8 detailed acceptance scenarios
  - Happy path + edge cases + errors
  - Performance scenarios included
- **Acceptance Criteria (3/3)**: Clear pass/fail
  - Each requirement has specific criteria
  - Quantified thresholds
- **Baseline Data (2/3)**: Minor gap
  - ✓ Current costs quantified
  - ✗ Current tool performance not detailed (-1)
- **Quality Metrics (3/3)**: Well-defined
  - Test coverage targets (>85%)
  - Performance benchmarks
  - Security requirements

### Final Score: 92/100 (High Quality)

**Interpretation**: The TaskMaster spec is ready for roadmap creation with minor enhancements recommended. The high score indicates low risk of implementation issues and clear understanding among all stakeholders.

**Recommendations**:
1. Add user journey visualization (15 minutes effort)
2. Include sequence diagram for WebSocket flow (30 minutes)
3. Gather baseline performance metrics from current tools (2 hours)

**Risk Assessment**: Very low risk proceeding to implementation planning.