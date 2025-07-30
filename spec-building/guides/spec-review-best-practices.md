# Spec Review Best Practices

## Overview
Effective spec reviews catch problems early, align stakeholders, and ensure implementation success. This guide provides proven practices for conducting thorough spec reviews.

## Review Participants and Roles

### Core Review Team

**Product Owner** (Decision Maker)
- Validates business value
- Confirms priorities
- Approves trade-offs
- Signs off on scope

**Technical Lead** (Feasibility Checker)
- Assesses technical approach
- Identifies risks
- Estimates complexity
- Validates architecture

**Lead Developer** (Implementation Voice)
- Checks implementability
- Questions ambiguities
- Estimates effort
- Identifies dependencies

**QA Lead** (Quality Guardian)
- Ensures testability
- Identifies edge cases
- Validates acceptance criteria
- Plans test approach

**UX/UI Designer** (User Advocate)
- Reviews user flows
- Validates usability
- Checks accessibility
- Ensures consistency

### Extended Reviewers

**Security Expert** (Risk Assessor)
- When: Always for external-facing systems
- Focus: Auth, data protection, vulnerabilities

**DevOps Engineer** (Operations Voice)
- When: For production systems
- Focus: Deployment, monitoring, scaling

**Customer Representative** (Reality Check)
- When: For customer-facing features
- Focus: Actual user needs, workflow fit

**Legal/Compliance** (Regulatory Guard)
- When: Handling PII, financial, health data
- Focus: Regulatory requirements

## Review Process Phases

### Phase 1: Pre-Review Preparation (2-3 days before)

**Document Distribution**
```
Email template:
Subject: Spec Review - [Project Name] - [Date]

Team,

Please review the attached spec before our meeting on [date].

Focus areas:
- Product: Business value and priorities (Sections 1-2)
- Tech: Architecture and feasibility (Sections 4-5)
- QA: Requirements and testability (Section 3)
- UX: User journeys and interfaces (Section 3.1)

Questions to consider:
1. Is anything unclear or ambiguous?
2. What risks do you see?
3. Is the scope achievable?
4. What's missing?

Add comments directly in the document or bring to meeting.

Thanks,
[PM Name]
```

**Reviewer Checklist**
Each reviewer should:
- [ ] Read entire spec (not just your section)
- [ ] Note unclear/ambiguous items
- [ ] Identify risks in your domain
- [ ] Estimate effort for your parts
- [ ] List missing requirements
- [ ] Prepare specific questions

### Phase 2: Review Meeting (2-3 hours)

**Meeting Structure**

**1. Context Setting (10 min)**
- Problem we're solving
- Success metrics
- Timeline/budget constraints
- Key stakeholders

**2. Walkthrough (60 min)**
Walk through spec systematically:
- Executive summary
- Requirements (functional & non-functional)
- Architecture
- Risks
- Implementation approach

For each section:
- Author presents (5 min)
- Clarifying questions (5 min)
- Concerns and risks (5 min)

**3. Deep Dives (60 min)**
Focus on identified issues:
- Ambiguous requirements
- Technical challenges
- Resource constraints
- Missing elements

**4. Action Items (20 min)**
- List all changes needed
- Assign owners
- Set deadlines
- Schedule follow-up

**Meeting Rules**
- No implementation details (save for planning)
- Focus on WHAT, not HOW
- Document all assumptions
- Capture all decisions
- Park lengthy debates

### Phase 3: Post-Review Actions (2-3 days)

**Update Spec**
- Incorporate all feedback
- Clarify ambiguities
- Add missing requirements
- Update risks
- Document decisions

**Follow-up Reviews**
- Share updated spec
- Quick review by key stakeholders
- Final sign-off

## Review Focus Areas

### 1. Completeness Check

**Requirements Coverage**
- [ ] All user stories have acceptance criteria
- [ ] Edge cases identified
- [ ] Error scenarios defined
- [ ] Performance requirements specified
- [ ] Security requirements included

**Missing Elements Common List**
- Admin functionality
- Reporting/analytics
- Data migration
- Integration points
- Monitoring/alerting
- Backup/recovery

### 2. Clarity Check

**Ambiguity Hunters**
Look for weasel words:
- "Should" → "Must" or "May"
- "Fast" → Specific metrics
- "User-friendly" → Specific criteria
- "Secure" → Specific standards
- "Scalable" → Specific targets

**Example Transformation**
```
Vague: "The system should handle many users"
Clear: "The system must support 1,000 concurrent users with <2s page load"

Vague: "Provide good search functionality"  
Clear: "Search must return results in <200ms for 95% of queries, support filters, and handle typos"
```

### 3. Feasibility Check

**Technical Reality**
- Proposed solution possible?
- Technology choices appropriate?
- Skills available on team?
- Timeline realistic?
- Infrastructure adequate?

**Red Flags**
- Unproven technology
- Tight coupling everywhere
- No fallback options
- Perfection required
- Magic solutions

### 4. Testability Check

**QA Checklist**
- [ ] Each requirement measurable
- [ ] Success criteria defined
- [ ] Test data available/creatable
- [ ] Performance benchmarks set
- [ ] Automation possible

**Untestable Requirement Examples**
- "System should be intuitive" → User testing metrics
- "Algorithm should be optimal" → Specific performance targets
- "UI should be attractive" → Design system compliance

### 5. Risk Assessment

**Risk Categories to Review**

**Technical Risks**
- New technology
- Complex integrations
- Performance requirements
- Scalability needs

**Business Risks**
- Market changes
- Competitor moves
- Regulatory changes
- User adoption

