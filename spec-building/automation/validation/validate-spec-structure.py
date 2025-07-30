#!/usr/bin/env python3
"""
Validate SPEC Structure
Ensures spec files follow the required structure and contain all mandatory sections.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Required sections in main SPEC.md
REQUIRED_SPEC_SECTIONS = [
    "Executive Summary",
    "Stakeholders", 
    "Requirements",
    "System Architecture",
    "Risks and Mitigations",
    "Implementation Approach",
    "Success Metrics",
    "Constraints and Assumptions"
]

# Required subsections
REQUIRED_SUBSECTIONS = {
    "Requirements": ["Functional Requirements", "Non-Functional Requirements"],
    "System Architecture": ["High-Level Architecture", "Technology Stack"],
    "Success Metrics": ["Technical Metrics", "Business Metrics"]
}

# Required files in .spec directory
REQUIRED_SPEC_FILES = [
    "outcomes.md",
    "requirements.md",
    "architecture.md",
    "risks.md"
]

class SpecValidator:
    def __init__(self, spec_path: str):
        self.spec_path = Path(spec_path)
        self.spec_dir = self.spec_path.parent / ".spec"
        self.errors = []
        self.warnings = []
        
    def validate(self) -> bool:
        """Run all validation checks"""
        print(f"🔍 Validating spec structure at: {self.spec_path}")
        
        # Check if SPEC.md exists
        if not self.spec_path.exists():
            self.errors.append(f"SPEC.md not found at {self.spec_path}")
            return False
            
        # Validate main spec structure
        self._validate_main_spec()
        
        # Validate modular spec files
        self._validate_modular_specs()
        
        # Check for placeholders
        self._check_placeholders()
        
        # Report results
        return self._report_results()
        
    def _validate_main_spec(self):
        """Validate main SPEC.md structure"""
        print("\n📋 Checking main SPEC.md structure...")
        
        with open(self.spec_path, 'r') as f:
            content = f.read()
            
        # Check for required sections
        for section in REQUIRED_SPEC_SECTIONS:
            pattern = rf'^#{1,3}\s+{re.escape(section)}'
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                self.errors.append(f"Missing required section: {section}")
            else:
                print(f"  ✅ Found section: {section}")
                
        # Check for required subsections
        for parent, subsections in REQUIRED_SUBSECTIONS.items():
            for subsection in subsections:
                pattern = rf'^#{2,4}\s+{re.escape(subsection)}'
                if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    self.warnings.append(f"Missing subsection '{subsection}' under '{parent}'")
                    
    def _validate_modular_specs(self):
        """Validate modular spec files in .spec directory"""
        print("\n📁 Checking modular spec files...")
        
        if not self.spec_dir.exists():
            self.warnings.append(".spec directory not found - modular specs not in use")
            return
            
        for required_file in REQUIRED_SPEC_FILES:
            file_path = self.spec_dir / required_file
            if not file_path.exists():
                self.warnings.append(f"Missing modular spec file: {required_file}")
            else:
                print(f"  ✅ Found: {required_file}")
                
    def _check_placeholders(self):
        """Check for TODO, TBD, FIXME placeholders"""
        print("\n🏷️  Checking for placeholders...")
        
        placeholder_patterns = ["TODO", "TBD", "FIXME", "XXX", "[PLACEHOLDER]"]
        files_to_check = [self.spec_path]
        
        if self.spec_dir.exists():
            files_to_check.extend(self.spec_dir.glob("*.md"))
            
        total_placeholders = 0
        for file_path in files_to_check:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                for pattern in placeholder_patterns:
                    matches = re.findall(rf'\b{pattern}\b', content, re.IGNORECASE)
                    count = len(matches)
                    if count > 0:
                        self.warnings.append(f"Found {count} '{pattern}' in {file_path.name}")
                        total_placeholders += count
                        
        if total_placeholders == 0:
            print("  ✅ No placeholders found")
            
    def _report_results(self) -> bool:
        """Report validation results"""
        print("\n" + "="*60)
        print("VALIDATION RESULTS")
        print("="*60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
                
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
                
        if not self.errors and not self.warnings:
            print("\n✅ All validation checks passed!")
            
        print("\n" + "="*60)
        
        # Return True only if no errors (warnings are acceptable)
        return len(self.errors) == 0

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python validate-spec-structure.py <path-to-SPEC.md>")
        sys.exit(1)
        
    spec_path = sys.argv[1]
    validator = SpecValidator(spec_path)
    
    if validator.validate():
        print("\n✅ Spec structure validation PASSED")
        sys.exit(0)
    else:
        print("\n❌ Spec structure validation FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()