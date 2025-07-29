# Project Standards and Best Practices

## Overview
This document defines the MANDATORY standards and practices for ALL projects in this repository. These standards ensure consistency, quality, and maintainability across all projects. Deviation from these standards requires explicit justification and approval.

## Core Development Principles

### 1. Research and Exploration FIRST
**CRITICAL**: Never start implementation without thorough research.

Before ANY implementation:
1. **Explore the problem space thoroughly**
   - Use subagents to research existing solutions
   - Investigate multiple approaches
   - Document findings in project logs
   - Identify potential challenges and risks

2. **Understand the ecosystem**
   - What libraries/frameworks exist?
   - What are the best practices in this domain?
   - What are common pitfalls?
   - What have others learned?

3. **Plan systematically**
   - Think long and hard about the approach
   - Consider multiple implementation strategies
   - Design for parallelization and subagent use
   - Document your reasoning

### 2. Continuous Understanding Updates
**REQUIREMENT**: You MUST update your understanding as you progress.

1. **Document learning as it happens**
   ```
   Location: .claude/logs/<task>/learning-journal.md
   ```
   - What assumptions were wrong?
   - What new insights emerged?
   - What patterns are becoming clear?
   - What questions arose?

2. **Revise plans based on new understanding**
   - Plans are living documents
   - Update them as you learn
   - Document why changes were made

3. **Share understanding with subagents**
   - Create clear context documents
   - Update shared knowledge bases
   - Ensure parallel work stays aligned

### 3. Systematic Thinking Requirements

**Think Long and Hard**: This is not a suggestion, it's a requirement.

1. **Break down problems systematically**
   - Decompose into smallest logical units
   - Identify dependencies clearly
   - Map out data flows
   - Consider error paths

2. **Step-by-step analysis**
   - Document each step of your thinking
   - Explain WHY, not just WHAT
   - Consider alternatives at each step
   - Justify chosen approaches

3. **Mental model documentation**
   ```
   Location: .claude/logs/<task>/mental-models.md
   ```
   - How do you conceptualize this problem?
   - What metaphors help understanding?
   - What diagrams illustrate key concepts?

### 4. Clarifying Questions Protocol

**ASK QUESTIONS**: Assumptions are project killers.

1. **Question categories to ALWAYS consider**:
   - **Requirements**: Is this what the user actually wants?
   - **Constraints**: What limitations exist?
   - **Performance**: What are acceptable metrics?
   - **Scale**: What growth is expected?
   - **Integration**: What must this work with?
   - **Maintenance**: Who will maintain this?

2. **Question timing**:
   - Before starting any task
   - When encountering ambiguity
   - When making architectural decisions
   - Before implementing complex features
   - When test cases reveal edge cases

3. **Document questions and answers**:
   ```
   Location: .claude/logs/<task>/qa-log.md
   ```

### 5. Strict Test-Driven Development

**See**: `.claude/patterns/tdd-strict.md` for detailed methodology

Key requirements:
- Write tests FIRST, always
- Minimum 80% coverage (100% for critical paths)
- Test behavior, not implementation
- Every commit must pass all tests

### 6. Subagent Utilization Standards

**MANDATORY**: Use subagents for parallel work and specialized tasks.

1. **When to use subagents**:
   - Research and exploration tasks
   - Parallel implementation of independent features
   - Specialized domain expertise needed
   - Large-scale file searches or analysis
   - Complex refactoring across multiple files

2. **Subagent task design**:
   - Provide complete, unambiguous context
   - Define clear success criteria
   - Specify exact output format needed
   - Include relevant file paths and constraints
   - Design tasks to be independent when possible

3. **Subagent coordination**:
   - See `.claude/patterns/subagent-coordination.md`
   - Document task dependencies clearly
   - Use standardized communication formats
   - Maintain task status tracking

## Code Quality Standards

### 1. Code Style and Conventions
- **Follow existing patterns**: Match the style already in the codebase
- **Consistency over preference**: Team consistency matters more than personal style
- **Use linters and formatters**: Automate style enforcement
- **Meaningful names**: Variables, functions, and files should be self-documenting

### 2. Documentation Requirements
Every project MUST include:

1. **README.md** with:
   - Project purpose and goals
   - Quick start guide
   - Development setup instructions
   - Architecture overview
   - Contributing guidelines

