#!/usr/bin/env python3
"""
Validate Alignment Between Documents
Ensures SPEC, roadmap, and phase plans are properly aligned.
"""

import os
import sys
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple

class AlignmentValidator:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.spec_path = self.project_dir / "spec" / "SPEC.md"
        self.roadmap_path = self.project_dir / "roadmap" / "*roadmap*.md"
        self.phase_plans_dir = self.project_dir / "phase-plans"
        
        self.spec_data = {}
        self.roadmap_data = {}
        self.phase_plans = {}
        
        self.errors = []
        self.warnings = []
        
    def validate(self) -> bool:
        """Run alignment validation"""
        print(f"🔄 Validating document alignment in: {self.project_dir}")
        
        # Check if required files exist
        if not self._check_files_exist():
            return False
            
        # Extract data from each document type
        self._extract_spec_data()
        self._extract_roadmap_data()
        self._extract_phase_plan_data()
        
        # Validate alignments
        self._validate_spec_to_roadmap()
        self._validate_roadmap_to_phases()
        self._validate_tech_stack_consistency()
        self._validate_timeline_consistency()
        self._validate_resource_consistency()
        
        # Report results
        return self._report_results()
        
    def _check_files_exist(self) -> bool:
        """Check if required files exist"""
        print("\n📁 Checking for required files...")
        
        if not self.spec_path.exists():
            # Try alternative location
            self.spec_path = self.project_dir / "SPEC.md"
            if not self.spec_path.exists():
                self.errors.append(f"SPEC.md not found in {self.project_dir}")
                return False
                
        # Find roadmap file
        roadmap_files = list(self.project_dir.glob("**/roadmap*.md"))
        if not roadmap_files:
            self.errors.append("No roadmap file found")
            return False
        self.roadmap_path = roadmap_files[0]
        
        # Check for phase plans
        if not self.phase_plans_dir.exists():
            self.warnings.append("No phase-plans directory found")
            
        print(f"  ✅ Found SPEC: {self.spec_path.name}")
        print(f"  ✅ Found Roadmap: {self.roadmap_path.name}")
        
        return True
        
    def _extract_spec_data(self):
        """Extract key data from SPEC"""
        print("\n📋 Extracting SPEC data...")
        
        with open(self.spec_path, 'r') as f:
            content = f.read()
            
        # Extract requirements
        self.spec_data["requirements"] = {
            "functional": re.findall(r'FR-\d+[:\s]+([^\n]+)', content),
            "non_functional": re.findall(r'NFR-\d+[:\s]+([^\n]+)', content)
        }
        
        # Extract tech stack
        tech_section = re.search(r'Technology Stack(.+?)(?=^#{1,3}|\Z)', 
                                content, re.MULTILINE | re.DOTALL)
        if tech_section:
            self.spec_data["tech_stack"] = {
                "frontend": re.findall(r'Frontend.*?:\s*([^\n]+)', tech_section.group(1)),
                "backend": re.findall(r'Backend.*?:\s*([^\n]+)', tech_section.group(1)),
                "database": re.findall(r'Database.*?:\s*([^\n]+)', tech_section.group(1))
            }
            
        # Extract timeline
        timeline_matches = re.findall(r'(\d+)\s*(months?|weeks?)', content, re.IGNORECASE)
        if timeline_matches:
            self.spec_data["timeline"] = timeline_matches[0]
            
        # Extract team size
        team_matches = re.findall(r'(\d+)\s*(developers?|engineers?|people)', content, re.IGNORECASE)
        if team_matches:
            self.spec_data["team_size"] = team_matches[0]
            
    def _extract_roadmap_data(self):
        """Extract key data from roadmap"""
        print("\n🗺️  Extracting roadmap data...")
        
        with open(self.roadmap_path, 'r') as f:
            content = f.read()
            
        # Extract phases
        phase_pattern = r'Phase\s+(\d+)[:\s]+([^\n]+)'
        phases = re.findall(phase_pattern, content, re.IGNORECASE)
        self.roadmap_data["phases"] = phases
        
        # Extract deliverables per phase
        self.roadmap_data["deliverables"] = {}
        for phase_num, phase_name in phases:
            # Find deliverables for this phase
            phase_section = re.search(
                rf'Phase\s+{phase_num}.*?(?=Phase\s+\d+|$)', 
                content, re.DOTALL | re.IGNORECASE
            )
            if phase_section:
                deliverables = re.findall(r'(?:Delivers|Outcomes?):\s*([^\n]+)', 
                                        phase_section.group(0))
                self.roadmap_data["deliverables"][f"Phase {phase_num}"] = deliverables
                
    def _extract_phase_plan_data(self):
        """Extract data from phase plans"""
        print("\n📅 Extracting phase plan data...")
        
        if not self.phase_plans_dir.exists():
            return
            
        for plan_file in self.phase_plans_dir.glob("*.yml"):
            with open(plan_file, 'r') as f:
                try:
                    plan_data = yaml.safe_load(f)
                    phase_num = plan_data.get('metadata', {}).get('phase', 'unknown')
                    self.phase_plans[f"Phase {phase_num}"] = {
                        "objectives": plan_data.get('objectives', {}).get('primary', []),
                        "team_size": plan_data.get('metadata', {}).get('team_size', 0),
                        "duration": plan_data.get('metadata', {}).get('duration_weeks', 0),
                        "tech": self._extract_tech_from_plan(plan_data)
                    }
                except yaml.YAMLError as e:
                    self.warnings.append(f"Could not parse {plan_file.name}: {e}")
                    
    def _extract_tech_from_plan(self, plan_data: dict) -> dict:
        """Extract technology mentions from plan"""
        tech = {}
        tech_req = plan_data.get('technical_requirements', {})
        
        if 'backend' in tech_req:
            tech['backend'] = tech_req['backend']
        if 'frontend' in tech_req:
            tech['frontend'] = tech_req['frontend']
            
        return tech
        
    def _validate_spec_to_roadmap(self):
        """Validate SPEC requirements are in roadmap"""
        print("\n🔍 Validating SPEC → Roadmap alignment...")
        
        # Check if all requirements are addressed in phases
        all_requirements = (
            self.spec_data.get("requirements", {}).get("functional", []) +
            self.spec_data.get("requirements", {}).get("non_functional", [])
        )
        
        roadmap_content = ""
        with open(self.roadmap_path, 'r') as f:
            roadmap_content = f.read().lower()
            
        untraced_reqs = []
        for req in all_requirements[:5]:  # Check first 5 requirements
            req_keywords = req.lower().split()[:3]  # First 3 words
            if not any(keyword in roadmap_content for keyword in req_keywords):
                untraced_reqs.append(req[:50] + "...")
                
        if untraced_reqs:
            self.warnings.append(
                f"Some requirements may not be in roadmap: {', '.join(untraced_reqs[:3])}"
            )
            
    def _validate_roadmap_to_phases(self):
        """Validate roadmap phases have phase plans"""
        print("\n🔍 Validating Roadmap → Phase Plans alignment...")
        
        for phase_info in self.roadmap_data.get("phases", []):
            phase_key = f"Phase {phase_info[0]}"
            if phase_key not in self.phase_plans:
                self.warnings.append(f"{phase_key} in roadmap but no phase plan found")
            else:
                print(f"  ✅ {phase_key} has phase plan")
                
    def _validate_tech_stack_consistency(self):
        """Validate tech stack is consistent across documents"""
        print("\n💻 Validating technology stack consistency...")
        
        spec_tech = self.spec_data.get("tech_stack", {})
        
        # Check phase plans use same tech
        for phase_name, phase_data in self.phase_plans.items():
            phase_tech = phase_data.get("tech", {})
            
            for tech_type in ["frontend", "backend"]:
                if tech_type in spec_tech and tech_type in phase_tech:
                    spec_items = spec_tech[tech_type]
                    phase_items = phase_tech[tech_type]
                    
                    # Simple consistency check
                    if isinstance(spec_items, list) and isinstance(phase_items, list):
                        if not any(item in str(phase_items) for item in spec_items):
                            self.warnings.append(
                                f"{phase_name} uses different {tech_type} tech than SPEC"
                            )
                            
    def _validate_timeline_consistency(self):
        """Validate timeline consistency"""
        print("\n⏰ Validating timeline consistency...")
        
        # Sum phase durations
        total_weeks = sum(
            plan.get("duration", 0) 
            for plan in self.phase_plans.values()
        )
        
        if self.spec_data.get("timeline"):
            spec_time, spec_unit = self.spec_data["timeline"]
            spec_weeks = int(spec_time) * (4 if "month" in spec_unit else 1)
            
            if abs(total_weeks - spec_weeks) > 2:  # Allow 2 week variance
                self.warnings.append(
                    f"Timeline mismatch: SPEC says {spec_time} {spec_unit}, "
                    f"phases total {total_weeks} weeks"
                )
            else:
                print(f"  ✅ Timeline aligned: ~{spec_weeks} weeks")
                
    def _validate_resource_consistency(self):
        """Validate resource allocation consistency"""
        print("\n👥 Validating resource consistency...")
        
        if self.spec_data.get("team_size"):
            spec_team = int(self.spec_data["team_size"][0])
            
            # Check phase plans
            for phase_name, phase_data in self.phase_plans.items():
                phase_team = phase_data.get("team_size", 0)
                if phase_team > spec_team:
                    self.warnings.append(
                        f"{phase_name} requires {phase_team} people but "
                        f"SPEC only mentions {spec_team}"
                    )
                    
    def _report_results(self) -> bool:
        """Generate alignment report"""
        print("\n" + "="*60)
        print("ALIGNMENT VALIDATION REPORT")
        print("="*60)
        
        # Summary
        print("\n📊 Alignment Summary:")
        print(f"  Documents analyzed: SPEC, Roadmap, {len(self.phase_plans)} phase plans")
        print(f"  Errors found: {len(self.errors)}")
        print(f"  Warnings found: {len(self.warnings)}")
        
        # Errors
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
                
        # Warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
                
        # Alignment matrix
        print("\n📋 Alignment Matrix:")
        print("  " + "-"*50)
        print("  Component     | SPEC | Roadmap | Phase Plans")
        print("  " + "-"*50)
        
        components = ["Requirements", "Tech Stack", "Timeline", "Resources"]
        for component in components:
            spec_check = "✅" if component.lower() in str(self.spec_data) else "❌"
            roadmap_check = "✅" if component.lower() in str(self.roadmap_data) else "⚠️"
            phase_check = "✅" if self.phase_plans else "❌"
            print(f"  {component:12} | {spec_check:4} | {roadmap_check:7} | {phase_check}")
            
        # Save report
        report_path = self.project_dir / "alignment-validation-report.json"
        report_data = {
            "project_dir": str(self.project_dir),
            "documents_found": {
                "spec": str(self.spec_path),
                "roadmap": str(self.roadmap_path),
                "phase_plans": len(self.phase_plans)
            },
            "errors": self.errors,
            "warnings": self.warnings,
            "extracted_data": {
                "spec": self.spec_data,
                "roadmap": self.roadmap_data,
                "phase_plans": self.phase_plans
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: {report_path}")
        print("="*60)
        
        # Success if no critical errors
        if not self.errors and len(self.warnings) < 5:
            print("\n✅ Documents are well-aligned")
            return True
        else:
            print("\n⚠️  Alignment issues found - review warnings")
            return len(self.errors) == 0

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python validate-alignment.py <project-directory>")
        print("Example: python validate-alignment.py ./example-project")
        sys.exit(1)
        
    project_dir = sys.argv[1]
    validator = AlignmentValidator(project_dir)
    
    if validator.validate():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()