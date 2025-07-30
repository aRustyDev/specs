# Spec Anti-Patterns Guide

## Overview
This guide identifies common mistakes in spec writing that lead to project failures, delays, or significant rework. Learn to recognize and avoid these patterns.

## Anti-Pattern Categories

### 1. Scope Anti-Patterns

#### 🚫 The Kitchen Sink
**Pattern**: Including every possible feature in v1
**Example**: 
```
"The system shall support email, SMS, push notifications, in-app messaging, 
carrier pigeons, smoke signals, and telepathic communication."
```
**Why it fails**: 
- Impossible to deliver on time
- Lacks focus on core value
- Creates complexity explosion

**Better approach**:
```
"Phase 1: Email notifications (MVP)
Phase 2: SMS for critical alerts  
Phase 3: Push notifications
Future: Evaluate additional channels based on user feedback"
```

#### 🚫 The Shape-Shifter
**Pattern**: Scope that changes fundamentally during development
**Signs**:
- "Small" additions that change architecture
- Pivoting target audience mid-project
- "While we're at it" syndrome

**Prevention**:
- Clear change control process
- Document what's explicitly OUT of scope
- Regular stakeholder alignment sessions

#### 🚫 The Iceberg
**Pattern**: Visible requirements hide massive complexity
**Example**: "Users can log in" (but needs SSO, MFA, social login, password policies, account recovery, admin override, audit trail...)

**Better approach**:
- Expand each requirement fully
- Create acceptance scenarios
- Review with implementation team

### 2. Requirements Anti-Patterns

#### 🚫 The Mind Reader
**Pattern**: Assuming shared understanding without explicit definition
**Examples**:
- "The system should be fast"
- "Use modern UI design"
- "Implement best practices"

**Fix**: Define everything measurably
- "Response time <200ms for 95th percentile"
- "Follow Material Design 3.0 guidelines"
- "Implement OWASP Top 10 security practices"

#### 🚫 The Unicorn
**Pattern**: Requirements that are technically impossible or contradictory
**Examples**:
- "100% uptime with zero infrastructure cost"
- "Real-time sync with offline-first architecture"
- "Infinitely scalable on a Raspberry Pi"

**Reality check questions**:
- Has anyone done this before?
- What are the physics/math limits?
- What are we trading off?

#### 🚫 The Lawyer
**Pattern**: Requirements written in legal/contract language
**Example**: 
```
"The party of the first part (hereinafter referred to as 'System') shall, 
pursuant to the requirements set forth in Appendix J, subsection 3.2.1, 
provide functionality whereby..."
```

**Better**: Write in plain English
- Use active voice
- Short sentences
- Examples and scenarios

### 3. Technical Anti-Patterns

#### 🚫 The Technology Parade
**Pattern**: Choosing tech because it's trendy, not because it fits
**Red flags**:
- "Let's use [latest framework] because it's hot"
- Technology shopping list without justification
- Resume-driven development

**Better approach**:
```
"Chose React because:
- Team has 3+ years experience
- Large ecosystem for our use cases
- Proven at our scale
- Strong community support"
```

#### 🚫 The Premature Optimizer
**Pattern**: Optimizing for problems you don't have yet
**Examples**:
- Microservices for 10 users
- Global CDN for local business
- Kubernetes for 2 containers

**Start simple principle**:
1. Build monolith first
2. Measure actual bottlenecks
3. Optimize what matters
4. Document why you optimized

#### 🚫 The Golden Hammer
**Pattern**: Using one technology/pattern for everything
**Example**: "We'll use blockchain for user authentication, file storage, and UI rendering"

**Diverse toolkit approach**:
- Right tool for each job
- Justify each technology choice
- Consider maintenance burden

### 4. Process Anti-Patterns

#### 🚫 The Waterfall in Disguise
**Pattern**: Claiming agile but requiring complete specs upfront
**Signs**:
- 200-page "agile" requirements document
- No customer feedback until end
- "Sprint 1: Complete all design"

**True agile approach**:
- Start with MVP spec
- Build, measure, learn
- Evolve spec with project

#### 🚫 The Committee Design
**Pattern**: Too many stakeholders creating franken-specs
**Symptoms**:
- Conflicting requirements
- Every department's pet feature included
- No clear vision

**Fix with**:
- Single product owner
- Clear decision rights
- Documented trade-offs

#### 🚫 The Set and Forget
**Pattern**: Spec created then never updated
**Problems**:
- Spec diverges from reality
- Decisions not documented
- New team members confused

**Living spec approach**:
- Version control everything
- Update with major decisions
- Regular spec/reality alignment

### 5. Quality Anti-Patterns

#### 🚫 The Happy Path Highway
**Pattern**: Only specifying success scenarios
**Missing**:
- Error handling
- Edge cases  
- Performance degradation
- Security failures

**Complete with**:
```
For each feature:
- Happy path (60%)
- Error cases (20%)
- Edge cases (15%)
- Performance limits (5%)
```

