# File Consolidation and Separation Decisions

## Files to Keep Separate (Different Purposes)

### 1. Spec Creation Processes
These serve different starting scenarios and should remain distinct:

| File | Target Scenario | Key Differences | Keep Because |
|------|----------------|-----------------|--------------|
| `1-create-spec-v3.md` → `01-greenfield-spec-process.md` | New projects starting from requirements | Template-driven, discovery phase, stakeholder interviews | Most projects start here |
| `spec-from-repo.md` → `02-repository-spec-process.md` | Existing codebases needing specs | Code analysis, reverse engineering, pattern detection | Different skillset and tools |

### 2. Planning Documents
These are sequential steps that build on each other:

| File | Purpose | Depends On | Produces |
|------|---------|------------|----------|
| `2-spec-to-roadmap.md` | Break spec into phases | Completed spec | Roadmap with milestones |
| `3-roadmap-to-phase-plan.md` | Detail each phase | Roadmap | Worker & review plans |

### 3. Quality Processes
Different quality checkpoints:

| File | When Used | Focus |
|------|-----------|-------|
| `5-review-improve-spec.md` | After spec creation | Spec quality (target 90+) |
| `alignment-validation.md` | After planning | Document consistency |

## Files to Consolidate or Remove

### 1. Redundant Versions
**Action: Archive older versions**
- `1-create-spec.md` - Original version, superseded by v3
- `1-create-spec-v2.md` - Intermediate version, superseded by v3
- Keep only: `1-create-spec-v3.md` (rename for clarity)

### 2. Overlapping Content
**Action: Merge or clarify scope**

| Files | Overlap | Resolution |
|-------|---------|------------|
| `2-spec-to-modules.md` | Partially covers breaking down specs | Merge useful content into `2-spec-to-roadmap.md`, then remove |
| `templates/alignment-validation.md` | Duplicates process file | Keep process file, remove template |
| `test-integration.md` | Testing the process itself | Move content to `automation/README.md` |

### 3. Unclear Purpose
**Action: Remove or repurpose**
- `shared-context.md` - Empty file, remove
- `4-mdbook-documenting.md` - If contains valuable content about documentation, move to guides/

### 4. Implementation Artifacts
**Action: Archive**
These were work products, not process docs:
- `implementation-plan.md`
- `improvement-implementation-plan.md`
- `IMPROVEMENTS-SUMMARY.md` (keep temporarily for reference during cleanup)

## Template Consolidation

### Keep All These Templates (Each Serves Unique Purpose)

**Requirements Templates:**
- `outcome-definition.md` - Business/user outcomes
- `acceptance-scenarios.md` - Test scenarios
- `user-story.md` - Individual story format
- `use-case.md` - Detailed use cases
- `non-functional-requirements.md` - Performance, security, etc.

**Planning Templates:**
- `worker-plan.yml` - Execution plan for developers
- `review-plan.yml` - Quality review plan
- `team-skills-matrix.md` - Team assessment

**Quality Templates:**
- `spec-quality-rubric.md` - Scoring framework
- `spec-improvement-checklist.md` - Quick improvement guide
- `review-checklist.md` - Review process checklist

**Decision Support:**
- `decision-matrix.md` - Technology/approach decisions
- `complexity-factors.md` - Estimation multipliers
- `estimation-calibration.md` - Estimation improvement

### Templates to Consolidate

| Current Files | Issue | Solution |
|---------------|-------|----------|
| `quality-criteria.md`, `validation-gates.md`, `phase-gates.md` | Overlapping quality checks | Merge into single `quality-gates.md` |
| `research-criteria.md`, `research-methodology.md` | Both about research | Merge into `research-guide.md` |
| `requirements.md`, `project-contexts.md` | Vague purposes | Clarify or merge into other templates |

## Naming Convention Rationale

### Process Files (Action-Oriented)
Format: `XX-verb-object.md`
- `01-create-greenfield-spec.md` ❌ Too specific
- `01-greenfield-spec-process.md` ✅ Clear it's a process
- `01-spec-to-roadmap.md` ✅ Shows transformation

### Templates (Noun-Based)
Format: `object-template.md`
- `outcome-definition.md` ✅ What you're defining
- `worker-plan.yml` ✅ Type of plan
- `spec-quality-rubric.md` ✅ Purpose clear

### Guides (Topic-Focused)
Format: `topic-guide.md` or `topic-best-practices.md`
- `spec-antipatterns.md` ✅ Clear topic
- `complexity-factors.md` ✅ Reference guide
- `spec-review-best-practices.md` ✅ How-to guide

## Decision Summary

### Keep Separate (22 files)
Core processes, unique templates, and valuable guides that serve distinct purposes.

### Consolidate (6-8 files → 3-4 files)
Overlapping quality gates, research guides, and vague templates.

### Archive (7 files)
Old versions, implementation plans, and superseded documents.

### Delete (2 files)
Empty or no-value files.

## Final File Count
- Current: ~58 files
- After cleanup: ~35-40 files (organized into clear directories)
- Reduction: ~30% fewer files, 100% better organization