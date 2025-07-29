## Create the rough SPEC file

PREREQUISITES:
- .claude/.spec/templates/user-story.md
- .claude/.spec/templates/use-case.md
- .claude/.spec/templates/quality-criteria.md
- .claude/.spec/wip/requirements.md
- .claude/.spec/wip/spec-v1.md

OUTPUTS:
- .claude/SPEC.md
- .claude/.spec/<sub-topic>.md

1. Generate the templates, Prompt me to fill them out, and wait for my ok to read them
2. Read the .spec/wip/* files
3. describe your understanding of the requirements based on the contents, then prompt for validation and clarification of specific requirements/content items, then update the contents, then re-read and repeat this process until the contents are clear and complete and you have no further clarifications.
    - questions must disambiguate the contents
    - questions must extract requirements from specified implementation details
    - questions must validate and gather rationale for specified requirements
    - questions must identify and decompose compound requirements into their constituent Requirements.
    - the requirements MUST specify CI/CD requirements
    - the requirements MUST specify pre-commit requirements
    - the requirements MUST specify MDBook requirements

3. REQUIREMENTS REFINEMENT:
   Phase A - Extraction:
   - Disambiguate all compound requirements
   - Extract requirements from implementation details
   - Create traceability matrix: requirement → rationale → source

   Phase B - Validation:
   - Cross-reference against user stories
   - Identify conflicts and dependencies
   - Create decision tree for conditional requirements

   Phase C - Formalization:
   - Convert to structured format (Given/When/Then or similar)
   - Add measurable acceptance criteria
   - Tag with MoSCoW priority (early classification)

GATE: Post-Requirements (after step 3)
    □ All compound requirements decomposed
    □ CI/CD requirements specified
    □ No implementation details without extracted requirements
    □ User confirms no missing requirements
    → Generate gate summary, get approval to proceed

4. COMPONENT IDENTIFICATION:
    - Identify logical boundaries (features, services, infrastructure layers)
    - Create stub files:
    .spec/components/auth.md (placeholder)
    .spec/components/api.md (placeholder)
    .spec/interfaces/auth-api.md (placeholder)
    - Mark each as "DRAFT" with known requirements
    - This allows future extensions to target specific files

5. LEAD RESEARCHER: Analyze requirements and create research assignments:
   - CI/CD Research Agent: Investigate tools/workflows with criteria:
     * Must support [identified project type]
     * Must integrate with [identified constraints]
     * Stop after finding 3-5 viable options with pros/cons
   - Architecture Research Agent: Similar bounded criteria
   - Tool Research Agent: MDBook/pre-commit with specific feature requirements

6. PARALLEL EXECUTION: Deploy sub-agents with:
   - Specific success criteria per agent
   - Token budget (e.g., 5k per agent)
   - Required output format for .spec/context/

7. SYNTHESIS: Lead researcher consolidates findings into decision matrix

GATE: Post-Research (after step 7)
    □ At least 3 options evaluated per category
    □ Decision criteria documented
    □ Trade-offs identified
    □ User confirms research scope sufficient
    → Generate decision matrix, get approval to proceed

4. Use the contents to generate research and exploration plans for the following:
    - ci/cd jobs, actions, tools, and workflows that could be useful
    - MDBook plugins that could be useful
    - pre-commit hooks that could be useful
    - application architecture patterns relevant to the project
    - deployment architecture patterns relevant to the project
    - infrastructure patterns relevant to the project
<!-- 5. Execute the plans in as sub agents, then write the discovered context to the .spec/context/ directory
6. When all the agents have completed their research, analyze and compile your findings, then put a summary of the findings as initial recommendations and follow up questions into a .spec/wip/follow-up-vX.md file. Then prompt me to read it and answer the questions. When i have responded then continue
7. Using the follow up document, and your compiled and analyzed context, create a plan to research and explore implementation patterns and tasks that will achieve optimal alignment with the project specs. Then implement that research plan. -->

8. Using the results of the research, analyze and compile your findings and create the SPEC.md file that defines the project's application architecture, deployment strategies, infrastructure patterns, features, capabilities, user experience, components, implementation patterns, libraries, tools, frameworks, dependencies, target coverages, compliances, security measures, performance metrics and targets, documentation goals, testing strategies, release formats and patterns, and development methodologies and standards.
9. Using the SPEC.md file, attempt to conduct MoSCoW prioritization, repeatedly prompt me to ensure accuracy, confirm your assessment and recommendations. When i have given full approval, create a plan to implement your approved recommendations, and finally implement that plan to update the SPEC.md file.
10. Using the SPEC.md file, attempt to define trade-off analysis, repeatedly prompt me to ensure accuracy, confirm your assessment and recommendations. When i have given full approval, create a plan to implement your approved recommendations, and finally implement that plan to update the SPEC.md file.
11. Using the SPEC.md file, attempt to detect Ambiguity in the content, repeatedly prompt me to ensure accuracy, confirm your assessment and recommendations. When i have given full approval, create a plan to implement your approved recommendations, and finally implement that plan to update the SPEC.md file.
12. Using the SPEC.md file, attempt to define stakeholder cross-validation, by role playing the different user stories and ones generated that are relevant to the project. Generate scenario-based walkthroughs until no relavant and distinctly unique scenarios remain or I say we have enough. As we go, continuously prompt me for my input and update the SPEC.md file with the new information reflecting the scenarios and role played user story outcomes.
13. Using the SPEC.md file, attempt to conduct interface analysis and traceability gap analysis, repeatedly prompt me to ensure accuracy, confirm your assessment and recommendations. When i have given full approval, create a plan to implement your approved recommendations, and finally implement that plan to update the SPEC.md file.
14. Using the SPEC.md file, attempt to identify opportunities for Formal verification using mathematical approaches including model checking, theorem proving, and static analysis. Prompt me with your analysis for validation and approval, then generate a plan to implement your approved recommendations, and finally implement that plan to update the SPEC.md file.
15. Using the SPEC.md file, attempt to identify Quality Metrics to track completeness, consistency, verifiability, traceability, and modifiability. Generate a plan to implement your approved recommendations, and finally implement that plan to update the SPEC.md file.
16. Using the SPEC.md file, attempt to define measurement gathering approaches like requirements traceability matrices, coverage analysis, defect density tracking. Generate a plan to implement your approved recommendations, and finally implement that plan to update the SPEC.md file.
17. Using the SPEC.md file, attempt to conduct Functional decomposition on the SPEC.md contents, repeatedly breaking high-level features into sub-features, user tasks, and system responses, and files the contents into smaller, more manageable pieces until no further decomposition is possible or I say we have enough. Then using that information create modular spec files in the project local .claude/.spec/ directory for each of the logically distinct components identified in the SPEC.md file.
18. Go through the modular spec files one by one, review the content and expand on it to make it more detailed and comprehensive.
19. Review the SPEC.md file and the modular spec files and refactor the SPEC.md file to serve as a higher level reference of the projects spec that references and points to the individual component specs. Finally, ensure that they are all consistent and aligned with eachother.

19. EXTENSION POINTS:
    - Create .spec/extension-points.md documenting:
        * Stable interfaces that won't change
        * Flexible areas designed for extension
        * Dependency boundaries
        * Version compatibility rules
    - Add "EXTENDS:" headers in component specs for traceability

20. Using the SPEC.md file and the spec files, create a detailed project roadmap that outlines the project's milestones, phases, and deliverables. The roadmap should Start with clear quality criteria and systematic processes while adapting to project context. It should Implement gradually through pilot projects, building expertise while establishing success metrics, automation patterns, and continuous validation practices. It should also include built in plans for project cleanup, updating and verifying Living documentation that is synchronized with code,

21. PHASE PLAN GENERATION:
    - Controller Agent: Reads roadmap, assigns phase planning tasks
    - Parallel Phase Planners:
        * Worker Planner: Uses worker template + phase requirements
        * Reviewer Planner: Uses review template + quality criteria
        * Aligner Planner: Cross-references all plans for conflicts
        * Documenter Planner: Creates living doc update plans
    - Synthesis Agent: Merges plans, identifies dependencies
    - Validation: User reviews consolidated phase plan


### Identify Ambiguous Goals/Requirements first
> through iterative refinement and continuous validation

- Prototyping and simulation

```markdown

```
