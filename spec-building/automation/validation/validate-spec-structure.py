#!/usr/bin/env python3
"""
Validate spec structure and completeness.

This tool ensures specifications follow the required structure and contain
all necessary sections. It checks for:
- Required sections and subsections
- Proper markdown formatting
- No placeholder content (TODO, TBD, etc.)
- Consistent structure
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from automation.lib.base import SpecTool
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from lib.base import SpecTool

@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    level: str  # ERROR, WARNING, INFO
    category: str
    message: str
    line_number: Optional[int] = None

class SpecStructureValidator(SpecTool):
    """Validate spec structure and completeness."""
    
    VERSION = "2.0.0"
    DESCRIPTION = "Validate specification structure and completeness"
    
    # Required sections for a complete spec
    REQUIRED_SECTIONS = {
        "Executive Summary": [],
        "Stakeholders": [],
        "Requirements": ["Functional Requirements", "Non-Functional Requirements"],
        "System Architecture": ["High-Level Architecture", "Technology Stack"],
        "Risks and Mitigations": [],
        "Implementation Approach": ["Development Methodology", "Quality Standards"],
        "Success Metrics": ["Technical Metrics", "Business Metrics"],
        "Constraints and Assumptions": ["Constraints", "Assumptions"]
    }
    
    # Common placeholders to check
    PLACEHOLDERS = [
        r'\[(?:TODO|TBD|FIXME|XXX|PLACEHOLDER|TBC)\]',
        r'(?:TODO|TBD|FIXME)(?:\s*:|\s+)',
        r'\[(?:[Xx]+|\.{3}|___+)\]',
        r'<(?:TODO|TBD|PLACEHOLDER)>'
    ]
    
    def create_parser(self):
        parser = super().create_parser()
        parser.add_argument('spec_path',
                          help='Path to SPEC.md file')
        parser.add_argument('-q', '--quiet', action='store_true',
                          help='Only show errors')
        parser.add_argument('--no-warnings', action='store_true',
                          help='Suppress warnings')
        parser.add_argument('--check-links', action='store_true',
                          help='Also validate internal links')
        parser.add_argument('--strict', action='store_true',
                          help='Treat warnings as errors')
        return parser
    
    def get_examples(self):
        return """
Examples:
  # Basic validation
  %(prog)s spec/SPEC.md
  
  # Only show errors (quiet mode)
  %(prog)s spec/SPEC.md -q
  
  # Strict mode for CI/CD
  %(prog)s spec/SPEC.md --strict
  
  # Also check internal links
  %(prog)s spec/SPEC.md --check-links
