# Repository SPEC Generation Prompt

## Context
You are tasked with analyzing a repository and generating a comprehensive SPEC.md file following a systematic methodology. You will reverse-engineer requirements from the existing codebase, identify patterns, and create detailed specifications.

## Prerequisites
Before starting, ensure you have access to:
- The complete repository structure
- All source code files
- Configuration files (CI/CD, build tools, etc.)
- Documentation (if any exists)
- Test files and coverage reports
- Dependency manifests (package.json, requirements.txt, etc.)

## Process

### Phase 1: Repository Analysis and Requirements Extraction

1. **Initial Repository Scan**
   - Map the complete directory structure
   - Identify technology stack and frameworks
   - Catalog all configuration files
   - List external dependencies
   - Note existing documentation

2. **Code Analysis**
   - Identify architectural patterns
   - Map component relationships
   - Extract business logic and features
   - Document APIs and interfaces
   - Analyze data models and schemas

3. **Infrastructure and DevOps Analysis**
   - Examine CI/CD configurations
   - Identify deployment patterns
   - Review infrastructure as code
   - Document build processes
   - Analyze testing strategies

### Phase 2: Requirements Synthesis

4. **Generate Initial Requirements**
   Based on your analysis, create:
   - Functional requirements derived from code features
   - Non-functional requirements from configurations
   - CI/CD requirements from pipeline definitions
   - Pre-commit requirements from hooks configuration
   - Documentation requirements from existing docs

5. **Disambiguation and Clarification**
   For each identified requirement:
   - Extract implicit requirements from implementation details
   - Decompose compound requirements into atomic ones
   - Identify missing or implied requirements
   - Document assumptions that need validation

### Phase 3: Research and Context Gathering

6. **Create Research Plans**
   Generate exploration plans for:
   - Alternative CI/CD patterns that could enhance current setup
   - Relevant architectural patterns for the technology stack
   - Industry best practices for similar projects
   - Security and compliance considerations
   - Performance optimization opportunities

7. **Document Context**
   Create context documentation for:
   - Current implementation patterns
   - Technology choices and rationale
   - Integration points and dependencies
   - Deployment architecture
   - Development workflow

### Phase 4: SPEC Generation

8. **Create Initial SPEC.md**
   Structure the specification to include:
   ```markdown
   # Project Specification

   ## Overview
   [Project description based on repository analysis]

   ## Architecture
   ### Application Architecture
   [Derived from code structure]

   ### Deployment Architecture
   [Based on CI/CD and infrastructure]

   ### Infrastructure Patterns
   [From IaC and configuration]

   ## Features and Capabilities
   [Extracted from codebase functionality]

   ## Components
   [Mapped from repository structure]

   ## Technical Stack
   ### Languages and Frameworks
   ### Libraries and Dependencies
   ### Tools and Services

   ## Development Standards
   ### Code Style and Conventions
   ### Testing Strategy
   ### Documentation Standards

   ## CI/CD Pipeline
   ### Build Process
   ### Testing Stages
   ### Deployment Strategy
   ### Release Patterns

   ## Quality Metrics
   ### Coverage Targets
   ### Performance Metrics
   ### Security Measures
   ### Compliance Requirements

   ## User Experience
   [If applicable, from UI/UX analysis]
   ```

9. **Apply Analysis Techniques**
   - MoSCoW prioritization of features
   - Trade-off analysis for architectural decisions
   - Ambiguity detection in specifications
   - Interface analysis and traceability
   - Quality metrics definition

### Phase 5: Modular Decomposition

10. **Functional Decomposition**
    - Break down high-level features into sub-features
    - Map user tasks to system responses
    - Create component-specific specifications
    - Generate modular spec files for logical components

11. **Create Modular Specs**
    Generate `.claude/.spec/` directory with:
    - Component-specific specifications
    - Interface definitions
    - Integration requirements
    - Testing specifications

### Phase 6: Validation and Refinement

12. **Cross-Reference and Validate**
    - Ensure consistency between SPEC.md and modular specs
    - Validate against actual codebase
    - Check for completeness and coverage
    - Identify gaps or contradictions

13. **Generate Roadmap**
    Based on current state vs. identified improvements:
    - Define enhancement milestones
    - Propose modernization phases
    - Suggest quality improvement initiatives
    - Plan documentation updates

## Output Requirements

### SPEC.md Format
- Use clear, hierarchical markdown structure
- Include cross-references to modular specs
- Provide traceability to code locations
- Use consistent terminology throughout

### YAML Configuration Standards
All YAML files must follow:
- 4-space indentation (no tabs)
- Array markers aligned with parent keys
- Clear visual hierarchy for nested structures

### Documentation Principles
- Living documentation synchronized with code
- Clear quality criteria and success metrics
- Systematic validation processes
- Automated documentation where possible

## Validation Questions

After generating the initial SPEC, validate by asking:
1. Does the SPEC accurately reflect the current codebase?
2. Are all major components and features captured?
3. Are the identified requirements complete and unambiguous?
4. Do the proposed improvements align with project goals?
5. Are there any critical aspects missing from the analysis?

## Implementation Notes

- Start with automated analysis where possible
- Use static analysis tools to extract metrics
- Parse configuration files programmatically
- Generate dependency graphs automatically
- Create traceability matrices from code to requirements

Remember: The goal is to create a comprehensive specification that both documents the current state and provides a foundation for future development, all derived from the actual repository contents.
