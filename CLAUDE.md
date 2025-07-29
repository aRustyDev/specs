# CLAUDE Configuration - Project Specification Repository

## Overview
This repository serves as a meta-framework for organizing and managing multiple software projects. Each project follows a standardized structure with specifications (SPEC), implementation plans (PLAN), AI prompts (PROMPT), and configurations (CONFIG).

## Repository Purpose
- **SPEC Files**: Define project target capabilities and requirements
- **PLAN Files**: Provide detailed implementation instructions for developers
- **PROMPT Files**: Instruct AI models to follow plans and implement specifications using subagents
- **CONFIG Files**: Store project-specific configurations, CI/CD settings, and environment definitions

## Module System Configuration
This configuration extends the global CLAUDE.md with project-specific modules and workflows.

### Core Principles (Always Active)
- **RESEARCH FIRST**: Always conduct thorough research and exploration before planning
- **SYSTEMATIC THINKING**: Think long, hard, and step by step through every problem
- **CONTINUOUS CLARIFICATION**: Ask clarifying questions regularly; never assume
- **STRICT TDD**: Test-Driven Development is mandatory for all projects
- **UPDATE UNDERSTANDING**: Regularly update and document evolving understanding
- **USE SUBAGENTS**: Leverage subagents for parallel workflows and specialized tasks
- **AVOID SYCOPHANCY**: Build trust through honest, direct communication (see trust-building guide)

### Module Loading Configuration
```yaml
contexts:
  new-project:
    triggers: ["create project", "new project", "setup project", "initialize"]
    loads:
      - workflows/new-project-setup.md
      - templates/project-structure.md
      - standards/project-standards.md
    scope: persistent

  project-planning:
    triggers: ["create spec", "write plan", "design", "architecture"]
    loads:
      - patterns/subagent-coordination.md
      - patterns/tdd-strict.md
      - processes/logging-standards.md
    scope: context

  implementation:
    triggers: ["implement", "code", "develop", "build"]
    loads:
      - patterns/tdd-strict.md
      - guides/dev-environment.md
      - guides/pre-commit-setup.md
    scope: context

  ci-cd:
    triggers: ["ci/cd", "pipeline", "deploy", "publish"]
    loads:
      - guides/cicd-setup.md
      - templates/justfile-template.md
    scope: context
```

## Project Structure Template
Every project in this repository follows this structure:
```
./project-name/
├── specs/              # Capability definitions
├── plans/              # Implementation instructions
├── prompts/            # AI model instructions
├── configs/            # Project configurations
└── .claude/
    └── logs/          # Task logs and lessons learned
        └── <task>/    # Specific task directories
```

## Working Directory Convention
When working on a project, the working directory should be set to:
- `./project-name/` for project-specific tasks
- Repository root for cross-project operations

## Module Directory Reference
```
.claude/
├── guides/             # How-to guides for setup and configuration
├── templates/          # Reusable templates and starting points
├── patterns/           # Development patterns (TDD, subagents)
├── standards/          # Project standards and best practices
├── processes/          # Workflows and procedures
└── workflows/          # Complete end-to-end processes
```

## Quick Start
1. Run `!load workflows/new-project-setup.md` to begin creating a new project
2. Follow the systematic workflow to establish project context
3. Use templates and guides as needed for specific configurations

## Important Reminders
- **Always think systematically**: Break down complex problems into manageable steps
- **Document progress**: Log all decisions, challenges, and solutions to project logs
- **Use parallel workflows**: Design plans that support multiple subagents working concurrently
- **Maintain high test coverage**: Minimum 80% coverage, 100% for critical paths
- **Ask for clarification**: When in doubt, always ask rather than assume

---
*Note: This configuration works in conjunction with the global ~/.claude/CLAUDE.md configuration*