"""
    
    def execute(self) -> int:
        # Load spec file
        spec_path = Path(self.args.spec_path)
        if not spec_path.exists():
            print(f"✗ Spec file not found: {spec_path}")
            return 1
        
        print(f"🔍 Validating spec structure at: {spec_path}\n")
        
        with open(spec_path, 'r') as f:
            self.content = f.read()
            self.lines = self.content.splitlines()
        
        # Run validations
        issues = []
        
        print("📋 Checking main SPEC.md structure...")
        issues.extend(self._check_required_sections())
        issues.extend(self._check_markdown_structure())
        
        print("\n🏷️  Checking for placeholders...")
        issues.extend(self._check_placeholders())
        
        if self.args.check_links:
            print("\n🔗 Checking internal links...")
            issues.extend(self._check_internal_links())
        
        # Check modular specs if directory exists
        spec_dir = spec_path.parent / ".spec"
        if not spec_dir.exists():
            spec_dir = spec_path.parent / "spec"
        
        if spec_dir.exists() and spec_dir.is_dir():
            print(f"\n📁 Checking modular spec files in {spec_dir.name}/...")
            issues.extend(self._check_modular_specs(spec_dir))
        
        # Report results
        self._report_results(issues)
        
        # Determine exit code
        errors = [i for i in issues if i.level == "ERROR"]
        warnings = [i for i in issues if i.level == "WARNING"]
        
        if errors or (self.args.strict and warnings):
            return 1
        return 0
    
    def _check_required_sections(self) -> List[ValidationIssue]:
        """Check for required sections and subsections."""
        issues = []
        
        # Extract all headings
        headings = {}
        current_h2 = None
        
        for i, line in enumerate(self.lines):
            if line.startswith("## "):
                current_h2 = line[3:].strip()
                headings[current_h2] = []
            elif line.startswith("### ") and current_h2:
                subsection = line[4:].strip()
                headings[current_h2].append(subsection)
        
        # Check required sections
        for section, subsections in self.REQUIRED_SECTIONS.items():
            if section not in headings:
                issues.append(ValidationIssue(
                    level="ERROR",
                    category="Structure",
                    message=f"Missing required section: {section}"
                ))
            else:
                # Check required subsections
                for subsection in subsections:
                    if subsection not in headings.get(section, []):
                        issues.append(ValidationIssue(
                            level="WARNING",
                            category="Structure",
                            message=f"Missing subsection '{subsection}' under '{section}'"
                        ))
        
        return issues
    
    def _check_markdown_structure(self) -> List[ValidationIssue]:
        """Check markdown formatting and structure."""
        issues = []
        
        # Check heading hierarchy
        prev_level = 0
        for i, line in enumerate(self.lines):
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                if level > prev_level + 1 and prev_level > 0:
                    issues.append(ValidationIssue(
                        level="WARNING",
                        category="Markdown",
                        message=f"Heading level skipped (from H{prev_level} to H{level})",
                        line_number=i + 1
                    ))
                prev_level = level
        
        # Check for empty sections
        for i in range(len(self.lines) - 1):
            if self.lines[i].startswith("#") and (
                i + 1 >= len(self.lines) or 
                (self.lines[i + 1].strip() == "" and 
                 (i + 2 >= len(self.lines) or self.lines[i + 2].startswith("#")))
            ):
                issues.append(ValidationIssue(
                    level="WARNING",
                    category="Content",
                    message=f"Empty section: {self.lines[i]}",
                    line_number=i + 1
                ))
        
        # Check for broken table formatting
        in_table = False
        for i, line in enumerate(self.lines):
            if "|" in line and not line.strip().startswith("|"):
                continue
            
            if line.strip().startswith("|"):
                if not in_table and i + 1 < len(self.lines):
                    next_line = self.lines[i + 1].strip()
                    if not re.match(r'^\|[\s\-:\|]+\|$', next_line):
                        issues.append(ValidationIssue(
                            level="WARNING",
                            category="Markdown",
                            message="Table missing separator line",
                            line_number=i + 1
                        ))
                in_table = True
            else:
                in_table = False
        
        return issues
    
    def _check_placeholders(self) -> List[ValidationIssue]:
        """Check for placeholder content."""
        issues = []
        
        for pattern in self.PLACEHOLDERS:
            for i, line in enumerate(self.lines):
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    issues.append(ValidationIssue(
                        level="WARNING",
                        category="Placeholder",
                        message=f"Found placeholder: {match.group()}",
                        line_number=i + 1
                    ))
        
        # Check for generic placeholder text
        generic_patterns = [
            r'Lorem ipsum',
            r'Insert .* here',
            r'Add .* here',
            r'Description goes here',
            r'Coming soon'
        ]
        
        for pattern in generic_patterns:
            for i, line in enumerate(self.lines):
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        level="WARNING",
                        category="Placeholder",
                        message=f"Found generic placeholder text",
                        line_number=i + 1
                    ))
        
        return issues
    
    def _check_internal_links(self) -> List[ValidationIssue]:
        """Check internal markdown links."""
        issues = []
        
        # Extract all heading anchors
        anchors = set()
        for line in self.lines:
            match = re.match(r'^#{1,6}\s+(.+)$', line)
            if match:
                # Convert heading to anchor format
                heading = match.group(1).strip()
                anchor = self._heading_to_anchor(heading)
                anchors.add(anchor)
        
        # Check all internal links
        link_pattern = r'\[([^\]]+)\]\(#([^)]+)\)'
        for i, line in enumerate(self.lines):
            for match in re.finditer(link_pattern, line):
                link_text = match.group(1)
                anchor = match.group(2)
                if anchor not in anchors:
                    issues.append(ValidationIssue(
                        level="ERROR",
                        category="Link",
                        message=f"Broken internal link: #{anchor}",
                        line_number=i + 1
                    ))
        
        return issues
    
    def _heading_to_anchor(self, heading: str) -> str:
        """Convert heading text to markdown anchor format."""
        # Remove markdown formatting
        anchor = re.sub(r'\*\*([^*]+)\*\*', r'\1', heading)
        anchor = re.sub(r'\*([^*]+)\*', r'\1', anchor)
        anchor = re.sub(r'`([^`]+)`', r'\1', anchor)
        
        # Convert to lowercase and replace spaces with hyphens
        anchor = anchor.lower()
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        anchor = re.sub(r'\s+', '-', anchor)
        
        return anchor
    
    def _check_modular_specs(self, spec_dir: Path) -> List[ValidationIssue]:
        """Check modular spec files."""
        issues = []
        
        spec_files = list(spec_dir.glob("*.md"))
        if not spec_files:
            issues.append(ValidationIssue(
                level="INFO",
                category="Modular",
                message=f"No modular spec files found in {spec_dir.name}/"
            ))
        else:
            for spec_file in spec_files:
                # Basic validation of modular specs
                with open(spec_file, 'r') as f:
                    content = f.read()
                
                if len(content.strip()) < 100:
                    issues.append(ValidationIssue(
                        level="WARNING",
                        category="Modular",
                        message=f"Modular spec seems too short: {spec_file.name}"
                    ))
                
                # Check for placeholders in modular specs
                for pattern in self.PLACEHOLDERS[:2]:  # Just check main patterns
                    if re.search(pattern, content, re.IGNORECASE):
                        issues.append(ValidationIssue(
                            level="WARNING",
                            category="Modular",
                            message=f"Placeholder found in {spec_file.name}"
                        ))
        
        return issues
    
    def _report_results(self, issues: List[ValidationIssue]):
        """Report validation results."""
        errors = [i for i in issues if i.level == "ERROR"]
        warnings = [i for i in issues if i.level == "WARNING"]
        infos = [i for i in issues if i.level == "INFO"]
        
        print("\n" + "=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60)
        
        if errors:
            print(f"\n❌ ERRORS ({len(errors)}):")
            for issue in errors:
                self._print_issue(issue)
        
        if warnings and not self.args.no_warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for issue in warnings:
                if not self.args.quiet:
                    self._print_issue(issue)
        
        if infos and not self.args.quiet:
            print(f"\nℹ️  INFO ({len(infos)}):")
            for issue in infos:
                self._print_issue(issue)
        
        print("\n" + "=" * 60)
        
        if not errors and not (self.args.strict and warnings):
            print("\n✅ Spec structure validation PASSED")
        else:
            print("\n❌ Spec structure validation FAILED")
    
    def _print_issue(self, issue: ValidationIssue):
        """Print a single issue."""
        location = f" (line {issue.line_number})" if issue.line_number else ""
        print(f"  - {issue.message}{location}")

def main():
    tool = SpecStructureValidator()
    sys.exit(tool.run())

if __name__ == '__main__':
    main()