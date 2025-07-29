# New Project Setup Workflow

## Overview
This workflow guides you through creating a new project in this repository. Follow these steps systematically and thoroughly. Each step builds upon the previous one, so DO NOT skip steps or work ahead.

## Pre-Setup Checklist
Before beginning, ensure you have:
- [ ] Clear understanding of project requirements
- [ ] Identified the primary technology stack
- [ ] Determined the CI/CD platform to use
- [ ] Decided between Docker or Nix for development environment
- [ ] Gathered any existing specifications or requirements documents

## Step-by-Step Project Creation Process

### Phase 1: Project Foundation

#### Step 1.1: Create Project Directory Structure
```bash
# From repository root
PROJECT_NAME="your-project-name"  # Use kebab-case
mkdir -p $PROJECT_NAME/{specs,plans,prompts,configs}
mkdir -p $PROJECT_NAME/.claude/logs
mkdir -p $PROJECT_NAME/{src,tests,docs}
```

**Think Long and Hard**: Before proceeding, consider:
- Is this the right project name?
- Does it clearly indicate the project's purpose?
- Will it conflict with existing projects?

#### Step 1.2: Initialize Project Specification
Create `$PROJECT_NAME/specs/project-overview.md`:

```markdown
# Project: [Project Name]

## Purpose
[Clear, concise statement of what this project does and why it exists]

## Target Capabilities
[List of specific capabilities this project must deliver]
1. 
2. 
3. 

## Success Criteria
[Measurable criteria that define project success]
- 
- 
- 

## Constraints
- Technical: [Languages, frameworks, performance requirements]
- Business: [Deadlines, budget, compliance requirements]
- Operational: [Deployment environment, scaling needs]

## Key Stakeholders
[Who will use this, who maintains it, who makes decisions]

## Initial Questions
[List questions that need answering before proceeding]
1. 
2. 
3. 
```

**STOP**: Do not proceed until you have answered ALL initial questions. Use subagents to research if needed.

### Phase 2: Research and Exploration

#### Step 2.1: Technology Research
**USE SUBAGENTS** for parallel research:

1. Create research tasks in `.claude/logs/research/`:
   ```markdown
   # Research Task: [Technology/Library/Pattern]
   
   ## Objective
   Investigate [specific aspect] for use in [project context]
   
   ## Questions to Answer
   - What are the best practices?
   - What are common pitfalls?
   - What alternatives exist?
   - What is the community recommendation?
   
   ## Success Criteria
   - Provide comparison matrix
   - Include code examples
   - Document pros/cons
   - Recommend best option with justification
   ```

2. Document findings in `.claude/logs/research/findings.md`

#### Step 2.2: Architecture Planning
Based on research, create `$PROJECT_NAME/specs/architecture.md`:

```markdown
# Architecture Design

## High-Level Architecture
[Diagram or description of overall system design]

## Component Breakdown
[Detailed breakdown of each component]

### Component: [Name]
- **Purpose**: 
- **Responsibilities**: 
- **Interfaces**: 
- **Dependencies**: 

## Data Flow
[How data moves through the system]

## Technology Choices
[Justify each technology selection based on research]
- Language: [Choice] because [reasons]
- Framework: [Choice] because [reasons]
- Database: [Choice] because [reasons]

## Parallelization Opportunities
[Identify parts that can be developed in parallel by subagents]
1. 
2. 
3. 
```

### Phase 3: Development Environment Setup

#### Step 3.1: Choose Development Environment
Based on `.claude/guides/dev-environment.md`, decide:

**Docker** if:
- Need consistent environment across different OS
- Working with multiple services
- Want easy cleanup
- Team uses various development machines

**Nix** if:
- Want reproducible builds
- Need fine-grained dependency control
- Prefer declarative configuration
- Team is comfortable with functional approach

Document decision in `.claude/logs/setup/environment-decision.md`

#### Step 3.2: Create Environment Configuration

**For Docker**:
Create `$PROJECT_NAME/docker-compose.yaml`:
```yaml
version: '3.8'

services:
  dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/workspace
      - /workspace/node_modules  # Example for Node projects
    environment:
      - ENV=development
    command: [specific to your project]

  # Add other services as needed (database, cache, etc.)
```

