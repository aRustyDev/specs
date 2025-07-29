# Phase Plan Generation Commands
# For use with Claude Code to create consistent implementation plans

# Generate a narrative phase plan from complete JSON configuration (v2)
create-phase-plan config_file:
    python3 scripts/generate_phase_plan_v2.py {{config_file}}

# Create example code review plan generator (see implementation guide)
example-review-generator:
    @echo "See .claude/guides/GENERATOR_IMPLEMENTATION_GUIDE.md for how to create"
    @echo "custom generators for different document types like code review plans."

# Show path to complete example configuration
show-phase-config-example:
    @echo "Complete example configuration with all sections:"
    @echo "  .claude/examples/phase-5-complete-config.json"
    @echo ""
    @echo "View with: cat .claude/examples/phase-5-complete-config.json | jq ."
    @echo ""
    @echo "The example includes:"
    @echo "  - All required sections with narrative content"
    @echo "  - Multiple work sections with tasks and code examples"
    @echo "  - Security requirements and learning paths"
    @echo "  - Complete content ready for generation"

# Validate phase plan quality (checks for TODOs, structure, actionability)
validate-phase-plan plan_file:
    python3 scripts/validate_workplan.py {{plan_file}}

# Validate JSON config and generate test plan to check output
validate-phase-config config_file:
    @echo "Validating {{config_file}}..."
    @python3 -m json.tool {{config_file}} > /dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON"
    @echo "Checking generated output quality..."
    @python3 scripts/validate_workplan.py --config {{config_file}} --check-generation

# Show generator implementation guide
show-generator-guide:
    @echo "Generator Implementation Guide:"
    @echo "  Location: .claude/guides/GENERATOR_IMPLEMENTATION_GUIDE.md"
    @echo ""
    @echo "This guide explains how to create generators for:"
    @echo "  - Code review plans"
    @echo "  - API documentation"
    @echo "  - Deployment runbooks"
    @echo "  - Architecture decision records"
    @echo "  - And any other structured document type"

# Clean up generated plans (removes all WORK_PLAN.md files)
clean-phase-plans:
    find .claude/.plan -name "WORK_PLAN.md" -delete 2>/dev/null || true
    @echo "Cleaned up generated phase plans"

# Run comprehensive tests on work plan generation
test-phase-plans:
    python3 scripts/test_workplan_generation.py -v

# Show help for phase plan generation
help-phase-plans:
    @echo "Phase Plan Generation Commands (v2):"
    @echo ""
    @echo "  create-phase-plan CONFIG_FILE      Generate narrative WORK_PLAN.md from JSON"
    @echo "  validate-phase-plan PLAN_FILE      Check work plan quality"
    @echo "  validate-phase-config CONFIG       Validate JSON and test generation"
    @echo "  test-phase-plans                   Run comprehensive test suite"
    @echo "  show-phase-config-example          Show example configuration format"
    @echo "  clean-phase-plans                  Remove all generated WORK_PLAN.md files"
    @echo ""
    @echo "Typical workflow:"
    @echo "  1. Review .claude/examples/phase-5-complete-config.json for reference"
    @echo "  2. Create phase-X-config.json with complete content specifications"
    @echo "  3. Run: just validate-phase-config phase-X-config.json"
    @echo "  4. Run: just create-phase-plan phase-X-config.json"
    @echo "  5. Review generated .claude/.plan/phase-X/WORK_PLAN.md"
    @echo ""
    @echo "Key differences in v2:"
    @echo "  - Complete content in JSON (no templates)"
    @echo "  - Generates narrative work plans (no TODOs)"
    @echo "  - Quality validation ensures professional output"