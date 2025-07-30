# Anti-Sycophancy Challenge Framework

## Purpose
This framework ensures we challenge assumptions, identify blind spots, and build robust specifications based on evidence rather than agreement.

## Red Team Questions by Phase

### Phase 1: Discovery Challenges

**Challenge the Problem**
- Is this the real problem or just a symptom?
- Who says this is a problem? What's their bias?
- What happens if we do nothing?
- Are we solving yesterday's problem?
- What problem should we be solving instead?

**Challenge the Scope**
- What are we assuming is in scope that shouldn't be?
- What are we excluding that will come back to bite us?
- Where will scope creep most likely occur?
- What dependencies are we pretending don't exist?

**Challenge the Users**
- Are these the real users or who we wish they were?
- What user behaviors are we assuming incorrectly?
- Which user group will resist this change? Why?
- What users are we ignoring?

### Phase 2: Analysis Challenges

**Challenge the Requirements**
- Which requirements contradict each other?
- What requirements are actually solutions in disguise?
- Which requirements will be ignored in practice?
- What's missing that no one wants to talk about?
- Which requirement will kill the project if enforced?

**Challenge the Priorities**
- Why is everything "high priority"?
- What's the real top priority when pushed?
- Which "must-have" is actually negotiable?
- What low priority item will cause failure if ignored?

**Challenge the Assumptions**
- List every assumption made. Now challenge each:
  - What evidence supports this?
  - When has this been false before?
  - What would break if this were false?
  - How can we test this assumption?

### Phase 3: Research Challenges

**Challenge the Research**
- What research are we avoiding because it's hard?
- Which sources have inherent bias?
- What conflicting research are we ignoring?
- Where are we cherry-picking data?
- What would a competitor's research show?

**Challenge the Options**
- What options are we not considering? Why?
- Which option are we biased toward? Why?
- What hybrid options exist?
- What would happen with the "crazy" option?

**Challenge the Recommendations**
- What recommends option A: evidence or preference?
- What are the hidden costs of each option?
- Which option fails most gracefully?
- What option would we choose if starting over?

### Phase 4: Design Challenges

**Challenge the Architecture**
- Where is this unnecessarily complex?
- What will break first under load?
- Which component has too much responsibility?
- Where are we over-engineering? Under-engineering?
- What can't be changed later?

**Challenge the Technology**
- Are we choosing tech we like or tech that fits?
- What tech debt are we creating?
- Where are we betting on unproven technology?
- What happens when [popular tech] isn't supported?

**Challenge the Integrations**
- Which integration will fail most often?
- What happens when the API changes?
- Where are we too tightly coupled?
- Which dependency will constrain us most?

### Phase 5: Validation Challenges

**Challenge the Validation**
- What scenarios are we afraid to test?
- Which stakeholder viewpoint are we avoiding?
- What edge cases are we calling "unlikely"?
- Where are we being optimistic about performance?

**Challenge the Risks**
- What risks are we not documenting? Why?
- Which "low probability" risk would be catastrophic?
- What risk mitigation is actually wishful thinking?
- What new risks does our solution create?

## Evidence Requirements

### For Every Major Decision
1. **Primary Evidence**: Direct data/research
2. **Counter Evidence**: What disagrees?
3. **Null Hypothesis**: What if we're wrong?
4. **Alternative Explanation**: Other interpretations?
5. **Confidence Level**: How sure are we? (%)

### Evidence Quality Checklist
- [ ] Source identified and credible
- [ ] Recent enough to be relevant
- [ ] Applicable to our context
- [ ] Independently verifiable
- [ ] Conflicts documented

## Devil's Advocate Protocol

### Rotating Role
- Assign different person per phase
- Must argue against prevailing view
- Document all counterarguments
- No dismissing without evidence

### Structured Opposition
For each major decision:
1. **Thesis**: The proposed decision
2. **Antithesis**: Why it's wrong
3. **Evidence**: Supporting the opposition
4. **Synthesis**: What we learned

## Assumption Hunting

### Assumption Log Template
| Assumption | Type | Risk if Wrong | How to Validate | Status |
|------------|------|---------------|-----------------|--------|
| Users will adopt feature X | User behavior | High - core value prop | User testing | Unvalidated |
| System can handle 10k users | Technical | Medium - need rearch | Load testing | Partially validated |
| Budget includes all costs | Business | High - project viability | Detailed estimate | Unvalidated |

### Assumption Categories
- **User Behavior**: What users will/won't do
- **Technical**: What's technically possible
- **Business**: Market/organization assumptions  
- **Resource**: Time/money/people availability
- **External**: Third-party dependencies

## Blind Spot Detection

### The Pre-Mortem Exercise
"It's 6 months later and the project failed spectacularly. What happened?"

Common blind spots:
- Political/organizational resistance
- Technical complexity underestimation
- User adoption challenges
- Integration nightmares
- Performance degradation
- Security vulnerabilities
- Compliance surprises

### Outside Perspective
Questions from different viewpoints:
- **New Employee**: What's confusing?
- **Competitor**: How would they attack this?
- **Regulator**: What concerns them?
- **Hacker**: How would they exploit this?
- **Accountant**: Where's the hidden cost?
- **Lawyer**: What's the liability?

## Measurement Over Opinion

### Convert Opinions to Hypotheses
| Opinion | Hypothesis | Metric | Test Method |
|---------|------------|--------|-------------|
| "Users want feature X" | >70% of users will use X weekly | Usage analytics | Beta test |
| "This will be fast" | p95 latency <200ms | Response time | Load test |
| "It's secure enough" | Passes OWASP Top 10 | Vulnerability count | Security scan |

### Falsifiable Claims
Every major claim must be:
- Specific enough to test
- Measurable objectively
- Time-bound for validation
- Documented with criteria

## Challenge Integration Points

### During Requirements
- "Prove this is needed with data"
- "What's the simplest solution?"
- "Who specifically asked for this?"

### During Design
- "What breaks this design?"
- "Where's the bottleneck?"
- "How does this fail?"

### During Validation
- "What aren't we testing?"
- "Which metric could be gamed?"
- "What would production reveal?"

## Success Metrics for Anti-Sycophancy

We're successfully avoiding sycophancy when:
- [ ] Uncomfortable questions are asked and answered
- [ ] Multiple viewpoints documented for each decision
- [ ] Evidence contradicts initial assumptions
- [ ] Design changes based on challenges
- [ ] Risks discovered that weren't initially considered
- [ ] Assumptions explicitly tested, not accepted
- [ ] Conflicting data preserved, not hidden
- [ ] "I don't know" is an acceptable answer

## The Final Challenge

Before approving any spec section, ask:
1. What would a harsh critic say?
2. What are we afraid to admit?
3. What would we do differently with unlimited resources?
4. What would we do with half the resources?
5. What decision will we most regret?
6. Are we solving the right problem the right way?