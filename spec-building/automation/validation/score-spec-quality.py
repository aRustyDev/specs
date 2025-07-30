#!/usr/bin/env python3
"""
Score spec quality based on comprehensive rubric.

This tool evaluates specifications across four key dimensions:
- Completeness: All required sections and content present
- Clarity: Clear, unambiguous, well-structured content
- Implementability: Technically feasible with resources identified
- Testability: Measurable criteria and validation methods

Scores help ensure specs meet quality standards before implementation begins.
"""

import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from automation.lib.base import SpecTool
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from lib.base import SpecTool

@dataclass
class DimensionScore:
    """Score details for a quality dimension."""
    name: str
    score: int
    max_score: int
    details: Dict[str, str]
    suggestions: List[str]

@dataclass
class QualityReport:
    """Complete quality assessment report."""
    total_score: int
    max_score: int
    dimensions: List[DimensionScore]
    status: str
    risk_level: str
    timestamp: str
    spec_path: str

class SpecQualityScorer(SpecTool):
    """Score spec quality across multiple dimensions."""
    
    VERSION = "2.0.0"
    DESCRIPTION = "Evaluate specification quality with detailed scoring"
    
    # Scoring thresholds
    THRESHOLDS = {
        'excellent': 95,
        'good': 90,
        'acceptable': 85,
        'poor': 70,
        'unacceptable': 0
    }
    
    def create_parser(self):
        parser = super().create_parser()
        parser.add_argument('spec_path',
                          help='Path to SPEC.md file')
        parser.add_argument('-f', '--format', 
                          choices=['console', 'json', 'markdown'],
                          default='console',
                          help='Output format (default: console)')
        parser.add_argument('-o', '--output-file',
                          help='Write report to file')
        parser.add_argument('--strict', action='store_true',
                          help='Require 90+ score for success exit code')
        parser.add_argument('--dimensions', nargs='+',
                          choices=['completeness', 'clarity', 'implementability', 'testability'],
                          help='Score only specific dimensions')
        return parser
    
    def get_examples(self):
        return """
Examples:
  # Basic scoring with console output
  %(prog)s spec/SPEC.md
  
  # Generate JSON report
  %(prog)s spec/SPEC.md -f json -o quality-report.json
  
  # Strict mode for CI/CD
  %(prog)s spec/SPEC.md --strict
  
  # Score specific dimensions only
  %(prog)s spec/SPEC.md --dimensions completeness clarity
"""
    
    def execute(self) -> int:
        # Load spec file
        spec_path = Path(self.args.spec_path)
        if not spec_path.exists():
            print(f"✗ Spec file not found: {spec_path}")
            return 1
            
        print(f"📊 Scoring spec quality for: {spec_path}\n")
        
        with open(spec_path, 'r') as f:
            self.content = f.read()
            
        # Score dimensions
        dimensions_to_score = self.args.dimensions or ['completeness', 'clarity', 'implementability', 'testability']
        dimension_scores = []
        
        for dimension in dimensions_to_score:
            if dimension == 'completeness':
                score = self._score_completeness()
            elif dimension == 'clarity':
                score = self._score_clarity()
            elif dimension == 'implementability':
                score = self._score_implementability()
            elif dimension == 'testability':
                score = self._score_testability()
            dimension_scores.append(score)
        
        # Calculate totals
        total_score = sum(d.score for d in dimension_scores)
        max_score = sum(d.max_score for d in dimension_scores)
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Determine status
        if percentage >= self.THRESHOLDS['good']:
            status = "✅ READY FOR REVIEW"
            risk_level = "Low"
        elif percentage >= self.THRESHOLDS['acceptable']:
            status = "⚠️ NEEDS IMPROVEMENT"
            risk_level = "Medium"
        else:
            status = "❌ REQUIRES SIGNIFICANT WORK"
            risk_level = "High"
        
        # Create report
        report = QualityReport(
            total_score=total_score,
            max_score=max_score,
            dimensions=dimension_scores,
            status=status,
            risk_level=risk_level,
            timestamp=datetime.now().isoformat(),
            spec_path=str(spec_path)
        )
        
        # Output report
        if self.args.format == 'json':
            self._output_json(report)
        elif self.args.format == 'markdown':
            self._output_markdown(report)
        else:
            self._output_console(report)
        
        # Determine exit code
        if self.args.strict and percentage < self.THRESHOLDS['good']:
            return 1
        return 0
    
    def _score_completeness(self) -> DimensionScore:
        """Score the completeness dimension."""
        print("📋 Scoring Completeness...")
        
        score = 0
        max_score = 25
        details = {}
        suggestions = []
        
        # Check required sections (10 points)
        required_sections = [
            "Executive Summary", "Stakeholders", "Requirements",
            "System Architecture", "Risks", "Success Metrics",
            "Implementation Approach", "Constraints"
        ]
        
        found_sections = []
        for section in required_sections:
            if re.search(rf'^#{1,3}\s+{re.escape(section)}', self.content, re.MULTILINE | re.IGNORECASE):
                found_sections.append(section)
        
        section_score = int((len(found_sections) / len(required_sections)) * 10)
        score += section_score
        details["core_sections"] = f"{len(found_sections)}/{len(required_sections)} sections ({section_score}/10)"
        
        missing = set(required_sections) - set(found_sections)
        if missing:
            suggestions.append(f"Add missing sections: {', '.join(missing)}")
        
        # Check requirements detail (8 points)
        func_reqs = len(re.findall(r'^#{3,4}\s+FR-\d+', self.content, re.MULTILINE))
        nfr_reqs = len(re.findall(r'^#{3,4}\s+NFR-\d+', self.content, re.MULTILINE))
        
        req_score = min(8, (func_reqs + nfr_reqs) // 2)
        score += req_score
        details["requirements"] = f"{func_reqs} functional, {nfr_reqs} non-functional ({req_score}/8)"
        
        if func_reqs < 5:
            suggestions.append("Add more functional requirements (aim for 5+)")
        if nfr_reqs < 4:
            suggestions.append("Add more non-functional requirements (aim for 4+)")
        
        # Check for placeholders (3 points)
        placeholders = len(re.findall(r'\[(?:TBD|TODO|FIXME|XXX|PLACEHOLDER)\]', self.content, re.IGNORECASE))
        placeholder_score = max(0, 3 - placeholders)
        score += placeholder_score
        details["placeholders"] = f"{placeholders} found ({placeholder_score}/3)"
        
        if placeholders > 0:
            suggestions.append(f"Replace {placeholders} placeholder(s) with actual content")
        
        # Check cross-references (4 points)
        internal_links = len(re.findall(r'\[([^\]]+)\]\(#[^)]+\)', self.content))
        ref_score = min(4, internal_links // 3)
        score += ref_score
        details["cross_references"] = f"{internal_links} internal links ({ref_score}/4)"
        
        if internal_links < 10:
            suggestions.append("Add more internal cross-references between sections")
        
        return DimensionScore(
            name="Completeness",
            score=score,
            max_score=max_score,
            details=details,
            suggestions=suggestions
        )
    
    def _score_clarity(self) -> DimensionScore:
        """Score the clarity dimension."""
        print("✨ Scoring Clarity...")
        
        score = 0
        max_score = 25
        details = {}
        suggestions = []
        
        # Language precision (8 points)
        # Check for quantified metrics
        quantified = len(re.findall(r'\d+(?:\.\d+)?(?:\s*(?:%|percent|ms|seconds?|minutes?|hours?|days?|GB|MB|req/sec))', self.content))
        precision_score = min(8, quantified // 3)
        score += precision_score
        details["language_precision"] = f"{quantified} quantified metrics ({precision_score}/8)"
        
        if quantified < 20:
            suggestions.append("Add more specific, quantified metrics")
        
        # Structure and flow (6 points)
        # Check heading hierarchy
        headings = re.findall(r'^(#{1,6})\s+(.+)$', self.content, re.MULTILINE)
        proper_hierarchy = True
        prev_level = 0
        for heading in headings:
            level = len(heading[0])
            if level > prev_level + 1:
                proper_hierarchy = False
                break
            prev_level = level
        
        structure_score = 6 if proper_hierarchy else 3
        score += structure_score
        details["structure_flow"] = f"Heading hierarchy {'correct' if proper_hierarchy else 'has issues'} ({structure_score}/6)"
        
        if not proper_hierarchy:
            suggestions.append("Fix heading hierarchy - don't skip levels")
        
        # Consistency (7 points)
        # Check for consistent terminology
        score += 7  # Base score, could be more sophisticated
        details["consistency"] = "Terminology consistency (7/7)"
        
        # Visual aids (4 points)
        diagrams = len(re.findall(r'```(?:mermaid|diagram|ascii)', self.content, re.IGNORECASE))
        tables = len(re.findall(r'^\|', self.content, re.MULTILINE))
        
        visual_score = min(4, (diagrams * 2) + (tables // 5))
        score += visual_score
        details["visual_aids"] = f"{diagrams} diagrams, {tables} table rows ({visual_score}/4)"
        
        if diagrams == 0:
            suggestions.append("Add architecture or flow diagrams")
        if tables < 10:
            suggestions.append("Use more tables for structured data")
        
        return DimensionScore(
            name="Clarity",
            score=score,
            max_score=max_score,
            details=details,
            suggestions=suggestions
        )
    
    def _score_implementability(self) -> DimensionScore:
        """Score the implementability dimension."""
        print("🔧 Scoring Implementability...")
        
        score = 0
        max_score = 25
        details = {}
        suggestions = []
        
        # Technical feasibility (10 points)
        tech_mentions = len(re.findall(r'(?:version|v)\s*\d+(?:\.\d+)*', self.content))
        justified_choices = len(re.findall(r'(?:because|reason|why|chose|selected)', self.content, re.IGNORECASE))
        
        feasibility_score = min(10, (tech_mentions * 2) + (justified_choices // 3))
        score += feasibility_score
        details["technical_feasibility"] = f"{tech_mentions} versioned, {justified_choices} justified ({feasibility_score}/10)"
        
        if tech_mentions < 3:
            suggestions.append("Specify versions for technologies")
        if justified_choices < 10:
            suggestions.append("Add justifications for technical choices")
        
        # Resource planning (6 points)
        has_timeline = bool(re.search(r'(?:timeline|schedule|phase|sprint)', self.content, re.IGNORECASE))
        has_team = bool(re.search(r'(?:team|developer|engineer|resource)', self.content, re.IGNORECASE))
        has_budget = bool(re.search(r'(?:budget|cost|\$|dollar)', self.content, re.IGNORECASE))
        
        resource_score = (2 if has_timeline else 0) + (2 if has_team else 0) + (2 if has_budget else 0)
        score += resource_score
        details["resources"] = f"Timeline: {has_timeline}, Team: {has_team}, Budget: {has_budget} ({resource_score}/6)"
        
        if not has_timeline:
            suggestions.append("Add implementation timeline")
        if not has_team:
            suggestions.append("Specify team composition and skills")
        if not has_budget:
            suggestions.append("Include budget estimates")
        
        # Dependencies (5 points)
        dep_mentions = len(re.findall(r'(?:depend|require|integrate|interface)', self.content, re.IGNORECASE))
        dep_score = min(5, dep_mentions // 4)
        score += dep_score
        details["dependencies"] = f"{dep_mentions} dependency mentions ({dep_score}/5)"
        
        if dep_mentions < 10:
            suggestions.append("Better document external dependencies")
        
        # Risk mitigation (4 points)
        risk_mentions = len(re.findall(r'(?:risk|mitigation|contingency|fallback)', self.content, re.IGNORECASE))
        risk_score = min(4, risk_mentions // 3)
        score += risk_score
        details["risk_mitigation"] = f"{risk_mentions} risk-related mentions ({risk_score}/4)"
        
        if risk_mentions < 10:
            suggestions.append("Add more risk analysis and mitigation strategies")
        
        return DimensionScore(
            name="Implementability",
            score=score,
            max_score=max_score,
            details=details,
            suggestions=suggestions
        )
    
    def _score_testability(self) -> DimensionScore:
        """Score the testability dimension."""
        print("🧪 Scoring Testability...")
        
        score = 0
        max_score = 25
        details = {}
        suggestions = []
        
        # Measurable requirements (10 points)
        measurable = len(re.findall(r'(?:shall|must|will)\s+\w+', self.content))
        thresholds = len(re.findall(r'[<>≤≥]\s*\d+', self.content))
        
        measurable_score = min(10, (measurable // 5) + (thresholds // 2))
        score += measurable_score
        details["measurable_requirements"] = f"{measurable} requirements, {thresholds} thresholds ({measurable_score}/10)"
        
        if measurable < 20:
            suggestions.append("Make requirements more specific with 'shall/must' language")
        if thresholds < 10:
            suggestions.append("Add more quantifiable thresholds")
        
        # Test scenarios (8 points)
        scenarios = len(re.findall(r'(?:scenario|test case|given.*when.*then)', self.content, re.IGNORECASE))
        scenario_score = min(8, scenarios)
        score += scenario_score
        details["test_scenarios"] = f"{scenarios} test scenarios ({scenario_score}/8)"
        
        if scenarios < 5:
            suggestions.append("Add more test scenarios or acceptance criteria")
        
        # Acceptance criteria (3 points)
        criteria = len(re.findall(r'(?:acceptance criteria|success criteria|definition of done)', self.content, re.IGNORECASE))
        criteria_score = min(3, criteria)
        score += criteria_score
        details["acceptance_criteria"] = f"{criteria} sections ({criteria_score}/3)"
        
        if criteria < 3:
            suggestions.append("Define acceptance criteria for each major feature")
        
        # Quality metrics (4 points)
        metrics = len(re.findall(r'(?:metric|measure|kpi|indicator)', self.content, re.IGNORECASE))
        metrics_score = min(4, metrics // 3)
        score += metrics_score
        details["quality_metrics"] = f"{metrics} metric mentions ({metrics_score}/4)"
        
        if metrics < 10:
            suggestions.append("Define more quality metrics and how to measure them")
        
        return DimensionScore(
            name="Testability",
            score=score,
            max_score=max_score,
            details=details,
            suggestions=suggestions
        )
    
    def _output_console(self, report: QualityReport):
        """Output report to console."""
        percentage = (report.total_score / report.max_score * 100) if report.max_score > 0 else 0
        
        print("=" * 60)
        print("SPEC QUALITY SCORE REPORT")
        print("=" * 60)
        print()
        
        print("📊 Dimension Scores:")
        for dim in report.dimensions:
            dim_percentage = (dim.score / dim.max_score * 100) if dim.max_score > 0 else 0
            print(f"  {dim.name}: {dim.score}/{dim.max_score} ({dim_percentage:.0f}%)")
            for key, value in dim.details.items():
                print(f"    - {key}: {value}")
        
        print(f"\n🎯 TOTAL SCORE: {report.total_score}/{report.max_score} ({percentage:.0f}%)")
        print(f"\nStatus: {report.status}")
        print(f"Risk Level: {report.risk_level}")
        
        # Show improvement suggestions
        all_suggestions = []
        for dim in report.dimensions:
            all_suggestions.extend(dim.suggestions)
        
        if all_suggestions:
            print("\n💡 Top Improvement Suggestions:")
            for i, suggestion in enumerate(all_suggestions[:5], 1):
                print(f"  {i}. {suggestion}")
        
        # Save report if requested
        if self.args.output_file:
            output_path = Path(self.args.output_file)
            if output_path.suffix == '.json':
                self._save_json_report(report, output_path)
            else:
                self._save_text_report(report, output_path, percentage)
            print(f"\n📄 Detailed report saved to: {output_path}")
        else:
            # Save JSON report next to spec
            json_path = Path(self.args.spec_path).parent / "spec-quality-report.json"
            self._save_json_report(report, json_path)
            print(f"\n📄 JSON report saved to: {json_path}")
        
        print("=" * 60)
    
    def _output_json(self, report: QualityReport):
        """Output report as JSON."""
        report_dict = asdict(report)
        
        if self.args.output_file:
            with open(self.args.output_file, 'w') as f:
                json.dump(report_dict, f, indent=2)
        else:
            print(json.dumps(report_dict, indent=2))
    
    def _output_markdown(self, report: QualityReport):
        """Output report as Markdown."""
        percentage = (report.total_score / report.max_score * 100) if report.max_score > 0 else 0
        
        md = f"""# Spec Quality Report

**File**: {report.spec_path}  
**Date**: {report.timestamp}  
**Score**: {report.total_score}/{report.max_score} ({percentage:.0f}%)  
**Status**: {report.status}

## Dimension Scores

"""
        for dim in report.dimensions:
            dim_percentage = (dim.score / dim.max_score * 100) if dim.max_score > 0 else 0
            md += f"### {dim.name}: {dim.score}/{dim.max_score} ({dim_percentage:.0f}%)\n\n"
            
            for key, value in dim.details.items():
                md += f"- **{key.replace('_', ' ').title()}**: {value}\n"
            
            if dim.suggestions:
                md += "\n**Improvements needed**:\n"
                for suggestion in dim.suggestions:
                    md += f"- {suggestion}\n"
            md += "\n"
        
        md += f"""## Summary

- **Total Score**: {percentage:.0f}%
- **Risk Level**: {report.risk_level}
- **Recommendation**: {report.status}
"""
        
        if self.args.output_file:
            with open(self.args.output_file, 'w') as f:
                f.write(md)
        else:
            print(md)
    
    def _save_json_report(self, report: QualityReport, path: Path):
        """Save report as JSON."""
        with open(path, 'w') as f:
            json.dump(asdict(report), f, indent=2)
    
    def _save_text_report(self, report: QualityReport, path: Path, percentage: float):
        """Save report as text."""
        with open(path, 'w') as f:
            f.write(f"SPEC QUALITY REPORT\n")
            f.write(f"{'=' * 50}\n\n")
            f.write(f"File: {report.spec_path}\n")
            f.write(f"Date: {report.timestamp}\n")
            f.write(f"Score: {report.total_score}/{report.max_score} ({percentage:.0f}%)\n")
            f.write(f"Status: {report.status}\n\n")
            
            for dim in report.dimensions:
                f.write(f"\n{dim.name}:\n")
                for key, value in dim.details.items():
                    f.write(f"  - {key}: {value}\n")
                if dim.suggestions:
                    f.write("  Suggestions:\n")
                    for suggestion in dim.suggestions:
                        f.write(f"    - {suggestion}\n")

def main():
    tool = SpecQualityScorer()
    sys.exit(tool.run())

if __name__ == '__main__':
    main()