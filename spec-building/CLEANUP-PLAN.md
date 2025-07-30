# Spec-Building Directory Cleanup Plan

## Current State Analysis

The directory contains:
- Multiple versions of processes (1-create-spec.md, v2, v3)
- Overlapping files with unclear purposes
- Good templates and guides but poor organization
- Numbered files that don't clearly show relationships
- Implementation artifacts mixed with process documentation

## Proposed Directory Structure

```
spec-building/
├── README.md                              # Overview and quick start guide
├── PROCESS-FLOW.md                        # Visual pipeline overview
│
├── 01-spec-creation/                      # Phase 1: Creating specs
│   ├── README.md                          # Overview of spec creation
│   ├── 01-greenfield-spec-process.md      # For new projects
│   ├── 02-repository-spec-process.md      # For existing codebases
│   └── 03-spec-quality-review.md          # Review and improvement
│
├── 02-planning/                           # Phase 2: From spec to plans
│   ├── README.md                          # Overview of planning
│   ├── 01-spec-to-roadmap.md              # Breaking into phases
│   ├── 02-roadmap-to-phase-plans.md       # Detailed planning
│   └── 03-alignment-validation.md         # Ensuring consistency
│
├── 03-execution/                          # Phase 3: Implementation
│   ├── README.md                          # Overview of execution
│   ├── 01-phase-execution-guide.md        # How to execute plans
│   ├── 02-change-management.md            # Managing changes
│   └── 03-failure-recovery.md             # When things go wrong
│
├── templates/                             # All reusable templates
│   ├── requirements/
│   │   ├── outcome-definition.md
│   │   ├── acceptance-scenarios.md
│   │   ├── user-stories.md
│   │   └── non-functional-requirements.md
│   ├── planning/
│   │   ├── roadmap-template.md
│   │   ├── worker-plan.yml
│   │   ├── review-plan.yml
│   │   └── team-skills-matrix.md
│   ├── quality/
│   │   ├── spec-quality-rubric.md
│   │   ├── review-checklist.md
│   │   └── alignment-validation.md
│   └── decision-support/
│       ├── decision-matrix.md
│       ├── complexity-factors.md
│       └── estimation-calibration.md
│
├── guides/                                # Best practices and how-tos
│   ├── spec-antipatterns.md
│   ├── spec-review-best-practices.md
│   ├── complexity-assessment.md
│   └── quick-reference.md
│
├── automation/                            # Scripts and tools
│   ├── README.md                          # Script documentation
│   ├── generate-spec-template.py
│   ├── validate-all.py
│   ├── validation/
│   │   ├── validate-spec-structure.py
│   │   ├── validate-spec-links.py
│   │   ├── score-spec-quality.py
│   │   ├── validate-requirements-traceability.py
│   │   └── validate-alignment.py
│   └── improvement/
│       └── suggest-spec-improvements.py
│
├── examples/                              # Complete worked examples
│   └── taskmaster/                        # Full example project
│       ├── README.md
│       ├── requirements/
│       ├── spec/
│       ├── roadmap/
│       ├── phase-plans/
│       └── validation/
│
└── archive/                               # Old versions for reference
    ├── implementation-plans/
    └── old-processes/
```

## File Renaming and Consolidation Plan

### 1. Core Process Files

**Rename and Move:**
- `1-create-spec-v3.md` → `01-spec-creation/01-greenfield-spec-process.md`
- `spec-from-repo.md` → `01-spec-creation/02-repository-spec-process.md`
- `5-review-improve-spec.md` → `01-spec-creation/03-spec-quality-review.md`
- `2-spec-to-roadmap.md` → `02-planning/01-spec-to-roadmap.md`
- `3-roadmap-to-phase-plan.md` → `02-planning/02-roadmap-to-phase-plans.md`
- `alignment-validation.md` → `02-planning/03-alignment-validation.md`
- `change-management.md` → `03-execution/02-change-management.md`
- `failure-recovery-guide.md` → `03-execution/03-failure-recovery.md`

**Archive:**
- `1-create-spec.md` → `archive/old-processes/`
- `1-create-spec-v2.md` → `archive/old-processes/`
- `implementation-plan.md` → `archive/implementation-plans/`
- `improvement-implementation-plan.md` → `archive/implementation-plans/`

**Delete or Merge:**
- `2-spec-to-modules.md` - Merge relevant content into planning process
- `4-mdbook-documenting.md` - Move to guides if valuable, otherwise archive
- `shared-context.md` - Delete (empty file)
- `test-integration.md` - Move relevant tests to automation/README.md

### 2. Create New Overview Files

**New Files to Create:**
- `README.md` - Main entry point with quick start guide
- `PROCESS-FLOW.md` - Visual overview replacing `end-to-end-process.md`
- `01-spec-creation/README.md` - When to use each spec creation approach
- `02-planning/README.md` - Planning phase overview
- `03-execution/README.md` - Execution phase overview
- `automation/README.md` - How to use the scripts

### 3. Template Organization

Move all templates to organized subdirectories:
- Requirements templates → `templates/requirements/`
- Planning templates → `templates/planning/`
- Quality templates → `templates/quality/`
- Decision templates → `templates/decision-support/`

### 4. Clear Naming Conventions

**Process Files:**
- Format: `XX-action-name.md` where XX is the step number
- Example: `01-greenfield-spec-process.md`

**Templates:**
- Format: `purpose-template.md` or `purpose-template.yml`
- Example: `outcome-definition.md`, `worker-plan.yml`

**Guides:**
- Format: `topic-guide.md` or `topic-best-practices.md`
- Example: `spec-antipatterns.md`, `spec-review-best-practices.md`

## Implementation Steps

### Phase 1: Create New Structure
```bash
# Create new directories
mkdir -p 01-spec-creation 02-planning 03-execution
mkdir -p templates/{requirements,planning,quality,decision-support}
mkdir -p guides automation/{validation,improvement}
mkdir -p examples archive/{implementation-plans,old-processes}
```

### Phase 2: Move and Rename Files
Execute the file movements according to the plan above.

### Phase 3: Create Overview Documentation
Write new README files that:
- Explain when to use each process
- Show clear flow between phases
- Provide quick decision trees

### Phase 4: Update Cross-References
- Update all internal links to match new structure
- Ensure numbered processes reference next steps
- Add "Next: " and "Previous: " navigation

### Phase 5: Validate
- Run link validation scripts
- Test full workflow with new structure
- Update automation scripts for new paths

## Benefits of New Structure

1. **Clear Flow**: Numbered directories show progression
2. **Purpose-Driven**: File names clearly indicate function
3. **No Duplication**: Each file has distinct purpose
4. **Easy Navigation**: Logical grouping by phase
5. **Scalable**: Easy to add new processes or templates
6. **Self-Documenting**: Structure explains the workflow

## Success Criteria

- [ ] New user can understand the process in 5 minutes
- [ ] Clear when to use greenfield vs repository approach
- [ ] No confusion about file purposes
- [ ] All links work correctly
- [ ] Automation scripts function with new structure
- [ ] Examples remain fully functional