#!/usr/bin/env python3
"""
Validate Requirements Traceability
Ensures all requirements are properly traced through the spec to implementation details.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import json

class TraceabilityValidator:
    def __init__(self, spec_path: str):
        self.spec_path = Path(spec_path)
        self.spec_dir = self.spec_path.parent
        self.requirements = {
            "functional": {},
            "non_functional": {}
        }
        self.traces = {
            "to_architecture": {},
            "to_acceptance": {},
            "to_risks": {}
        }
        self.errors = []
        self.warnings = []
        
    def validate(self) -> bool:
        """Run traceability validation"""
        print(f"🔍 Validating requirements traceability in: {self.spec_path}")
        
        # Extract requirements
        self._extract_requirements()
        
        # Find traces
        self._find_architecture_traces()
        self._find_acceptance_traces()
        self._find_risk_traces()
        
        # Validate coverage
        self._validate_coverage()
        
        # Report results
        return self._report_results()
        
    def _extract_requirements(self):
        """Extract all requirements from spec"""
        print("\n📋 Extracting requirements...")
        
        with open(self.spec_path, 'r') as f:
            content = f.read()
            
        # Extract functional requirements
        fr_pattern = r'^#{3,4}\s+(FR-\d+)[:\s]+(.+?)(?=^#{1,4}|\Z)'
        for match in re.finditer(fr_pattern, content, re.MULTILINE | re.DOTALL):
            req_id = match.group(1)
            req_text = match.group(2).strip()
            self.requirements["functional"][req_id] = {
                "text": req_text.split('\n')[0],  # First line as summary
                "traced": False
            }
            
        # Extract non-functional requirements
        nfr_pattern = r'^#{3,4}\s+(NFR-\d+)[:\s]+(.+?)(?=^#{1,4}|\Z)'
        for match in re.finditer(nfr_pattern, content, re.MULTILINE | re.DOTALL):
            req_id = match.group(1)
            req_text = match.group(2).strip()
            self.requirements["non_functional"][req_id] = {
                "text": req_text.split('\n')[0],
                "traced": False
            }
            
        total_reqs = len(self.requirements["functional"]) + len(self.requirements["non_functional"])
        print(f"  Found {len(self.requirements['functional'])} functional requirements")
        print(f"  Found {len(self.requirements['non_functional'])} non-functional requirements")
        
    def _find_architecture_traces(self):
        """Find traces from requirements to architecture"""
        print("\n🏗️  Finding architecture traces...")
        
        with open(self.spec_path, 'r') as f:
            content = f.read()
            
        # Look for requirement references in architecture section
        arch_section = re.search(r'#{1,2}\s+System Architecture(.+?)(?=^#{1,2}|\Z)', 
                                content, re.MULTILINE | re.DOTALL)
        
        if arch_section:
            arch_content = arch_section.group(1)
            
            # Find all requirement references
            for req_type in ["functional", "non_functional"]:
                for req_id in self.requirements[req_type]:
                    if req_id in arch_content:
                        self.traces["to_architecture"][req_id] = True
                        self.requirements[req_type][req_id]["traced"] = True
                        print(f"  ✅ {req_id} traced to architecture")
                        
    def _find_acceptance_traces(self):
        """Find traces from requirements to acceptance scenarios"""
        print("\n🧪 Finding acceptance scenario traces...")
        
        # Check main spec
        with open(self.spec_path, 'r') as f:
            content = f.read()
            
        # Also check for acceptance scenarios file
        acceptance_files = [
            self.spec_path,
            self.spec_dir / ".spec" / "acceptance-scenarios.md",
            self.spec_dir / "requirements" / "acceptance-scenarios.md"
        ]
        
        all_content = ""
        for file_path in acceptance_files:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    all_content += f.read() + "\n"
                    
        # Find requirement references in scenarios
        for req_type in ["functional", "non_functional"]:
            for req_id in self.requirements[req_type]:
                if req_id in all_content:
                    self.traces["to_acceptance"][req_id] = True
                    print(f"  ✅ {req_id} has acceptance scenarios")
                    
    def _find_risk_traces(self):
        """Find traces from requirements to risks"""
        print("\n⚠️  Finding risk traces...")
        
        with open(self.spec_path, 'r') as f:
            content = f.read()
            
        # Look for requirement references in risks section
        risk_section = re.search(r'#{1,2}\s+Risk(.+?)(?=^#{1,2}|\Z)', 
                               content, re.MULTILINE | re.DOTALL)
        
        if risk_section:
            risk_content = risk_section.group(1)
            
            # High-risk requirements should be in risk section
            high_risk_keywords = ["real-time", "performance", "security", "integration"]
            
            for req_type in ["functional", "non_functional"]:
                for req_id, req_data in self.requirements[req_type].items():
                    # Check if requirement text contains high-risk keywords
                    req_text_lower = req_data["text"].lower()
                    is_high_risk = any(keyword in req_text_lower for keyword in high_risk_keywords)
                    
                    if is_high_risk:
                        if req_id in risk_content:
                            self.traces["to_risks"][req_id] = True
                            print(f"  ✅ High-risk {req_id} addressed in risks")
                        else:
                            self.warnings.append(f"High-risk requirement {req_id} not addressed in risk section")
                            
    def _validate_coverage(self):
        """Validate traceability coverage"""
        print("\n📊 Validating coverage...")
        
        # Check functional requirements coverage
        for req_id, req_data in self.requirements["functional"].items():
            if not req_data["traced"]:
                self.errors.append(f"Functional requirement {req_id} not traced to architecture")
                
            if req_id not in self.traces["to_acceptance"]:
                self.warnings.append(f"Functional requirement {req_id} lacks acceptance scenarios")
                
        # Check non-functional requirements coverage
        for req_id, req_data in self.requirements["non_functional"].items():
            if not req_data["traced"]:
                self.warnings.append(f"Non-functional requirement {req_id} not explicitly traced")
                
    def _report_results(self) -> bool:
        """Generate traceability report"""
        print("\n" + "="*60)
        print("REQUIREMENTS TRACEABILITY REPORT")
        print("="*60)
        
        # Summary statistics
        total_reqs = len(self.requirements["functional"]) + len(self.requirements["non_functional"])
        traced_to_arch = len(self.traces["to_architecture"])
        traced_to_accept = len(self.traces["to_acceptance"])
        traced_to_risk = len(self.traces["to_risks"])
        
        print(f"\n📊 Traceability Summary:")
        print(f"  Total requirements: {total_reqs}")
        print(f"  Traced to architecture: {traced_to_arch} ({traced_to_arch/max(total_reqs,1)*100:.0f}%)")
        print(f"  Have acceptance scenarios: {traced_to_accept} ({traced_to_accept/max(total_reqs,1)*100:.0f}%)")
        print(f"  High-risk addressed: {traced_to_risk}")
        
        # Errors and warnings
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
                
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
                
        # Traceability matrix
        print("\n📋 Traceability Matrix:")
        print("  Requirement | Architecture | Acceptance | Risk")
        print("  " + "-"*50)
        
        all_reqs = []
        for req_type in ["functional", "non_functional"]:
            all_reqs.extend(self.requirements[req_type].keys())
            
        for req_id in sorted(all_reqs):
            arch = "✅" if req_id in self.traces["to_architecture"] else "❌"
            accept = "✅" if req_id in self.traces["to_acceptance"] else "❌"
            risk = "✅" if req_id in self.traces["to_risks"] else "N/A"
            print(f"  {req_id:10} | {arch:12} | {accept:10} | {risk}")
            
        # Save detailed report
        report_path = self.spec_path.parent / "requirements-traceability.json"
        report_data = {
            "requirements": self.requirements,
            "traces": self.traces,
            "errors": self.errors,
            "warnings": self.warnings,
            "summary": {
                "total_requirements": total_reqs,
                "traced_to_architecture": traced_to_arch,
                "have_acceptance_scenarios": traced_to_accept,
                "high_risk_addressed": traced_to_risk
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: {report_path}")
        print("="*60)
        
        # Return True if no critical errors
        return len(self.errors) == 0

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python validate-requirements-traceability.py <path-to-SPEC.md>")
        sys.exit(1)
        
    spec_path = sys.argv[1]
    validator = TraceabilityValidator(spec_path)
    
    if validator.validate():
        print("\n✅ Requirements traceability validation PASSED")
        sys.exit(0)
    else:
        print("\n❌ Requirements traceability validation FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()