2. **Code documentation**:
   - Public APIs must be documented
   - Complex algorithms need explanations
   - "Why" comments for non-obvious decisions
   - Examples for common use cases

3. **Architecture Decision Records (ADRs)**:
   ```
   Location: .claude/logs/<task>/decisions/
   ```
   - Document significant decisions
   - Include context, options considered, and rationale
   - Update when decisions change

### 3. Version Control Standards

1. **Commit practices**:
   - Small, atomic commits
   - Conventional commit format
   - Test pass before EVERY commit
   - No commented-out code

2. **Branch strategy**:
   - Feature branches from main
   - Branch names: `feature/`, `fix/`, `chore/`
   - Keep branches short-lived
   - Rebase before merging

3. **Code review requirements**:
   - All code must be reviewed
   - Tests reviewed as rigorously as code
   - Documentation updates included
   - CI/CD must pass

## Project Setup Standards

### 1. Required Project Structure
```
project-name/
├── specs/                      # Capability definitions
├── plans/                      # Implementation instructions
├── prompts/                    # AI model instructions  
├── configs/                    # Project configurations
├── .claude/
│   └── logs/                  # Task logs and learning
├── src/                       # Source code
├── tests/                     # Test files
├── docs/                      # Additional documentation
├── .pre-commit-config.yaml    # Pre-commit hooks
├── Justfile                   # Common commands
├── docker-compose.yaml        # Container setup (if using Docker)
├── flake.nix                  # Nix setup (if using Nix)
└── README.md                  # Project documentation
```

### 2. Development Environment
- Must support reproducible builds
- Choose between Docker or Nix (see `.claude/guides/dev-environment.md`)
- Document ALL dependencies
- Include setup automation

### 3. CI/CD Pipeline
- Must run on EVERY commit
- Include: linting, testing, building, security scanning
- Block merging on failures
- Generate artifacts and reports

## Communication Standards

### 1. Avoiding Sycophancy
**Reference**: `.claude/guides/trust-building.md`

Key principles:
- Provide honest assessments
- Acknowledge limitations
- Offer alternatives when disagreeing
- Explain reasoning clearly
- Build trust through transparency

### 2. Progress Communication
- Regular status updates in logs
- Clear blocker identification
- Proactive risk communication
- Learning and insights sharing

## Quality Gates

### Mandatory Checks Before Marking Task Complete
1. ✓ All tests pass
2. ✓ Coverage meets minimum requirements  
3. ✓ Code follows style guidelines
4. ✓ Documentation is updated
5. ✓ Pre-commit hooks pass
6. ✓ CI/CD pipeline succeeds
7. ✓ Learning journal updated
8. ✓ Questions log current

### Definition of Done
A task is ONLY complete when:
- Functionality works as specified
- Tests provide confidence
- Code is maintainable
- Documentation enables others
- Knowledge is captured
- Standards are followed

## Continuous Improvement

### 1. Retrospectives
After each major task:
- What went well?
- What was challenging?
- What would you do differently?
- What patterns emerged?
- What tools would help?

### 2. Standards Evolution
- Standards are living documents
- Propose improvements with evidence
- Test changes on small projects first
- Document impact of changes

## Enforcement and Accountability

### 1. Pre-commit Hooks
Every project MUST configure pre-commit to check:
- Code style compliance
- Test execution
- Coverage thresholds
- Security scanning
- Documentation generation

### 2. CI/CD Enforcement
Pipelines MUST:
- Run all quality checks
- Block on any failure
- Generate compliance reports
- Track metrics over time

### 3. Review Checklist
Reviewers MUST verify:
- [ ] Standards compliance
- [ ] Test coverage adequate
- [ ] Documentation updated
- [ ] Subagents used appropriately
- [ ] Learning captured
- [ ] Questions asked and answered

---

## Remember: Excellence is a Habit

These standards exist to ensure every project delivers exceptional quality. They are not bureaucracy - they are the practices that distinguish professional work from amateur efforts.

**Think systematically. Work deliberately. Document thoroughly. Test rigorously.**

When in doubt, refer to these standards. When standards conflict with project needs, document why and propose updates.

**Your adherence to these standards directly impacts project success.**