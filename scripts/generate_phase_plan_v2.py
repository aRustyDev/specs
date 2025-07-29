#!/usr/bin/env python3
"""
Narrative Document Generator - Transform JSON specs into professional documentation

This script generates complete, narrative documents from structured JSON configurations.
It uses an algorithmic approach (no LLM/AI) to transform data into readable markdown.

Core Concept:
    JSON Config (complete content) → Python Processing → Markdown Document

Usage:
    python3 scripts/generate_phase_plan_v2.py path/to/config.json [output_dir]

Features:
    - Transforms structured data into natural narrative flow
    - Generates professional markdown with consistent formatting
    - No templates or placeholders - all content comes from config
    - Extensible to any document type (plans, reviews, guides, etc.)

How it works:
    1. Loads JSON configuration with complete content
    2. Validates required sections exist
    3. Processes each section through specialized generators
    4. Outputs formatted markdown document
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class NarrativeWorkPlanGenerator:
    """
    Transforms JSON configurations into narrative markdown documents.
    
    This class implements a section-based approach where each document
    section has its own generator method. The class is designed to be
    subclassed for different document types.
    
    Architecture:
        - load_config(): Validates and loads JSON input
        - generate_*(): Section-specific generators that format content
        - add_line(): Helper for building markdown with proper spacing
        - generate_plan(): Orchestrates the document generation
    
    To adapt for other document types:
        1. Subclass this generator
        2. Override section generators as needed
        3. Modify required_sections in load_config()
        4. Add new generator methods for new sections
    """
    
    def __init__(self):
        """Initialize the generator with empty config and output buffer."""
        self.config: Dict[str, Any] = {}
        self.output_lines: List[str] = []
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load and validate JSON configuration file.
        
        The config file must contain all content to be included in the
        generated document. No content is generated - only formatted.
        
        Args:
            config_path: Path to JSON configuration file
            
        Returns:
            Loaded configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If JSON is invalid or required sections missing
        """
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        
        # Define required sections for this document type
        # Override in subclasses for different document types
        required_sections = ['phase', 'prerequisites', 'resources', 'overview', 
                           'methodology', 'done_criteria', 'work_breakdown']
        
        # Validate all required sections exist
        missing_sections = [s for s in required_sections if s not in self.config]
        if missing_sections:
            raise ValueError(f"Missing required sections: {', '.join(missing_sections)}")
        
        return self.config
    
    def add_line(self, content: str = "", level: int = 0) -> None:
        """
        Add a line to the output with optional indentation.
        
        This is the core method for building the markdown document.
        It handles proper indentation for nested content.
        
        Args:
            content: The text to add (empty string for blank line)
            level: Indentation level (number of 2-space indents)
        """
        if level > 0:
            content = "  " * level + content
        self.output_lines.append(content)
    
    def add_section_break(self) -> None:
        """Add a blank line for visual separation between sections."""
        self.add_line()
    
    def generate_header(self) -> None:
        """
        Generate the main document header.
        
        Creates the H1 title using phase information.
        Override this method to change document title format.
        """
        phase = self.config['phase']
        self.add_line(f"# Phase {phase['number']}: {phase['title']} - Work Plan")
        self.add_section_break()
        
    def generate_prerequisites(self) -> None:
        """Generate prerequisites section with narrative flow."""
        prereq = self.config['prerequisites']
        
        self.add_line("## Prerequisites")
        self.add_section_break()
        self.add_line(prereq['intro_narrative'])
        
        # Completed phases
        if prereq.get('completed_phases'):
            self.add_line(f"- **Completed Phases**: {prereq['completed_phases']['required']} - "
                         f"{prereq['completed_phases']['descriptions']}")
        
        # Knowledge areas
        self.add_line("- **Required Knowledge**:")
        for area in prereq['knowledge_areas']:
            self.add_line(f"  - **{area['area']}**: {area['description']} "
                         f"(*{area['importance']}*)", level=1)
        
        self.add_section_break()
        
    def generate_resources(self) -> None:
        """Generate resources section with descriptions."""
        resources = self.config['resources']
        
        self.add_line("## Quick Reference - Essential Resources")
        self.add_section_break()
        self.add_line(resources['intro_narrative'])
        self.add_section_break()
        
        # Example files
        self.add_line("### Example Files")
        if resources['example_files']:
            # Extract directory from first file path
            first_path = Path(resources['example_files'][0]['path'])
            example_dir = str(first_path.parent)
            self.add_line(f"All example files are located in `{example_dir}/`:")
        for example in resources['example_files']:
            self.add_line(f"- **[{example['name']}]({example['path']})** - "
                         f"{example['description']} - {example['purpose']}")
        
        self.add_section_break()
        
        # Specifications
        self.add_line("### Specification Documents")
        self.add_line("Key specifications for this phase:")
        for spec in resources['specifications']:
            self.add_line(f"- **[{spec['name']}]({spec['path']})** - {spec['description']}")
            if spec.get('key_sections'):
                sections = ", ".join(spec['key_sections'])
                self.add_line(f"  - Key sections: {sections}", level=1)
        
        self.add_section_break()
        
        # Junior developer guides
        self.add_line("### Junior Developer Resources")
        self.add_line("Additional learning resources organized by when you'll need them:")
        for guide in resources['junior_dev_guides']:
            self.add_line(f"- **[{guide['name']}]({guide['path']})** - "
                         f"{guide['description']}")
            self.add_line(f"  - *When to read*: {guide['when_to_read']}", level=1)
        
        self.add_section_break()
        
        # Quick links
        self.add_line("### Quick Links")
        for link in resources['quick_links']:
            self.add_line(f"- **{link['name']}**: `{link['command']}` - "
                         f"{link['purpose']}")
        
        self.add_section_break()
        
    def generate_overview(self) -> None:
        """Generate overview section."""
        overview = self.config['overview']
        
        self.add_line("## Overview")
        self.add_section_break()
        self.add_line(overview['narrative'])
        self.add_section_break()
        self.add_line(f"**Checkpoint Strategy**: {overview['checkpoint_summary']}")
        self.add_section_break()
        self.add_line(f"**Time Estimate**: {overview['time_estimate']}")
        self.add_section_break()
        
    def generate_build_commands(self) -> None:
        """Generate build commands section."""
        if 'build_commands' not in self.config:
            return
            
        build = self.config['build_commands']
        
        self.add_line("## Build and Test Commands")
        self.add_section_break()
        self.add_line(build['intro_narrative'])
        
        for cmd in build['commands']:
            self.add_line(f"- `{build['tool']} {cmd['command']}` - "
                         f"{cmd['description']} ({cmd['when_to_use']})")
        
        self.add_section_break()
        
    def generate_review_process(self) -> None:
        """Generate review process section."""
        if 'review_process' not in self.config:
            return
            
        review = self.config['review_process']
        
        self.add_line("## IMPORTANT: Review Process")
        self.add_section_break()
        self.add_line(f"**{review['importance_narrative']}**")
        self.add_section_break()
        
        self.add_line(f"At each of the {review['checkpoint_count']} checkpoints:")
        self.add_line(f"1. **{review['checkpoint_procedure']['stop_instructions']}**")
        self.add_line("2. **Request external review** by:")
        for step in review['checkpoint_procedure']['review_preparation']:
            self.add_line(f"   - {step}")
        self.add_line(f"3. **{review['checkpoint_procedure']['wait_instructions']}**")
        
        self.add_section_break()
        
    def generate_methodology(self) -> None:
        """Generate development methodology section."""
        methodology = self.config['methodology']
        
        self.add_line(f"## Development Methodology: {methodology['approach']}")
        self.add_section_break()
        self.add_line(f"**IMPORTANT**: {methodology['importance_narrative']}")
        self.add_section_break()
        
        for i, rule in enumerate(methodology['rules'], 1):
            self.add_line(f"{i}. **{rule['step']}** - {rule['description']}")
            self.add_line(f"   - *{rule['rationale']}*", level=1)
        
        self.add_section_break()
        
    def generate_done_criteria(self) -> None:
        """Generate done criteria checklist."""
        done = self.config['done_criteria']
        
        self.add_line("## Done Criteria Checklist")
        self.add_section_break()
        self.add_line(done['intro_narrative'])
        
        for criterion in done['checklist']:
            self.add_line(f"- [ ] {criterion['criterion']}")
            self.add_line(f"  - *Verification*: {criterion['verification_method']}", level=1)
        
        self.add_section_break()
        
    def generate_work_breakdown(self) -> None:
        """Generate detailed work breakdown sections."""
        self.add_line("## Work Breakdown with Review Checkpoints")
        self.add_section_break()
        
        for section in self.config['work_breakdown']:
            self.generate_work_section(section)
            
    def generate_work_section(self, section: Dict[str, Any]) -> None:
        """Generate a single work section with all details."""
        # Section header
        self.add_line(f"### {section['section_number']} {section['title']} "
                     f"({section['work_unit_context']['scope']['estimated_lines']}, "
                     f"{section['work_unit_context']['scope']['file_count']})")
        self.add_section_break()
        
        # Work unit context
        context = section['work_unit_context']
        self.add_line("**Work Unit Context:**")
        self.add_line(f"- **Complexity**: {context['complexity']} - "
                     f"{context['complexity_reason']}")
        self.add_line(f"- **Scope**: {context['scope']['estimated_lines']} across "
                     f"{context['scope']['file_count']}")
        self.add_line("- **Key Components**:")
        
        for component in context['key_components']:
            self.add_line(f"  - {component['name']} ({component['estimated_lines']}) - "
                         f"{component['purpose']}")
        
        if context.get('patterns'):
            self.add_line(f"- **Patterns**: {', '.join(context['patterns'])}")
        
        if context.get('algorithms'):
            self.add_line(f"- **Required Algorithms**: {', '.join(context['algorithms'])}")
        
        self.add_section_break()
        
        # Tasks
        for task in section['tasks']:
            self.generate_task(task)
        
        # Checkpoint
        if 'checkpoint' in section:
            self.generate_checkpoint(section['checkpoint'])
            
    def generate_task(self, task: Dict[str, Any]) -> None:
        """Generate a single task with full details."""
        self.add_line(f"#### Task {task['number']}: {task['title']}")
        self.add_section_break()
        
        # Tips/warnings before description
        for tip in task.get('tips', []):
            icon = {'junior_dev': '💡', 'warning': '⚠️', 
                   'security': '🔒', 'performance': '⚡'}[tip['type']]
            self.add_line(f"{icon} **{tip['type'].replace('_', ' ').title()} Tip**: "
                         f"{tip['content']}")
            if tip.get('resource_link'):
                self.add_line(f"   See: [{tip['resource_link']}]({tip['resource_link']})")
            self.add_line()
        
        # Task description
        self.add_line(task['description'])
        self.add_section_break()
        
        # TDD instructions if present
        if task.get('tdd_instructions'):
            self.add_line(f"**TDD Approach**: {task['tdd_instructions']}")
            self.add_section_break()
        
        # Code examples
        for example in task.get('code_examples', []):
            self.add_line(f"**{example['purpose']}:**")
            self.add_line(f"```{example['language']}")
            self.add_line(example['code'])
            self.add_line("```")
            self.add_line()
            self.add_line(f"*{example['explanation']}*")
            self.add_section_break()
        
        # Special considerations
        if task.get('special_considerations'):
            self.add_line("**Special Considerations:**")
            for consideration in task['special_considerations']:
                self.add_line(f"- {consideration}")
            self.add_section_break()
            
    def generate_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        """Generate checkpoint section."""
        self.add_line(f"---")
        self.add_section_break()
        self.add_line(f"### {checkpoint['stop_message']}")
        self.add_section_break()
        
        # Deliverables
        self.add_line("**Deliverables:**")
        for deliverable in checkpoint['deliverables']:
            self.add_line(f"- {deliverable}")
        self.add_section_break()
        
        # Verification steps
        self.add_line("**Verification Steps:**")
        for i, step in enumerate(checkpoint['verification_steps'], 1):
            self.add_line(f"{i}. {step}")
        self.add_section_break()
        
        # Common issues
        if checkpoint.get('common_issues'):
            self.add_line("**Common Issues:**")
            for issue in checkpoint['common_issues']:
                self.add_line(f"- **Issue**: {issue['issue']}")
                self.add_line(f"  **Solution**: {issue['solution']}")
            self.add_section_break()
        
        self.add_line("**DO NOT PROCEED** until review is complete and approved.")
        self.add_section_break()
        self.add_line(f"---")
        self.add_section_break()
        
    def generate_troubleshooting(self) -> None:
        """Generate troubleshooting section."""
        if 'troubleshooting' not in self.config:
            return
            
        trouble = self.config['troubleshooting']
        
        self.add_line("## Troubleshooting")
        self.add_section_break()
        self.add_line(trouble['intro_narrative'])
        self.add_section_break()
        
        for category in trouble['common_issues']:
            self.add_line(f"### {category['category']}")
            for issue in category['issues']:
                self.add_line(f"- **Symptom**: {issue['symptom']}")
                self.add_line(f"  - **Cause**: {issue['cause']}", level=1)
                self.add_line(f"  - **Solution**: {issue['solution']}", level=1)
            self.add_section_break()
        
        # Escalation path
        if trouble.get('escalation_path'):
            self.add_line("### Escalation Path")
            self.add_line(trouble['escalation_path']['when_stuck'])
            self.add_line("**Documentation Requirements:**")
            for req in trouble['escalation_path']['documentation_requirements']:
                self.add_line(f"- {req}")
            self.add_section_break()
            
    def generate_security_requirements(self) -> None:
        """Generate security requirements section."""
        if 'security_requirements' not in self.config:
            return
            
        security = self.config['security_requirements']
        
        self.add_line("## Security Requirements")
        self.add_section_break()
        self.add_line(f"**{security['importance_narrative']}**")
        self.add_section_break()
        
        for category in security['categories']:
            self.add_line(f"### {category['name']}")
            
            # Requirements
            for req in category['requirements']:
                self.add_line(f"- **{req['type']}**: {req['requirement']}")
                if req.get('rationale'):
                    self.add_line(f"  - *Rationale*: {req['rationale']}", level=1)
            
            # Implementation guidance
            if category.get('implementation_guidance'):
                self.add_line()
                self.add_line(f"**Implementation**: {category['implementation_guidance']}")
            
            # Testing approach
            if category.get('testing_approach'):
                self.add_line(f"**Testing**: {category['testing_approach']}")
            
            self.add_section_break()
            
    def generate_learning_path(self) -> None:
        """Generate junior developer learning path."""
        if 'learning_path' not in self.config:
            return
            
        learning = self.config['learning_path']
        
        self.add_line("## Junior Developer Learning Path")
        self.add_section_break()
        self.add_line(f"**Target Audience**: {learning['target_audience']}")
        self.add_line()
        self.add_line(learning['intro_narrative'])
        self.add_section_break()
        
        # Learning progression
        for step in learning['progression']:
            self.add_line(f"### Step {step['step']}: {step['focus']}")
            self.add_line(f"- **Resources**: {', '.join(step['resources'])}")
            self.add_line(f"- **Time**: {step['estimated_time']}")
            self.add_line(f"- **Practice**: {step['practical_exercise']}")
            self.add_section_break()
        
        # Key warnings
        if learning.get('key_warnings'):
            self.add_line("### Remember:")
            for warning in learning['key_warnings']:
                self.add_line(f"- ⚠️ {warning}")
            self.add_section_break()
            
    def generate_next_phase(self) -> None:
        """Generate next phase preview."""
        if 'next_phase' not in self.config:
            return
            
        next_phase = self.config['next_phase']
        
        self.add_line("## Next Phase Preview")
        self.add_section_break()
        self.add_line(f"### Phase {next_phase['number']}: {next_phase['title']}")
        self.add_line()
        self.add_line(next_phase['preview_narrative'])
        
        if next_phase.get('key_features'):
            self.add_line()
            self.add_line("**Key Features:**")
            for feature in next_phase['key_features']:
                self.add_line(f"- {feature}")
        
        self.add_section_break()
        
    def generate_footer(self) -> None:
        """Generate document footer."""
        self.add_line("---")
        self.add_line()
        self.add_line(f"*Generated on {datetime.now().strftime('%Y-%m-%d')} "
                     f"by Phase Plan Generator v2*")
        
    def ensure_output_directory(self, phase_number: int, 
                              project_root: Optional[str] = None) -> Path:
        """Create output directory if it doesn't exist."""
        if project_root is None:
            project_root = Path.cwd()
        else:
            project_root = Path(project_root)
        
        output_dir = project_root / ".claude" / ".plan" / f"phase-{phase_number}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        return output_dir
        
    def generate_plan(self, config_path: str, 
                     project_root: Optional[str] = None) -> str:
        """Main method: Generate complete narrative WORK_PLAN.md."""
        # Load configuration
        self.load_config(config_path)
        
        # Clear output
        self.output_lines = []
        
        # Generate all sections in order
        self.generate_header()
        self.generate_prerequisites()
        self.generate_resources()
        self.generate_overview()
        self.generate_build_commands()
        self.generate_review_process()
        self.generate_methodology()
        self.generate_done_criteria()
        self.generate_work_breakdown()
        self.generate_troubleshooting()
        self.generate_security_requirements()
        self.generate_learning_path()
        self.generate_next_phase()
        self.generate_footer()
        
        # Determine output location
        phase_number = self.config['phase']['number']
        output_dir = self.ensure_output_directory(phase_number, project_root)
        output_file = output_dir / "WORK_PLAN.md"
        
        # Write output file
        content = '\n'.join(self.output_lines)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_file)


def main():
    """
    Command-line interface entry point.
    
    Parses arguments and runs the generator.
    Provides helpful usage information if arguments missing.
    """
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/generate_phase_plan_v2.py <config.json> [output_dir]", 
              file=sys.stderr)
        print("", file=sys.stderr)
        print("This script generates narrative documents from JSON configurations.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Arguments:", file=sys.stderr)
        print("  config.json  - Path to JSON configuration with complete content", file=sys.stderr)
        print("  output_dir   - Optional output directory (defaults to current dir)", file=sys.stderr)
        print("", file=sys.stderr)
        print("Example:", file=sys.stderr)
        print("  python3 scripts/generate_phase_plan_v2.py phase-5-config.json ./output", file=sys.stderr)
        print("", file=sys.stderr)
        print("See .claude/examples/phase-5-complete-config.json for a complete example.", file=sys.stderr)
        sys.exit(1)
    
    config_path = sys.argv[1]
    project_root = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        generator = NarrativeWorkPlanGenerator()
        output_file = generator.generate_plan(config_path, project_root)
        print(f"Generated narrative work plan: {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()