Create `$PROJECT_NAME/Dockerfile.dev`:
```dockerfile
FROM [base-image]

WORKDIR /workspace

# Install development dependencies
RUN [package manager] install [dev tools]

# Copy dependency files
COPY [dependency files] .

# Install project dependencies
RUN [install command]

# Development command runs via docker-compose
```

**For Nix**:
Create `$PROJECT_NAME/flake.nix`:
```nix
{
  description = "[Project description]";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Add your development dependencies
          ];

          shellHook = ''
            echo "Development environment for [project-name]"
            # Add any setup commands
          '';
        };
      });
}
```

### Phase 4: Project Tooling Setup

#### Step 4.1: Create Justfile
Create `$PROJECT_NAME/Justfile` based on `.claude/templates/justfile-template.md`:

```just
# Project: [Project Name]
# This Justfile contains common commands for development

# Default command - shows help
default:
    @just --list

# Setup development environment
setup:
    [[ setup commands based on your environment ]]

# Run tests with coverage
test:
    [[ test command with coverage ]]

# Run linting
lint:
    [[ lint command ]]

# Run type checking (if applicable)
typecheck:
    [[ typecheck command ]]

# Build the project
build:
    [[ build command ]]

# Run the development server
dev:
    [[ dev server command ]]

# Clean build artifacts
clean:
    [[ clean command ]]

# Run pre-commit checks
pre-commit:
    [[ pre-commit run --all-files ]]

# Generate documentation
docs:
    [[ documentation generation command ]]
```

#### Step 4.2: Configure Pre-commit Hooks
Create `$PROJECT_NAME/.pre-commit-config.yaml` based on `.claude/guides/pre-commit-setup.md`:

```yaml
repos:
  # Language-specific linters
  - repo: [linter repo]
    rev: [version]
    hooks:
      - id: [linter-id]

  # Security scanning
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets

  # General file checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  # Custom test runner
  - repo: local
    hooks:
      - id: test-coverage
        name: Run tests with coverage check
        entry: just test
        language: system
        pass_filenames: false
        always_run: true
```

Install pre-commit:
```bash
cd $PROJECT_NAME
pre-commit install
pre-commit run --all-files  # Verify it works
```

### Phase 5: CI/CD Pipeline Setup

#### Step 5.1: Configure CI/CD
Based on `.claude/guides/cicd-setup.md` and project requirements:

Store configuration choice in `$PROJECT_NAME/configs/cicd-platform.yaml`:
```yaml
platform: [github-actions|gitlab-ci|jenkins|circleci]
reasons:
  - [reason 1]
  - [reason 2]
```

Create appropriate CI/CD configuration file.

### Phase 6: Planning and Documentation

#### Step 6.1: Create Initial Development Plan
Create `$PROJECT_NAME/plans/initial-development.md`:

```markdown
# Initial Development Plan

## Overview
[Brief description of the development approach]

## Phase 1: Foundation (Tasks for Parallel Development)
### Subagent Task 1: [Core Module]
- **Objective**: 
- **Dependencies**: None
- **Deliverables**: 
- **Test Requirements**: 

### Subagent Task 2: [Another Module]
- **Objective**: 
- **Dependencies**: None
- **Deliverables**: 
- **Test Requirements**: 

## Phase 2: Integration
[Tasks that depend on Phase 1 completion]

## Phase 3: Enhancement
[Additional features and optimizations]

## Risk Mitigation
[Identify risks and mitigation strategies]

## Success Metrics
[How we measure progress and completion]
```

#### Step 6.2: Create Subagent Prompts
For each parallel task, create a prompt in `$PROJECT_NAME/prompts/`:

