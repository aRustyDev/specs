#!/usr/bin/env python3
"""
Run All Spec Validations
Comprehensive validation suite for spec quality.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

class ValidationRunner:
    def __init__(self, spec_path: str):
        self.spec_path = Path(spec_path).resolve()
        self.scripts_dir = Path(__file__).parent
        self.results = {}
        self.passed = 0
        self.failed = 0
        
    def run_all(self):
        """Run all validation scripts"""
        print("🚀 COMPREHENSIVE SPEC VALIDATION")
        print("="*60)
        print(f"Spec: {self.spec_path}")
        print(f"Scripts: {self.scripts_dir}")
        print("="*60)
        
        # Define validation scripts and their purposes
        validations = [
            {
                "name": "Structure Validation",
                "script": "validate-spec-structure.py",
                "description": "Checks required sections and format"
            },
            {
                "name": "Link Validation", 
                "script": "validate-spec-links.py",
                "description": "Verifies all internal links are valid"
            },
            {
                "name": "Quality Scoring",
                "script": "score-spec-quality.py",
                "description": "Calculates spec quality score (target: 90+)"
            },
            {
                "name": "Requirements Traceability",
                "script": "validate-requirements-traceability.py",
                "description": "Ensures requirements trace to implementation"
            }
        ]
        
        # Run each validation
        for validation in validations:
            self._run_validation(validation)
            
        # Check for alignment if this is part of a project
        if self._is_project_structure():
            self._run_alignment_validation()
            
        # Generate improvement suggestions
        self._run_improvement_analysis()
        
        # Final report
        self._generate_final_report()
        
    def _run_validation(self, validation: dict):
        """Run a single validation script"""
        print(f"\n🔍 Running: {validation['name']}")
        print(f"   {validation['description']}")
        print("-" * 60)
        
        script_path = self.scripts_dir / validation["script"]
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path), str(self.spec_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check result
            if result.returncode == 0:
                self.results[validation["name"]] = {
                    "status": "PASSED",
                    "output": result.stdout
                }
                self.passed += 1
                print("✅ PASSED")
            else:
                self.results[validation["name"]] = {
                    "status": "FAILED",
                    "output": result.stdout + "\n" + result.stderr
                }
                self.failed += 1
                print("❌ FAILED")
                
            # Show key findings
            if "score" in validation["script"].lower():
                # Extract score from output
                import re
                score_match = re.search(r'TOTAL SCORE:\s*(\d+)/100', result.stdout)
                if score_match:
                    score = int(score_match.group(1))
                    print(f"   Score: {score}/100")
                    if score < 90:
                        print(f"   ⚠️  Below target of 90")
                        
        except subprocess.TimeoutExpired:
            self.results[validation["name"]] = {
                "status": "TIMEOUT",
                "output": "Validation timed out after 30 seconds"
            }
            self.failed += 1
            print("⏱️  TIMEOUT")
            
        except Exception as e:
            self.results[validation["name"]] = {
                "status": "ERROR",
                "output": str(e)
            }
            self.failed += 1
            print(f"💥 ERROR: {e}")
            
    def _is_project_structure(self):
        """Check if spec is part of a full project structure"""
        project_dir = self.spec_path.parent.parent
        return (
            (project_dir / "roadmap").exists() or
            (project_dir / "phase-plans").exists()
        )
        
    def _run_alignment_validation(self):
        """Run alignment validation for full project"""
        print(f"\n🔄 Running: Document Alignment Validation")
        print("   Checks consistency between spec, roadmap, and plans")
        print("-" * 60)
        
        project_dir = self.spec_path.parent.parent
        script_path = self.scripts_dir / "validate-alignment.py"
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path), str(project_dir)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.results["Alignment Validation"] = {
                    "status": "PASSED",
                    "output": result.stdout
                }
                self.passed += 1
                print("✅ PASSED - Documents are aligned")
            else:
                self.results["Alignment Validation"] = {
                    "status": "WARNING",
                    "output": result.stdout
                }
                print("⚠️  WARNING - Alignment issues found")
                
        except Exception as e:
            print(f"💥 ERROR: {e}")
            
    def _run_improvement_analysis(self):
        """Generate improvement suggestions"""
        print(f"\n💡 Running: Improvement Analysis")
        print("   Generates specific suggestions for improvement")
        print("-" * 60)
        
        script_path = self.scripts_dir / "suggest-spec-improvements.py"
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path), str(self.spec_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Count suggestions
            import re
            high_priority = len(re.findall(r'HIGH PRIORITY.*?(\d+) items', result.stdout))
            med_priority = len(re.findall(r'MEDIUM PRIORITY.*?(\d+) items', result.stdout))
            
            print(f"📝 Suggestions generated")
            if high_priority > 0:
                print(f"   🔴 High priority items found")
                
        except Exception as e:
            print(f"💥 ERROR: {e}")
            
    def _generate_final_report(self):
        """Generate final validation report"""
        print("\n" + "="*60)
        print("FINAL VALIDATION REPORT")
        print("="*60)
        
        # Summary
        total = self.passed + self.failed
        print(f"\n📊 Summary: {self.passed}/{total} validations passed")
        
        # Quality gates
        print("\n🚦 Quality Gates:")
        
        # Extract quality score
        quality_score = None
        if "Quality Scoring" in self.results:
            import re
            score_match = re.search(r'TOTAL SCORE:\s*(\d+)/100', 
                                  self.results["Quality Scoring"]["output"])
            if score_match:
                quality_score = int(score_match.group(1))
                
        if quality_score:
            if quality_score >= 90:
                print(f"  ✅ Quality Score: {quality_score}/100 - READY FOR STANDARD APPROVAL")
            elif quality_score >= 85:
                print(f"  ⚠️  Quality Score: {quality_score}/100 - CONDITIONAL APPROVAL")
            elif quality_score >= 80:
                print(f"  ⚠️  Quality Score: {quality_score}/100 - EXTENDED APPROVAL POSSIBLE")
            else:
                print(f"  ❌ Quality Score: {quality_score}/100 - REQUIRES IMPROVEMENT")
        else:
            print(f"  ❓ Quality Score: Unable to determine")
            
        # Individual results
        print("\n📋 Detailed Results:")
        for name, result in self.results.items():
            status_icon = {
                "PASSED": "✅",
                "FAILED": "❌",
                "WARNING": "⚠️",
                "TIMEOUT": "⏱️",
                "ERROR": "💥"
            }.get(result["status"], "❓")
            
            print(f"  {status_icon} {name}: {result['status']}")
            
        # Recommendations
        print("\n📝 Next Steps:")
        if self.failed > 0:
            print("  1. Fix validation failures")
            print("  2. Review improvement suggestions")
            print("  3. Re-run validation")
        elif quality_score and quality_score < 90:
            print("  1. Review improvement suggestions")
            print("  2. Implement high priority improvements")
            print("  3. Target quality score of 90+")
        else:
            print("  ✅ Spec is ready to proceed!")
            print("  1. Get stakeholder approval")
            print("  2. Create implementation roadmap")
            print("  3. Begin phase planning")
            
        # Save summary
        summary_path = self.spec_path.parent / "validation-summary.txt"
        with open(summary_path, 'w') as f:
            f.write(f"Validation Summary\n")
            f.write(f"==================\n\n")
            f.write(f"Spec: {self.spec_path.name}\n")
            f.write(f"Date: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}\n")
            f.write(f"Results: {self.passed}/{total} passed\n")
            if quality_score:
                f.write(f"Quality Score: {quality_score}/100\n")
            f.write(f"\nDetailed results in individual report files.\n")
            
        print(f"\n📄 Summary saved to: {summary_path}")
        print("="*60)

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python validate-all.py <path-to-SPEC.md>")
        print("\nThis runs all validation scripts:")
        print("  - Structure validation")
        print("  - Link validation")
        print("  - Quality scoring")
        print("  - Requirements traceability")
        print("  - Alignment validation (if full project)")
        print("  - Improvement suggestions")
        sys.exit(1)
        
    spec_path = sys.argv[1]
    
    # Check spec exists
    if not Path(spec_path).exists():
        print(f"❌ Error: Spec file not found: {spec_path}")
        sys.exit(1)
        
    runner = ValidationRunner(spec_path)
    runner.run_all()

if __name__ == "__main__":
    main()