#### 🚫 The Perfection Paralysis
**Pattern**: Requirements for perfection that prevent shipping
**Examples**:
- "Zero bugs" (impossible)
- "Handles every possible input"
- "Works on all devices ever made"

**Pragmatic quality**:
- Define acceptable error rates
- Specify supported platforms
- Plan for graceful degradation

#### 🚫 The Test Later
**Pattern**: No testing requirements in spec
**Problems**:
- Untestable requirements
- No budget for testing
- Quality afterthought

**Embed testing**:
- Acceptance criteria for each requirement
- Test scenarios in spec
- Testing effort in estimates

### 6. Communication Anti-Patterns

#### 🚫 The Tower of Babel
**Pattern**: Technical jargon overwhelming business stakeholders
**Example**: "The system will implement a hexagonal architecture with CQRS and event sourcing using DDD tactical patterns..."

**Bilingual approach**:
- Executive summary in business terms
- Technical details in appendix
- Glossary for terms

#### 🚫 The Assumption Avalanche
**Pattern**: Undocumented assumptions everywhere
**Hidden bombs**:
- "Obviously, users have smartphones"
- "Of course we'll have admin access"
- "Everyone knows SQL"

**Document all assumptions**:
```
## Assumptions
- Users: Have modern browsers (Chrome/Firefox/Safari last 2 versions)
- Infrastructure: AWS is approved vendor
- Team: Familiar with JavaScript
- Timeline: No major holidays in dev period
```

#### 🚫 The Silent Treatment
**Pattern**: No mechanism for clarification during implementation
**Results in**:
- Developers guessing
- Building wrong thing
- Expensive rework

**Communication plan**:
- Weekly stakeholder sync
- Slack channel for questions
- Decision log maintained

## Real-World Horror Stories

### Case 1: The Infinity Spec
**Project**: Enterprise Resource Planning
**Anti-pattern**: Kitchen Sink + Committee Design
**Result**: 
- 18-month spec phase
- 400+ requirements
- Project cancelled before development
**Lesson**: Start small, grow incrementally

### Case 2: The Moving Target
**Project**: Mobile Social App
**Anti-pattern**: Shape-Shifter + Mind Reader
**Result**:
- 6 major pivots
- 3x budget overrun
- Team burnout and turnover
**Lesson**: Lock down MVP, defer changes

### Case 3: The Perfect Platform
**Project**: Internal Tools Portal  
**Anti-pattern**: Premature Optimizer + Technology Parade
**Result**:
- Microservices for 50 users
- 12 different technologies
- Unmaintainable after team left
**Lesson**: Boring technology, exciting features

## Anti-Pattern Checklist

Before finalizing your spec, check for these smells:

### 🚩 Red Flags
- [ ] Requirements with "all", "every", "any", "never"
- [ ] Technology choices without justification
- [ ] No error scenarios described
- [ ] Missing non-functional requirements
- [ ] No clear prioritization (everything "critical")
- [ ] Assumptions not documented
- [ ] No validation with dev team
- [ ] Success metrics undefined
- [ ] No budget/timeline reality check

### 🤔 Warning Signs
- [ ] Spec longer than 50 pages
- [ ] Multiple conflicting stakeholders
- [ ] Bleeding-edge technology everywhere
- [ ] No mention of testing
- [ ] Perfect uptime/performance requirements
- [ ] No change process defined
- [ ] Requirements still growing
- [ ] Team skills not considered

## Recovery Strategies

If you recognize anti-patterns in existing specs:

### 1. Scope Surgery
- List all features
- Force rank by business value
- Draw line at realistic capacity
- Move rest to "Future" section

### 2. Requirement Rehab
- Add metrics to vague requirements
- Create scenarios for unclear items
- Validate technical feasibility
- Get sign-off on interpretations

### 3. Technical Detox
- List all technology choices
- Document why each was chosen
- Identify resume-driven choices
- Replace with boring alternatives

### 4. Process Patches
- Assign single decision maker
- Create lightweight change process
- Schedule regular reviews
- Keep spec updated

## Prevention Guidelines

### Start Right
1. **Define the problem** before solutions
2. **Start with outcomes**, not features  
3. **Validate feasibility** early
4. **Include whole team** in reviews

### Stay Focused
1. **MVP discipline**: What's truly minimum?
2. **Say no**: Document out-of-scope
3. **Prioritize ruthlessly**: Not everything is critical
4. **Time box spec phase**: Don't over-engineer

### Finish Strong
1. **Test the spec**: Can team implement from it?
2. **Reality check**: With budget and timeline
3. **Get commitment**: From all stakeholders
4. **Plan for change**: It will happen

## Remember

> "The best spec is not the most complete one, but the one that gets the right thing built efficiently."

Anti-patterns often come from good intentions:
- Wanting to please everyone
- Trying to prevent all problems
- Pursuing technical excellence
- Avoiding difficult decisions

Recognize these impulses and channel them productively:
- Please users with focused solutions
- Prevent likely problems, accept rare ones
- Pursue excellence in what matters
- Make decisions with clear rationale

Your spec is a communication tool, not a contract. Make it clear, realistic, and actionable.