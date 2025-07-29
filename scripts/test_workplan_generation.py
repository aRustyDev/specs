#!/usr/bin/env python3
"""
Work Plan Generation Test Suite

Comprehensive tests for the narrative work plan generator to ensure:
- Complete JSON configs generate valid work plans
- Partial configs fail gracefully with helpful errors
- Generated content matches quality of hand-written plans
- Edge cases are handled properly

Usage:
    python3 scripts/test_workplan_generation.py
    python3 scripts/test_workplan_generation.py -v  # Verbose output
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
import sys
import subprocess
import re
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from generate_phase_plan_v2 import NarrativeWorkPlanGenerator
from validate_workplan import WorkPlanValidator, ValidationLevel


class TestWorkPlanGeneration(unittest.TestCase):
    """Test suite for work plan generation."""
    
    def setUp(self):
        """Set up test environment."""
        self.generator = NarrativeWorkPlanGenerator()
        self.validator = WorkPlanValidator()
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def create_minimal_config(self) -> Dict[str, Any]:
        """Create a minimal valid configuration."""
        return {
            "phase": {
                "number": 1,
                "title": "Test Phase",
                "focus": "Testing",
                "narrative_overview": "This is a test phase for validation.",
                "critical_requirements": ["Test requirement 1", "Test requirement 2"]
            },
            "prerequisites": {
                "intro_narrative": "Before starting, ensure:",
                "completed_phases": {
                    "required": "None",
                    "descriptions": "This is the first phase"
                },
                "knowledge_areas": [
                    {
                        "area": "Unit Testing",
                        "description": "Understanding of test frameworks",
                        "importance": "Essential"
                    }
                ]
            },
            "resources": {
                "intro_narrative": "Resources for this phase:",
                "example_files": [
                    {
                        "name": "test.py",
                        "path": "examples/test.py",
                        "description": "Test examples",
                        "purpose": "Show testing patterns"
                    }
                ],
                "specifications": [
                    {
                        "name": "test-spec.md",
                        "path": "specs/test-spec.md",
                        "description": "Testing specification",
                        "key_sections": ["Overview", "Requirements"]
                    }
                ],
                "junior_dev_guides": [
                    {
                        "name": "Testing Guide",
                        "path": "guides/testing.md",
                        "description": "Introduction to testing",
                        "when_to_read": "Before writing any tests"
                    }
                ],
                "quick_links": [
                    {
                        "name": "Run Tests",
                        "command": "python -m pytest",
                        "purpose": "Execute test suite"
                    }
                ]
            },
            "overview": {
                "narrative": "This phase establishes the testing foundation.",
                "checkpoint_summary": "One checkpoint after basic setup.",
                "time_estimate": "1 week"
            },
            "methodology": {
                "approach": "Test-Driven Development",
                "importance_narrative": "TDD ensures quality from the start.",
                "rules": [
                    {
                        "step": "Write test first",
                        "description": "Create failing test",
                        "rationale": "Verify test can detect bugs"
                    }
                ]
            },
            "done_criteria": {
                "intro_narrative": "Phase is complete when:",
                "checklist": [
                    {
                        "criterion": "All tests pass",
                        "verification_method": "Run pytest"
                    }
                ]
            },
            "work_breakdown": [
                {
                    "section_number": "1.1",
                    "title": "Basic Setup",
                    "work_unit_context": {
                        "complexity": "Low",
                        "complexity_reason": "Simple configuration",
                        "scope": {
                            "estimated_lines": "~100 lines",
                            "file_count": "2-3 files"
                        },
                        "key_components": [
                            {
                                "name": "Test runner",
                                "estimated_lines": "~50",
                                "purpose": "Execute tests"
                            }
                        ],
                        "patterns": ["Test fixtures"],
                        "algorithms": []
                    },
                    "tasks": [
                        {
                            "number": "1.1.1",
                            "title": "Set up test framework",
                            "description": "Install and configure pytest. Ensure test data doesn't contain sensitive information.",
                            "tips": [
                                {
                                    "type": "junior_dev",
                                    "content": "Start with pytest tutorial",
                                    "resource_link": "guides/pytest.md"
                                },
                                {
                                    "type": "security",
                                    "content": "Never commit test data with real passwords or tokens",
                                    "resource_link": "guides/security.md"
                                }
                            ],
                            "code_examples": [
                                {
                                    "purpose": "Basic test structure",
                                    "language": "python",
                                    "code": "def test_example():\n    assert 1 + 1 == 2",
                                    "explanation": "Simple test example"
                                }
                            ]
                        }
                    ],
                    "checkpoint": {
                        "number": 1,
                        "title": "Setup Complete",
                        "stop_message": "CHECKPOINT 1: Review test setup",
                        "deliverables": ["Pytest configured", "Initial tests"],
                        "verification_steps": ["Run pytest", "Check coverage"],
                        "common_issues": []
                    }
                }
            ]
        }
    
    def test_minimal_config_generates_valid_plan(self):
        """Test that minimal config produces valid work plan."""
        config = self.create_minimal_config()
        config_path = self.test_dir / "test-config.json"
        
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        # Generate plan
        output_path = self.generator.generate_plan(str(config_path), str(self.test_dir))
        
        # Validate generated plan
        passed, issues = self.validator.validate_file(output_path)
        
        # Check no errors
        errors = [i for i in issues if i.level == ValidationLevel.ERROR]
        self.assertEqual(len(errors), 0, 
                        f"Generated plan has errors: {[e.message for e in errors]}")
        self.assertTrue(passed)
    
    def test_complete_config_generates_comprehensive_plan(self):
        """Test that complete config produces comprehensive work plan."""
        # Load the example complete config
        example_config = Path(__file__).parent.parent / ".claude" / "examples" / "phase-5-complete-config.json"
        self.assertTrue(example_config.exists(), "Example config not found")
        
        # Generate plan
        output_path = self.generator.generate_plan(str(example_config), str(self.test_dir))
        
        # Validate
        passed, issues = self.validator.validate_file(output_path)
        self.assertTrue(passed, "Complete config should generate valid plan")
        
        # Check content quality
        with open(output_path, 'r') as f:
            content = f.read()
        
        # Verify no TODOs
        self.assertNotIn("[TODO", content)
        
        # Verify key sections present
        self.assertIn("## Prerequisites", content)
        self.assertIn("## Development Methodology", content)
        self.assertIn("## Work Breakdown", content)
        self.assertIn("### 5.1 Metrics Implementation", content)
        
        # Verify rich content
        self.assertIn("💡", content)  # Tips present
        self.assertIn("```rust", content)  # Code examples
        self.assertIn("CHECKPOINT", content)  # Checkpoints
    
    def test_missing_required_fields_fail_gracefully(self):
        """Test that missing required fields produce helpful errors."""
        config = self.create_minimal_config()
        
        # Remove required field
        del config['phase']['title']
        
        config_path = self.test_dir / "invalid-config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        # Should raise ValueError with helpful message
        with self.assertRaises(KeyError) as context:
            self.generator.generate_plan(str(config_path), str(self.test_dir))
    
    def test_narrative_flow_quality(self):
        """Test that generated narrative has good flow."""
        config = self.create_minimal_config()
        
        # Add more narrative content
        config['work_breakdown'][0]['tasks'][0]['description'] = (
            "This task establishes the foundation for our testing infrastructure. "
            "We'll start by installing pytest and creating our first test file. "
            "Pay special attention to the directory structure as it affects test discovery."
        )
        
        config_path = self.test_dir / "narrative-config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        output_path = self.generator.generate_plan(str(config_path), str(self.test_dir))
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        # Check narrative quality
        lines = content.split('\n')
        
        # Find task description
        task_start = None
        for i, line in enumerate(lines):
            if "Task 1.1.1: Set up test framework" in line:
                task_start = i
                break
        
        self.assertIsNotNone(task_start)
        
        # Check multi-sentence description
        desc_lines = []
        for i in range(task_start + 1, min(task_start + 10, len(lines))):
            if lines[i].strip() and not lines[i].startswith('#'):
                desc_lines.append(lines[i])
            if lines[i].startswith('**'):
                break
        
        full_desc = ' '.join(desc_lines)
        self.assertIn("foundation", full_desc)
        self.assertIn("Pay special attention", full_desc)
    
    def test_security_section_generation(self):
        """Test security requirements section generation."""
        config = self.create_minimal_config()
        
        # Add security requirements
        config['security_requirements'] = {
            "importance_narrative": "Security is critical for this phase.",
            "categories": [
                {
                    "name": "Input Validation",
                    "requirements": [
                        {
                            "type": "MUST",
                            "requirement": "Validate all inputs",
                            "rationale": "Prevent injection attacks"
                        }
                    ],
                    "implementation_guidance": "Use schema validation",
                    "testing_approach": "Fuzz testing"
                }
            ]
        }
        
        config_path = self.test_dir / "security-config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        output_path = self.generator.generate_plan(str(config_path), str(self.test_dir))
        
        # Validate has security section
        passed, issues = self.validator.validate_file(output_path)
        
        # Check no security warnings
        security_warnings = [i for i in issues if i.category == "Security"]
        self.assertEqual(len(security_warnings), 0, 
                        "Should have no security warnings when section present")
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        self.assertIn("## Security Requirements", content)
        self.assertIn("**MUST**: Validate all inputs", content)
        self.assertIn("*Rationale*: Prevent injection attacks", content)
    
    def test_code_example_formatting(self):
        """Test that code examples are properly formatted."""
        config = self.create_minimal_config()
        
        # Add complex code example
        code_example = '''use tokio::test;

#[test]
async fn test_async_operation() {
    let result = async_function().await;
    assert_eq!(result, expected_value);
}'''
        
        config['work_breakdown'][0]['tasks'][0]['code_examples'][0]['code'] = code_example
        config['work_breakdown'][0]['tasks'][0]['code_examples'][0]['language'] = 'rust'
        
        config_path = self.test_dir / "code-config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        output_path = self.generator.generate_plan(str(config_path), str(self.test_dir))
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        # Verify code block formatting
        self.assertIn("```rust", content)
        self.assertIn("async fn test_async_operation()", content)
        self.assertIn("```", content.split("```rust")[1])  # Closing block
    
    def test_checkpoint_formatting(self):
        """Test checkpoint sections are properly formatted."""
        config = self.create_minimal_config()
        
        # Add detailed checkpoint
        config['work_breakdown'][0]['checkpoint']['common_issues'] = [
            {
                "issue": "Pytest not found",
                "solution": "Install with pip install pytest"
            },
            {
                "issue": "Tests not discovered",
                "solution": "Ensure test files start with test_"
            }
        ]
        
        config_path = self.test_dir / "checkpoint-config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        output_path = self.generator.generate_plan(str(config_path), str(self.test_dir))
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        # Check checkpoint formatting
        self.assertIn("---", content)  # Separator
        self.assertIn("### CHECKPOINT 1:", content)
        self.assertIn("**Common Issues:**", content)
        self.assertIn("**Issue**: Pytest not found", content)
        self.assertIn("**Solution**: Install with pip install pytest", content)
        self.assertIn("**DO NOT PROCEED**", content)
    
    def test_cli_integration(self):
        """Test command-line interface."""
        config_path = self.test_dir / "cli-test.json"
        config = self.create_minimal_config()
        
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        # Run script via CLI
        script_path = Path(__file__).parent / "generate_phase_plan_v2.py"
        result = subprocess.run(
            [sys.executable, str(script_path), str(config_path), str(self.test_dir)],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"CLI failed: {result.stderr}")
        self.assertIn("Generated narrative work plan:", result.stdout)
        
        # Verify file was created
        output_file = self.test_dir / ".claude" / ".plan" / "phase-1" / "WORK_PLAN.md"
        self.assertTrue(output_file.exists())
    
    def test_validation_integration(self):
        """Test integration with validation script."""
        config_path = self.test_dir / "validation-test.json"
        config = self.create_minimal_config()
        
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        # Run validation with --check-generation
        validator_script = Path(__file__).parent / "validate_workplan.py"
        result = subprocess.run(
            [sys.executable, str(validator_script), 
             "--config", str(config_path), 
             "--check-generation"],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, 
                        f"Validation failed: {result.stdout}\n{result.stderr}")
        self.assertIn("Validation PASSED", result.stdout)


class TestQualityMetrics(unittest.TestCase):
    """Test quality metrics for generated work plans."""
    
    def setUp(self):
        """Set up quality testing."""
        self.generator = NarrativeWorkPlanGenerator()
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.test_dir)
    
    def measure_readability_score(self, text: str) -> float:
        """Simple readability metric based on sentence/word length."""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if not sentences:
            return 0.0
        
        total_words = 0
        for sentence in sentences:
            total_words += len(sentence.split())
        
        avg_sentence_length = total_words / len(sentences)
        
        # Ideal sentence length is 15-20 words
        if 15 <= avg_sentence_length <= 20:
            return 1.0
        elif avg_sentence_length < 10 or avg_sentence_length > 30:
            return 0.5
        else:
            return 0.75
    
    def test_readability_metrics(self):
        """Test that generated content has good readability."""
        config = Path(__file__).parent.parent / ".claude" / "examples" / "phase-5-complete-config.json"
        output_path = self.generator.generate_plan(str(config), str(self.test_dir))
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        # Extract narrative sections
        overview_match = re.search(r'## Overview\n\n(.+?)\n\n', content, re.DOTALL)
        self.assertIsNotNone(overview_match)
        
        overview_text = overview_match.group(1)
        readability = self.measure_readability_score(overview_text)
        
        self.assertGreater(readability, 0.7, 
                          "Overview section should have good readability")
    
    def test_completeness_metrics(self):
        """Test that all required elements are present."""
        config = Path(__file__).parent.parent / ".claude" / "examples" / "phase-5-complete-config.json"
        output_path = self.generator.generate_plan(str(config), str(self.test_dir))
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        # Count key elements
        metrics = {
            "code_examples": len(re.findall(r'```\w+', content)),
            "tips": len(re.findall(r'[💡⚠️🔒⚡]', content)),
            "checkpoints": len(re.findall(r'CHECKPOINT \d+:', content)),
            "tasks": len(re.findall(r'#### Task \d+\.\d+\.\d+:', content)),
            "external_links": len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))
        }
        
        # Verify minimum thresholds
        self.assertGreater(metrics['code_examples'], 5, "Should have multiple code examples")
        self.assertGreater(metrics['tips'], 10, "Should have many tips/warnings")
        self.assertEqual(metrics['checkpoints'], 4, "Should have 4 checkpoints")
        self.assertGreater(metrics['tasks'], 8, "Should have many tasks")
        self.assertGreater(metrics['external_links'], 15, "Should have many resource links")


if __name__ == '__main__':
    # Run with verbose output if -v flag provided
    import sys
    if '-v' in sys.argv:
        unittest.main(verbosity=2)
    else:
        unittest.main()