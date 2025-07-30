# Agent Implementation Guide - From Nothing to Complete Spec

## Overview

This guide shows how to use an AI agent to implement a complete specification from scratch using the spec-building process. The agent will follow the structured phases and use the automation tools to ensure quality.

## Prerequisites

Before starting, ensure:
1. The spec-building directory is available at `/path/to/spec-building/`
2. Python 3.6+ is installed
3. The agent has file system access to create and modify files

## Complete Agent Prompt Template

Use this prompt to instruct an agent to build a spec from scratch:

```markdown
You are tasked with creating a complete software specification for [PROJECT NAME]. You will follow a structured process using the spec-building framework located at [SPEC_BUILDING_PATH].

## Project Context
[Provide 2-3 paragraphs about:
- What problem this project solves
- Who the users are
- Key business objectives
- Any known constraints or requirements]

## Your Task

Follow these phases to create a complete, high-quality specification:

### Phase 1: Setup and Requirements Gathering (2-3 hours)

1. **Create Project Structure**
   ```bash
   cd [WORKING_DIRECTORY]
   python3 [SPEC_BUILDING_PATH]/automation/generate-spec-template.py "[PROJECT NAME]" -t standard
   cd [project-name]
   ```

2. **Requirements Discovery**
   - Read and understand the greenfield spec process: `[SPEC_BUILDING_PATH]/01-spec-creation/01-greenfield-spec-process.md`
   - Create these requirements documents in order:
     a. `requirements/outcome-definition.md` - Define what success looks like
     b. `requirements/acceptance-scenarios.md` - Create 10+ test scenarios
     c. `requirements/non-functional-requirements.md` - Performance, security, etc.

3. **Stakeholder Analysis**
   Ask me these questions to understand stakeholders:
   - Who are the primary users and what are their roles?
   - Who has approval authority for features?
   - What are the communication preferences?
   - Are there any compliance or regulatory stakeholders?

### Phase 2: Spec Development (3-4 hours)

1. **Initial Spec Creation**
   Using the requirements as input, create `spec/SPEC.md` following the template structure:
   - Fill ALL sections with specific, measurable content
   - No placeholders like [TBD] or [TODO]
   - Include at least 5 functional requirements (FR-001 through FR-005)
   - Include at least 4 non-functional requirements (NFR-001 through NFR-004)
   - Add quantified metrics (response times, user counts, etc.)

2. **Architecture Design**
   - Create a high-level architecture section with:
     - ASCII or mermaid diagram showing system components
     - Technology stack with specific versions
     - Data flow description
     - Integration points

3. **Risk Analysis**
   - Identify at least 5 technical/business risks
   - Provide specific mitigation strategies
   - Assign risk owners and probabilities

### Phase 3: Quality Validation (1-2 hours)

1. **Run Quality Checks**
   ```bash
   python3 [SPEC_BUILDING_PATH]/automation/validate-all.py spec/SPEC.md
   ```

2. **Review Score**
   - Target score: 90+ for approval
   - If score < 90, review the improvement suggestions
   - Update the spec based on suggestions

3. **Iterate Until Quality**
   Keep improving based on the automated feedback until:
   - Structure validation: PASSED
   - Quality score: 90+
   - No critical warnings

### Phase 4: Review and Refinement (1 hour)

1. **Self-Review Checklist**
   Verify that your spec:
   - [ ] Answers any implementation question without ambiguity
   - [ ] Has quantified success metrics
   - [ ] Includes concrete test scenarios
   - [ ] Defines clear acceptance criteria
   - [ ] Addresses all major risks
   - [ ] Specifies technology versions
   - [ ] Has realistic timelines and budgets

2. **Final Validation**
   ```bash
   python3 [SPEC_BUILDING_PATH]/automation/score-spec-quality.py spec/SPEC.md -f markdown -o final-score.md
   ```

3. **Prepare for Review**
   Create a summary document `SPEC-SUMMARY.md` that includes:
   - Executive overview (2 paragraphs)
   - Key requirements list
   - Major technical decisions
   - Timeline and budget summary
   - Next steps for roadmap creation

## Key Quality Principles

Throughout this process:

1. **Be Specific**: Replace vague terms with quantified metrics
   - Bad: "Fast response time" 
   - Good: "Response time <200ms for 95th percentile"

2. **Think Testing**: For every requirement, define how to verify it
   - Include acceptance criteria
   - Create test scenarios
   - Define measurable thresholds

3. **Consider Implementation**: 
   - Justify technology choices
   - Address integration challenges
   - Plan for scalability

4. **Document Decisions**: 
   - Explain WHY, not just WHAT
   - Include alternatives considered
   - Document assumptions

## Expected Outputs

By the end, you should have:
1. `/[project-name]/spec/SPEC.md` - Complete specification (90+ quality score)
2. `/[project-name]/requirements/*.md` - All requirement documents filled
3. `/[project-name]/spec-quality-report.json` - Quality validation report
4. `/[project-name]/SPEC-SUMMARY.md` - Executive summary

## Anti-Patterns to Avoid

- Don't use placeholders or generic text
- Don't skip sections even if they seem less relevant
- Don't make assumptions without documenting them
- Don't ignore the quality score feedback
- Don't rush - take time to think through each section

Start now with Phase 1. Ask me any clarifying questions as you go.
```

## Example Usage

Here's how to use this with a specific project:

```markdown
You are tasked with creating a complete software specification for "CustomerInsight Pro". You will follow a structured process using the spec-building framework located at /Users/asmith/code/public/specs/spec-building.

## Project Context
CustomerInsight Pro is a B2B SaaS platform that helps e-commerce companies understand their customer behavior through advanced analytics. The platform will integrate with popular e-commerce platforms (Shopify, WooCommerce, etc.) to collect customer data, analyze purchasing patterns, and provide actionable insights through dashboards and automated reports.

Key objectives:
- Reduce customer churn by identifying at-risk customers
- Increase average order value through personalized recommendations  
- Improve marketing ROI with customer segmentation

Initial constraints:
- Must be GDPR compliant
- Initial budget of $500K
- 6-month timeline to MVP
- Team of 4 developers available

## Your Task
[Rest of the prompt template follows...]
```

## Tips for Success

### 1. Front-load Information
Provide the agent with as much context as possible upfront:
- Business goals and constraints
- User personas and needs
- Technical preferences or limitations
- Compliance requirements

### 2. Interactive Clarification
Encourage the agent to ask questions:
- "What specific metrics matter most to the business?"
- "Are there existing systems this needs to integrate with?"
- "What's the expected user load at launch?"

### 3. Iterative Refinement
- Let the agent complete a full draft first
- Review and provide specific feedback
- Have the agent run validation tools
- Iterate based on quality scores

### 4. Quality Gates
Don't proceed to the next phase until:
- Phase 1: All requirements documents are complete
- Phase 2: Initial spec scores at least 70+
- Phase 3: Final spec scores 90+

### 5. Use the Tools
The automation scripts are there to help:
- `generate-spec-template.py` - Creates proper structure
- `score-spec-quality.py` - Identifies improvements needed
- `validate-spec-structure.py` - Catches formatting issues
- `validate-all.py` - Comprehensive validation

## Common Challenges and Solutions

### Challenge: Agent creates vague requirements
**Solution**: Provide specific examples in your prompt:
```
For each requirement, include:
- Specific measurable criteria (e.g., "process 1000 orders/minute")
- User story format: "As a [user], I want [feature] so that [benefit]"
- Acceptance criteria checklist
```

### Challenge: Low quality scores
**Solution**: Focus on the dimension with lowest score:
- Completeness: Add missing sections
- Clarity: Add more quantified metrics
- Implementability: Add version numbers and justifications
- Testability: Add more test scenarios

### Challenge: Agent gets stuck
**Solution**: Break down the task:
```
Let's focus just on the functional requirements. For the e-commerce integration feature:
1. What specific data needs to be synchronized?
2. How often should synchronization occur?
3. What happens if the external system is unavailable?
```

## Monitoring Progress

Track these milestones:
1. ✅ Project structure created
2. ✅ Requirements documents complete
3. ✅ Initial SPEC.md created
4. ✅ First quality score run
5. ✅ Improvements implemented
6. ✅ 90+ quality score achieved
7. ✅ Final review complete

## Next Steps After Spec

Once the spec is complete (90+ score), the agent can:
1. Create a roadmap using `[SPEC_BUILDING_PATH]/02-planning/01-spec-to-roadmap.md`
2. Generate phase plans using `[SPEC_BUILDING_PATH]/02-planning/02-roadmap-to-phase-plans.md`
3. Set up execution tracking using `[SPEC_BUILDING_PATH]/03-execution/01-phase-execution-guide.md`

---

Remember: The goal is a spec that can answer any implementation question without ambiguity. Take the time to do it right.