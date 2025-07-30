#!/usr/bin/env python3
"""
Run all spec validation scripts in sequence.

This tool provides a comprehensive validation suite that checks:
- Structure and completeness
- Quality scoring
- Link validation
- Requirements traceability
- Improvement suggestions

Use this before major reviews or as a CI/CD gate.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from automation.lib.base import SpecTool
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from lib.base import SpecTool

class SpecValidationSuite(SpecTool):
    """Run all spec validation scripts."""
    
    VERSION = "1.0.0"
    DESCRIPTION = "Comprehensive spec validation suite"
    
    # Validation scripts to run in order
    VALIDATORS = [
        {
            'name': 'Structure Validation',
            'script': 'validation/validate-spec-structure.py',
            'critical': True,
            'args': []
        },
        {
            'name': 'Quality Scoring',
            'script': 'validation/score-spec-quality.py',
            'critical': True,
            'args': ['--strict']
        },
        {
            'name': 'Link Validation',
            'script': 'validation/validate-spec-links.py',
            'critical': False,
            'args': []
        },
        {
            'name': 'Requirements Traceability',
            'script': 'validation/validate-requirements-traceability.py',
            'critical': False,
            'args': []
        }
    ]
    
    def create_parser(self):
        parser = super().create_parser()
        parser.add_argument('spec_path',
                          help='Path to SPEC.md file')
        parser.add_argument('--stop-on-error', action='store_true',
                          help='Stop at first validation failure')
        parser.add_argument('--quiet', action='store_true',
                          help='Minimal output')
        parser.add_argument('--report', metavar='FILE',
                          help='Save validation report to file')
        parser.add_argument('--skip', nargs='+',
                          choices=['structure', 'quality', 'links', 'traceability'],
                          help='Skip specific validators')
        return parser
    
    def get_examples(self):
        return """
Examples:
  # Run all validations
  %(prog)s spec/SPEC.md
  
  # Stop at first error (good for CI/CD)
  %(prog)s spec/SPEC.md --stop-on-error
  
  # Generate report
  %(prog)s spec/SPEC.md --report validation-report.json
  
  # Skip specific validators
  %(prog)s spec/SPEC.md --skip links traceability
"""
    
    def execute(self) -> int:
        spec_path = Path(self.args.spec_path)
        if not spec_path.exists():
            print(f"✗ Spec file not found: {spec_path}")
            return 1
        
        print(f"🔍 Running comprehensive validation for: {spec_path}")
        print("=" * 60)
        
        results = []
        overall_success = True
        
        # Run each validator
        for validator in self.VALIDATORS:
            if self._should_skip(validator['name']):
                continue
                
            result = self._run_validator(validator, spec_path)
            results.append(result)
            
            if not result['success'] and validator['critical']:
                overall_success = False
                if self.args.stop_on_error:
                    break
        
        # Show summary
        self._show_summary(results, overall_success)
        
        # Save report if requested
        if self.args.report:
            self._save_report(results, spec_path)
        
        # Check if improvement suggestions should be shown
        if not overall_success and not self.args.quiet:
            self._run_improvement_suggestions(spec_path)
        
        return 0 if overall_success else 1
    
    def _should_skip(self, validator_name: str) -> bool:
        """Check if validator should be skipped."""
        if not self.args.skip:
            return False
            
        skip_map = {
            'Structure Validation': 'structure',
            'Quality Scoring': 'quality',
            'Link Validation': 'links',
            'Requirements Traceability': 'traceability'
        }
        
        return skip_map.get(validator_name, '') in self.args.skip
    
    def _run_validator(self, validator: Dict, spec_path: Path) -> Dict:
        """Run a single validator."""
        if not self.args.quiet:
            print(f"\n▶️  Running {validator['name']}...")
            print("-" * 40)
        
        # Build command
        script_path = Path(__file__).parent / validator['script']
        cmd = [sys.executable, str(script_path), str(spec_path)] + validator['args']
        
        # Run validator
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            
            if not self.args.quiet:
                if success:
                    print("✅ PASSED")
                else:
                    print("❌ FAILED")
                    if result.stdout:
                        print(result.stdout)
                    if result.stderr:
                        print(f"Error: {result.stderr}")
            
            return {
                'name': validator['name'],
                'success': success,
                'critical': validator['critical'],
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            print("⏱️  TIMEOUT")
            return {
                'name': validator['name'],
                'success': False,
                'critical': validator['critical'],
                'output': '',
                'error': 'Validation timed out',
                'return_code': -1
            }
        except Exception as e:
            print(f"💥 ERROR: {e}")
            return {
                'name': validator['name'],
                'success': False,
                'critical': validator['critical'],
                'output': '',
                'error': str(e),
                'return_code': -1
            }
    
    def _show_summary(self, results: List[Dict], overall_success: bool):
        """Show validation summary."""
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in results if r['success'])
        total = len(results)
        
        print(f"\nValidations run: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        
        if results:
            print("\nDetails:")
            for result in results:
                status = "✅ PASS" if result['success'] else "❌ FAIL"
                critical = " (critical)" if result['critical'] and not result['success'] else ""
                print(f"  - {result['name']}: {status}{critical}")
        
        print("\n" + "=" * 60)
        
        if overall_success:
            print("\n🎉 All validations PASSED! Spec is ready for review.")
        else:
            print("\n❌ Validation FAILED. Please address the issues above.")
    
    def _save_report(self, results: List[Dict], spec_path: Path):
        """Save validation report to file."""
        report = {
            'spec_path': str(spec_path),
            'timestamp': datetime.now().isoformat(),
            'overall_success': all(r['success'] for r in results if r['critical']),
            'results': results
        }
        
        report_path = Path(self.args.report)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Validation report saved to: {report_path}")
    
    def _run_improvement_suggestions(self, spec_path: Path):
        """Run improvement suggestions script."""
        print("\n💡 Getting improvement suggestions...")
        print("=" * 60)
        
        script_path = Path(__file__).parent / 'improvement' / 'suggest-spec-improvements.py'
        if script_path.exists():
            cmd = [sys.executable, str(script_path), str(spec_path)]
            subprocess.run(cmd)

def main():
    tool = SpecValidationSuite()
    sys.exit(tool.run())

if __name__ == '__main__':
    main()