**Project Risks**
- Timeline aggressive
- Budget constraints
- Resource availability
- Dependencies

**Risk Response Template**
```
Risk: [Description]
Probability: [Low/Medium/High]
Impact: [Low/Medium/High]
Mitigation: [Specific actions]
Contingency: [If risk occurs]
Owner: [Who monitors]
```

## Review Techniques

### 1. Scenario Walkthroughs

**Technique**: Act out user scenarios
**Value**: Finds gaps and ambiguities

Example:
"OK, I'm a new user. I go to the site and... wait, how do I register? The spec says 'users can register' but doesn't describe the process."

### 2. Edge Case Brainstorming

**Technique**: "What if..." exercises
**Value**: Identifies missing requirements

Examples:
- What if network fails mid-transaction?
- What if user enters 1GB of text?
- What if 10,000 users hit submit simultaneously?

### 3. Dependency Mapping

**Technique**: Draw connection diagram
**Value**: Identifies hidden complexity

```
Login Feature
├── Depends on: User Database
├── Depends on: Email Service  
├── Depends on: Session Storage
└── Impacts: All authenticated features
```

### 4. Estimation Poker

**Technique**: Blind estimation reveals misunderstandings
**Value**: Surfaces hidden complexity

If estimates vary wildly (2 hours vs 2 weeks), dig into why.

### 5. Red Team Review

**Technique**: Adversarial review
**Value**: Finds security/abuse cases

"How would I break this?"
"How would I abuse this?"
"What would a hacker try?"

## Common Review Pitfalls

### 🚫 The Rubber Stamp
**Problem**: Review meeting is just a formality
**Signs**: 
- No questions asked
- Quick approval
- "Looks good to me"

**Fix**: 
- Assign specific sections to reviewers
- Require written feedback
- Use checklist

### 🚫 The Bike Shed
**Problem**: Debating trivial details, missing big issues
**Signs**:
- 30 minutes on button color
- Ignoring architecture flaws
- Personal preferences dominate

**Fix**:
- Time box discussions
- Focus on user/business impact
- Park style debates

### 🚫 The Design Meeting
**Problem**: Trying to solve problems in review
**Signs**:
- Whiteboarding solutions
- Implementation debates
- "How" dominates "what"

**Fix**:
- Clarify review purpose
- Note problems, don't solve
- Schedule separate design sessions

### 🚫 The Echo Chamber
**Problem**: Only positive feedback
**Signs**:
- No criticism
- Group think
- Avoiding conflict

**Fix**:
- Assign devil's advocate
- Anonymous feedback option
- Reward finding issues

## Review Outcomes

### Possible Decisions

**1. Approved**
- All major concerns addressed
- Minor changes only
- Can proceed to planning

**2. Conditional Approval**  
- Specific changes required
- Re-review not needed
- Proceed after updates

**3. Major Revision Needed**
- Significant gaps/issues
- Requires re-review
- Do not proceed yet

**4. Reject and Restart**
- Fundamental flaws
- Wrong approach
- Back to discovery

### Documentation Template

```markdown
# Spec Review Summary - [Project Name]

**Date**: [Date]
**Participants**: [Names and roles]
**Decision**: [Approved/Conditional/Revision/Reject]

## Key Findings

### Strengths
- [What's good about the spec]

### Concerns Raised
1. [Concern]: [Who raised] - [Resolution]
2. [Concern]: [Who raised] - [Resolution]

### Action Items
- [ ] [Action] - Owner: [Name] - Due: [Date]
- [ ] [Action] - Owner: [Name] - Due: [Date]

### Risks Identified
- [Risk]: [Mitigation plan]

### Estimates
- Development: [X weeks]
- Testing: [X weeks]
- Total: [X weeks]

### Next Steps
1. [Update spec with feedback]
2. [Schedule planning session]
3. [Begin sprint 0]

### Sign-offs
- Product: ✓ [Name] [Date]
- Tech: ✓ [Name] [Date]  
- QA: ✓ [Name] [Date]
- UX: ✓ [Name] [Date]
```

## Continuous Improvement

### Review Retrospectives

After project completion, assess review effectiveness:

**Questions to Ask**
1. What did reviews catch early?
2. What problems weren't caught?
3. Was review effort appropriate?
4. How could process improve?

**Metrics to Track**
- Issues found in review vs development
- Time spent in review vs rework avoided
- Spec changes after review
- Post-implementation spec accuracy

### Review Efficiency Tips

**Before Meeting**
- Use collaborative docs for async feedback
- Share specific questions in advance
- Provide context for new reviewers
- Set clear review objectives

**During Meeting**
- Start with biggest risks
- Time box each section
- Capture decisions immediately
- Assign action items with dates

**After Meeting**
- Send summary within 24 hours
- Update spec within 48 hours
- Get sign-offs electronically
- Archive review artifacts

## Quick Reference

### Review Checklist
- [ ] Right people invited
- [ ] Spec distributed early
- [ ] Meeting agenda clear
- [ ] Note taker assigned
- [ ] Decision criteria defined
- [ ] Follow-up scheduled

### Red Flags That Must Be Addressed
- Undefined acceptance criteria
- Missing error handling
- No performance targets
- Ambiguous requirements
- Unrealistic timeline
- No testing approach
- Missing security requirements

### Green Flags of a Good Spec
- Clear success metrics
- Concrete examples
- Testable requirements
- Realistic constraints
- Identified risks
- Defined trade-offs
- Stakeholder alignment

Remember: The goal isn't a perfect spec, but one that's good enough to build the right thing efficiently. Reviews are an investment that pays off in reduced rework and faster delivery.