# Agent Prompt Template - Build Complete Spec

Copy and customize this prompt for your agent:

```markdown
You will create a complete software specification for [PROJECT NAME] using a structured spec-building process.

## Project Brief
[2-3 paragraphs describing:
- Problem being solved
- Target users
- Key objectives
- Known constraints]

## Process to Follow

### Step 1: Setup (10 minutes)
Run these commands:
```bash
cd [WORKING_DIR]
python3 [SPEC_BUILDING_PATH]/automation/generate-spec-template.py "[PROJECT NAME]" -t standard
cd [project-folder]
```

### Step 2: Requirements (1 hour)
Create these files in order, filling all sections:
1. `requirements/outcome-definition.md` - Business outcomes, user outcomes, success metrics
2. `requirements/acceptance-scenarios.md` - 10+ concrete test scenarios 
3. `requirements/non-functional-requirements.md` - Performance, security, reliability

### Step 3: Build Spec (2 hours)
Create `spec/SPEC.md` with:
- Executive Summary (problem, solution, impact)
- 5+ Functional Requirements (FR-001 to FR-005) with acceptance criteria
- 4+ Non-Functional Requirements with specific metrics
- Architecture with diagram
- Technology stack with versions and justifications
- 5+ risks with mitigation strategies
- Timeline, budget, and team composition
- Quantified success metrics

NO PLACEHOLDERS - every [bracket] must be replaced with real content.

### Step 4: Validate Quality (30 minutes)
Run validation and improve until score is 90+:
```bash
python3 [SPEC_BUILDING_PATH]/automation/validate-all.py spec/SPEC.md
```

Review suggestions and update the spec. Repeat until:
- Structure validation: PASSED
- Quality score: 90+

### Step 5: Final Review (30 minutes)
Ensure the spec can answer:
- What exactly are we building?
- How do we know when it's done?
- What could go wrong?
- How long will it take?
- What resources do we need?

## Quality Rules
1. Be specific - use numbers, not adjectives
2. Every requirement needs acceptance criteria
3. Every decision needs justification
4. Test scenarios must be concrete
5. Risks must have mitigation plans

## Example Transformations
❌ "Fast performance" → ✅ "API response <200ms for 95th percentile"
❌ "User-friendly" → ✅ "New users complete onboarding in <5 minutes"
❌ "Scalable" → ✅ "Supports 10,000 concurrent users without degradation"

Begin with Step 1. Ask clarifying questions as needed.
```

## Quick Start Examples

### Example 1: E-commerce Analytics Platform
```markdown
You will create a complete software specification for "CustomerInsight Pro" using a structured spec-building process.

## Project Brief
CustomerInsight Pro is a B2B SaaS platform for e-commerce analytics. It integrates with Shopify/WooCommerce to analyze customer behavior and provide actionable insights through dashboards. 

Key objectives: Reduce churn by 20%, increase AOV by 15%, improve marketing ROI by 25%.

Constraints: $500K budget, 6-month timeline, GDPR compliant, team of 4 developers.

[Continue with process steps...]
```

### Example 2: Internal Tool
```markdown
You will create a complete software specification for "DevOps Dashboard" using a structured spec-building process.

## Project Brief
DevOps Dashboard is an internal tool to monitor our microservices infrastructure. It aggregates metrics from Kubernetes, Prometheus, and GitHub to provide a unified view of system health and deployment status.

Key objectives: Reduce incident response time by 50%, automate 80% of routine checks, provide real-time alerts.

Constraints: Must integrate with existing tools, 3-month timeline, 2 developers, on-premise deployment.

[Continue with process steps...]
```

### Example 3: Mobile App
```markdown
You will create a complete software specification for "FitTracker Pro" using a structured spec-building process.

## Project Brief  
FitTracker Pro is a mobile fitness app that uses AI to create personalized workout plans. It tracks exercises through phone sensors and provides real-time form feedback using computer vision.

Key objectives: 100K downloads in year 1, 4.5+ app store rating, 40% monthly active users.

Constraints: iOS first then Android, $200K budget, 4-month MVP timeline, HIPAA compliant.

[Continue with process steps...]
```

## Usage Tips

1. **Be Specific in the Brief**: The more context you provide upfront, the better the spec
2. **Let Agent Ask Questions**: Encourage clarification on ambiguous points
3. **Enforce Quality Gates**: Don't let the agent proceed until each phase meets standards
4. **Use the Tools**: The automation scripts catch issues humans miss
5. **Iterate on Low Scores**: If quality score is low, focus on the weakest dimension

## Monitoring Checklist
- [ ] Project structure created successfully
- [ ] All 3 requirements documents completed
- [ ] SPEC.md has all sections filled
- [ ] No [TBD] or [TODO] placeholders remain
- [ ] Quality score is 90+
- [ ] All validation checks pass

The agent should complete the entire process in 3-4 hours of focused work.