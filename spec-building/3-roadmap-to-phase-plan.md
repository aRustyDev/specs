## Convert ROADMAP Phases to PLAN files

```markdown
First, Look through the specs, specifically at phase-9.
- api/.claude/SPEC.md
- api/.claude/.spec/*
- api/.claude/.plan/phase-9/*
- api/.claude/.plan/phase-1/*
- api/.claude/ROADMAP.md

GOAL: Create an optimal and robust plan that aligns with the projects specs/*, SPEC.md & ROADMAP.md, and mirrors phase-1 in its structure and content.

OUTPUTS:
- api/.claude/.plan/phase-9/WORK_PLAN.md
- api/.claude/.plan/phase-9/REVIEW_PLAN.md
- updates to contents of api/.claude/junior-dev-helper/

Next, Create a plan for the work that should be done to accomplish phase-9
Next, analyse the WORK_PLAN.md in api/.claude/.plan/phase-9/WORK_PLAN.md
Next, compare your plan against the WORK_PLAN, and update your knowledge
Next, think long and hard about what the optimal plan is for phase-9, break the plan up into two categories.
    1. Technical Implementation
    2. Quality Assurance/Code Review

When you have the plan categorized, write the Technical Implementation to the WORK_PLAN, and the Quality Assurance/Code Review to the REVIEW_PLAN.md

Purpose of REVIEW_PLAN: informs the reviewing agent of what to look for explicitly, and that they must give feedback on what they found, as well as updated plans for successfully completing the phase as defined.

The REVIEW_PLAN MUST
- set MANDATORY review scoping to ONLY the checkpoint in question and previously completed checkpoints.
- Require Stopping and giving feedback after finishing a review. Write to api/.claude/.reviews/checkpoint-X-feedback.md
- Require Stopping and writing progress to a file for the reviewers own reference after finishing a review. Write to api/.claude/.reviews/checkpoint-X-review-vY.md
- ALWAYS attempt to read any questions asked in the api/.claude/.reviews/checkpoint-X-questions.md, and write answers back in the same file if any exist.
- Have comprehensive reviewing instructions in it.
- verify the worker documented/commented their code well
- verify that tests are written and make sense
- verify that TDD patterns were followed
- check for "cleanliness" that looks for left over artifacts/stubs/test code or docs that need to be removed.
- direct the worker to the api/.claude/junior-dev-helper/ files for further guidance.
- check if the api/.claude/junior-dev-helper/ files provided adequate guidance for any topic the junior dev struggled with.
- Create/Update the relavent files in api/docs/src/ to reflect the changes/features implemented; use the api/docs/src/index.md to determine what files to update
- Commit changes at the end of every review
- Read questions from the api/.claude/.reviews/phase-9-checkpoint-X-questions.md and write answers back in the same file if any exist.
- Write Feedback to api/.claude/.reviews/phase-9-checkpoint-X-feedback.md

The WORK_PLAN MUST
- Set EXPLICIT NOT OPTIONAL ALWAYS MANDATORY requirements to stop for review of the agents work by an external party.
- Write any follow up questions after review to api/.claude/.reviews/checkpoint-X-questions.md, and wait until feedback has been provided if any questions are asked.
- ONLY have work plans in it, not items or context for external reviewers
- Commit changes at every checkpoint without exception; it is possible that there may be changes committed since the last checkpoint.
- Write questions to the api/.claude/.reviews/phase-9-checkpoint-X-questions.md
- Read Feedback from api/.claude/.reviews/phase-9-checkpoint-X-feedback.md

Make the stop points are in places where it will be easier to clean up, and that both the REVIEW_PLAN and WORK_PLAN checkpoints align.

update the contents of api/.claude/junior-dev-helper/ adding/updating examples, common errors, tutorials, tips, best practices, etc relevant to the junior dev for phase-9. phase-9 work plans MUST reference these.

Stop and Ask me for clarification whenever you are unsure or unclear
```

---

## Review and Update the PLANS

```markdown
GOAL: Identify escape hatches in the WORK_PLAN & REVIEW_PLAN and modify the plans to be strict enough but still flexible

First, review the files in the phase-9 directory
Second, Identify any and all escape hatches in the WORK_PLAN & REVIEW_PLAN
Third, Using your recent experience searching for escape hatches Identify points where using too strict of langauge may force an agent to panic or get stuck.
Fourth, Analyze the improvements you identified and create a plan to update the WORK_PLAN and REVIEW_PLAN to be strict enough to keep an agent honest and on task, but flexible enough to allow agents to recover from mistakes.
Fifth, Implement the plan.

GOAL(Updated after step 5): determine how good of plans the work and review plans are.

Sixth, review the following files & analyze their contents
Files (Step 6):
- api/.claude/.plan/phase-9/WORK_PLAN.md
- api/.claude/.plan/phase-9/REVIEW_PLAN.md
- api/.claude/SPEC.md
- api/.claude/.spec/*
- api/.claude/junior-dev-helper/** (How well do these files support the WORK_PLAN and REVIEW_PLAN?)
Factors (Step 6):
- Are the contents of the WORK_PLAN a clear enough description of what to do that a junior dev could be easily expected to successfully complete each stage?
- Do the PLANs align with the SPEC.md & .spec/* files definitions?
- Do the PLANs align with the ROADMAPs definition and order?
- Do both PLANs align with each other?

api/.claude/.plan/phase-9/WORK_PLAN.md
api/.claude/.plan/phase-9/REVIEW_PLAN.md
```