```markdown
# Subagent Task: [Task Name]

## Context
You are implementing [specific component] for [project name]. This component is responsible for [clear description].

## Your Objective
Think long and hard about this problem, then implement [specific functionality] following strict TDD practices.

## Requirements
1. [Specific requirement 1]
2. [Specific requirement 2]

## Constraints
- Must follow TDD (write tests first)
- Must achieve >90% test coverage
- Must follow existing code style in [reference files]
- Must integrate with [interfaces]

## Steps to Follow
1. **Research**: Investigate [specific aspects]
2. **Design**: Create interface design that [requirements]
3. **Test First**: Write comprehensive tests for all functionality
4. **Implement**: Create minimal implementation to pass tests
5. **Refactor**: Improve code quality while maintaining green tests
6. **Document**: Update documentation with your implementation

## Deliverables
- [ ] Test files with >90% coverage
- [ ] Implementation that passes all tests
- [ ] Updated documentation
- [ ] Learning journal with insights

## Important Reminders
- Ask clarifying questions if anything is ambiguous
- Update your understanding as you learn
- Think systematically and document your reasoning
- Use the TDD cycle: Red-Green-Refactor
- Commit after each successful cycle

Remember: Think step by step, systematically, and thoroughly.
```

### Phase 7: Project Initialization

#### Step 7.1: Initialize Version Control
```bash
cd $PROJECT_NAME
git init
git add .
git commit -m "Initial project structure for $PROJECT_NAME"
```

#### Step 7.2: Create Initial README
Create `$PROJECT_NAME/README.md`:

```markdown
# [Project Name]

## Purpose
[One paragraph description]

## Quick Start
\```bash
# Clone the repository
git clone [repo-url]
cd [project-name]

# Setup development environment
just setup

# Run tests
just test

# Start development
just dev
\```

## Project Structure
\```
.
├── specs/      # Project specifications
├── plans/      # Development plans
├── prompts/    # Subagent task prompts
├── configs/    # Configuration files
├── src/        # Source code
├── tests/      # Test files
└── docs/       # Additional documentation
\```

## Development
See [plans/initial-development.md](plans/initial-development.md) for the development roadmap.

## Contributing
1. Follow TDD practices (see .claude/patterns/tdd-strict.md)
2. Ensure all tests pass before committing
3. Update documentation with changes
4. Use conventional commits

## Standards
This project follows the standards defined in `.claude/standards/project-standards.md`
```

### Phase 8: Verification and Handoff

#### Step 8.1: Verify Setup Completeness
Run through this checklist:
- [ ] All directory structures created
- [ ] Specifications documented
- [ ] Research completed and documented
- [ ] Development environment works
- [ ] Pre-commit hooks installed and working
- [ ] CI/CD pipeline configured
- [ ] Initial plan created with parallel tasks
- [ ] Subagent prompts prepared
- [ ] README provides clear starting point

#### Step 8.2: Create Setup Summary
Create `.claude/logs/setup/summary.md`:

```markdown
# Project Setup Summary

## Project: [Name]
## Setup Date: [Date]
## Setup By: [Agent/Human]

## Decisions Made
1. Development Environment: [Docker/Nix] because [reasons]
2. CI/CD Platform: [Platform] because [reasons]
3. Technology Stack: [Summary]

## Research Findings
[Key insights from research phase]

## Identified Risks
[Any risks discovered during setup]

## Next Steps
1. Begin Phase 1 development using subagent prompts
2. [Other immediate tasks]

## Lessons Learned
[Any insights gained during setup]
```

## Post-Setup Reminders

1. **Start with TDD**: Don't write any code without tests first
2. **Use Subagents**: Launch parallel development tasks immediately
3. **Document Progress**: Keep logs updated in `.claude/logs/`
4. **Ask Questions**: Better to clarify than assume
5. **Think Systematically**: Take time to think through problems properly

## Troubleshooting

### Common Issues

**Issue**: Pre-commit hooks failing
**Solution**: Run `just lint` and `just test` separately to identify specific issues

**Issue**: Docker/Nix environment not working
**Solution**: Check logs in `.claude/logs/setup/` for environment decisions and validate configuration

**Issue**: Unclear requirements
**Solution**: STOP and ask for clarification. Document questions in specs.

**Issue**: Technology choice proving problematic
**Solution**: Document the issue, research alternatives, propose change with justification

---

Remember: **Quality over speed**. Take time to set up projects properly. A well-structured project saves countless hours later.