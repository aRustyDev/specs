#!/usr/bin/env python3
"""
Score Spec Quality
Automated quality scoring based on the spec quality rubric.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
import json

class SpecScorer:
    def __init__(self, spec_path: str):
        self.spec_path = Path(spec_path)
        self.spec_dir = self.spec_path.parent
        self.scores = {
            "completeness": 0,
            "clarity": 0,
            "implementability": 0,
            "testability": 0
        }
        self.details = {
            "completeness": {},
            "clarity": {},
            "implementability": {},
            "testability": {}
        }
        
    def score(self) -> int:
        """Calculate overall spec quality score"""
        print(f"📊 Scoring spec quality for: {self.spec_path}")
        
        # Score each dimension
        self._score_completeness()
        self._score_clarity()
        self._score_implementability()
        self._score_testability()
        
        # Calculate total
        total_score = sum(self.scores.values())
        
        # Report results
        self._report_results(total_score)
        
        return total_score
        
    def _score_completeness(self):
        """Score completeness dimension (0-25 points)"""
        print("\n📋 Scoring Completeness...")
        
        score = 0
        details = {}
        
        # Check core sections (10 points)
        required_sections = [
            "Executive Summary", "Stakeholders", "Requirements",
            "System Architecture", "Risks", "Success Metrics"
        ]
        
        with open(self.spec_path, 'r') as f:
            content = f.read()
            
        found_sections = 0
        for section in required_sections:
            if re.search(rf'^#{1,3}\s+{re.escape(section)}', content, re.MULTILINE | re.IGNORECASE):
                found_sections += 1
                
        section_score = int((found_sections / len(required_sections)) * 10)
        score += section_score
        details["core_sections"] = f"{found_sections}/{len(required_sections)} sections found ({section_score}/10)"
        
        # Check requirements coverage (8 points)
        func_reqs = len(re.findall(r'^#{3,4}\s+FR-\d+', content, re.MULTILINE))
        nfr_reqs = len(re.findall(r'^#{3,4}\s+NFR-\d+', content, re.MULTILINE))
        
        if func_reqs >= 5 and nfr_reqs >= 4:
            req_score = 8
        elif func_reqs >= 3 and nfr_reqs >= 2:
            req_score = 6
        else:
            req_score = 4
            
        score += req_score
        details["requirements"] = f"{func_reqs} functional, {nfr_reqs} non-functional ({req_score}/8)"
        
        # Check cross-references (4 points)
        cross_refs = len(re.findall(r'\[([^\]]+)\]\(#[^)]+\)', content))
        if cross_refs >= 10:
            ref_score = 4
        elif cross_refs >= 5:
            ref_score = 3
        else:
            ref_score = 2
            
        score += ref_score
        details["cross_references"] = f"{cross_refs} internal links ({ref_score}/4)"
        
        # Check placeholders (3 points)
        placeholders = len(re.findall(r'\b(TODO|TBD|FIXME|XXX)\b', content, re.IGNORECASE))
        if placeholders == 0:
            placeholder_score = 3
        elif placeholders <= 3:
            placeholder_score = 2
        else:
            placeholder_score = 0
            
        score += placeholder_score
        details["placeholders"] = f"{placeholders} found ({placeholder_score}/3)"
        
        self.scores["completeness"] = score
        self.details["completeness"] = details
        
    def _score_clarity(self):
        """Score clarity dimension (0-25 points)"""
        print("\n✨ Scoring Clarity...")
        
        score = 0
        details = {}
        
        with open(self.spec_path, 'r') as f:
            content = f.read()
            
        # Language precision (8 points)
        # Check for quantified metrics
        metrics = len(re.findall(r'\d+\s*(%|ms|s|GB|MB|hours?|days?|weeks?)', content))
        if metrics >= 20:
            precision_score = 8
        elif metrics >= 10:
            precision_score = 6
        else:
            precision_score = 4
            
        score += precision_score
        details["language_precision"] = f"{metrics} quantified metrics ({precision_score}/8)"
        
        # Consistency (7 points)
        # Simple check: consistent header formatting
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        consistent_headers = all(h[0].count('#') <= 4 for h in headers)
        consistency_score = 7 if consistent_headers else 5
        
        score += consistency_score
        details["consistency"] = f"Header consistency {'good' if consistent_headers else 'issues found'} ({consistency_score}/7)"
        
        # Structure & Flow (6 points)
        # Check logical section ordering
        section_order = []
        for match in re.finditer(r'^#{1,2}\s+(.+)$', content, re.MULTILINE):
            section_order.append(match.group(1).lower())
            
        expected_flow = ["executive", "stakeholder", "requirement", "architecture", "risk"]
        flow_score = 6
        for i, expected in enumerate(expected_flow):
            if not any(expected in section for section in section_order):
                flow_score -= 1
                
        score += flow_score
        details["structure_flow"] = f"Section flow score ({flow_score}/6)"
        
        # Visual aids (4 points)
        diagrams = len(re.findall(r'```(?:mermaid|diagram|ascii)', content))
        tables = len(re.findall(r'\|.+\|.+\|', content))
        
        if diagrams >= 2 and tables >= 5:
            visual_score = 4
        elif diagrams >= 1 and tables >= 3:
            visual_score = 3
        else:
            visual_score = 2
            
        score += visual_score
        details["visual_aids"] = f"{diagrams} diagrams, {tables} tables ({visual_score}/4)"
        
        self.scores["clarity"] = score
        self.details["clarity"] = details
        
    def _score_implementability(self):
        """Score implementability dimension (0-25 points)"""
        print("\n🔧 Scoring Implementability...")
        
        score = 0
        details = {}
        
        with open(self.spec_path, 'r') as f:
            content = f.read()
            
        # Technical feasibility (10 points)
        # Check for technology choices with rationale
        tech_choices = len(re.findall(r'(chose|selected|using|built with).{0,50}(because|due to|for)', 
                                     content, re.IGNORECASE))
        if tech_choices >= 5:
            feasibility_score = 10
        elif tech_choices >= 3:
            feasibility_score = 8
        else:
            feasibility_score = 6
            
        score += feasibility_score
        details["technical_feasibility"] = f"{tech_choices} justified tech choices ({feasibility_score}/10)"
        
        # Resource realism (6 points)
        # Check for timeline and team size mentions
        has_timeline = bool(re.search(r'\d+\s*(weeks?|months?)', content))
        has_team_size = bool(re.search(r'\d+\s*(developers?|engineers?|people|FTE)', content))
        has_budget = bool(re.search(r'\$[\d,]+', content))
        
        resource_score = 2 * sum([has_timeline, has_team_size, has_budget])
        score += resource_score
        details["resources"] = f"Timeline: {has_timeline}, Team: {has_team_size}, Budget: {has_budget} ({resource_score}/6)"
        
        # Dependency management (5 points)
        dependencies = len(re.findall(r'(depends on|requires|prerequisite|dependency)', content, re.IGNORECASE))
        if dependencies >= 5:
            dep_score = 5
        elif dependencies >= 3:
            dep_score = 4
        else:
            dep_score = 2
            
        score += dep_score
        details["dependencies"] = f"{dependencies} dependency mentions ({dep_score}/5)"
        
        # Risk mitigation (4 points)
        risks = len(re.findall(r'(risk|mitigation|contingency)', content, re.IGNORECASE))
        if risks >= 10:
            risk_score = 4
        elif risks >= 5:
            risk_score = 3
        else:
            risk_score = 2
            
        score += risk_score
        details["risk_mitigation"] = f"{risks} risk-related mentions ({risk_score}/4)"
        
        self.scores["implementability"] = score
        self.details["implementability"] = details
        
    def _score_testability(self):
        """Score testability dimension (0-25 points)"""
        print("\n🧪 Scoring Testability...")
        
        score = 0
        details = {}
        
        with open(self.spec_path, 'r') as f:
            content = f.read()
            
        # Measurable requirements (10 points)
        measurable = len(re.findall(r'<\s*\d+\s*(ms|s|%|GB|MB)', content))
        if measurable >= 10:
            measure_score = 10
        elif measurable >= 5:
            measure_score = 8
        else:
            measure_score = 5
            
        score += measure_score
        details["measurable_requirements"] = f"{measurable} measurable thresholds ({measure_score}/10)"
        
        # Test scenarios (8 points)
        scenarios = len(re.findall(r'(scenario|test case|acceptance criteria)', content, re.IGNORECASE))
        if scenarios >= 8:
            scenario_score = 8
        elif scenarios >= 4:
            scenario_score = 6
        else:
            scenario_score = 4
            
        score += scenario_score
        details["test_scenarios"] = f"{scenarios} test scenario mentions ({scenario_score}/8)"
        
        # Acceptance criteria (3 points)
        criteria = len(re.findall(r'(acceptance criteria|definition of done|success criteria)', 
                                 content, re.IGNORECASE))
        if criteria >= 5:
            criteria_score = 3
        elif criteria >= 2:
            criteria_score = 2
        else:
            criteria_score = 1
            
        score += criteria_score
        details["acceptance_criteria"] = f"{criteria} acceptance criteria sections ({criteria_score}/3)"
        
        # Baseline data (2 points)
        baseline = len(re.findall(r'(current|existing|baseline|today)', content, re.IGNORECASE))
        baseline_score = 2 if baseline >= 5 else 1
        
        score += baseline_score
        details["baseline_data"] = f"{baseline} baseline mentions ({baseline_score}/2)"
        
        # Quality metrics (3 points)
        quality = len(re.findall(r'(coverage|uptime|availability|performance|quality)', 
                                content, re.IGNORECASE))
        if quality >= 10:
            quality_score = 3
        elif quality >= 5:
            quality_score = 2
        else:
            quality_score = 1
            
        score += quality_score
        details["quality_metrics"] = f"{quality} quality metric mentions ({quality_score}/3)"
        
        self.scores["testability"] = score
        self.details["testability"] = details
        
    def _report_results(self, total_score: int):
        """Generate detailed scoring report"""
        print("\n" + "="*60)
        print("SPEC QUALITY SCORE REPORT")
        print("="*60)
        
        # Dimension scores
        print("\n📊 Dimension Scores:")
        for dimension, score in self.scores.items():
            print(f"  {dimension.capitalize()}: {score}/25")
            for key, detail in self.details[dimension].items():
                print(f"    - {key}: {detail}")
                
        # Total score
        print(f"\n🎯 TOTAL SCORE: {total_score}/100")
        
        # Interpretation
        if total_score >= 90:
            status = "✅ READY FOR STANDARD APPROVAL"
            risk = "Low risk - proceed to roadmap"
        elif total_score >= 85:
            status = "⚠️  CONDITIONAL APPROVAL"
            risk = "Medium risk - document gaps and mitigations"
        elif total_score >= 80:
            status = "⚠️  EXTENDED APPROVAL POSSIBLE"
            risk = "High risk - requires controls and monitoring"
        else:
            status = "❌ REQUIRES IMPROVEMENT"
            risk = "Very high risk - do not proceed"
            
        print(f"\nStatus: {status}")
        print(f"Risk Assessment: {risk}")
        
        # Save detailed report
        report_path = self.spec_path.parent / "spec-quality-report.json"
        report_data = {
            "spec_file": str(self.spec_path),
            "total_score": total_score,
            "dimension_scores": self.scores,
            "details": self.details,
            "status": status,
            "risk": risk
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: {report_path}")
        print("="*60)

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python score-spec-quality.py <path-to-SPEC.md>")
        sys.exit(1)
        
    spec_path = sys.argv[1]
    scorer = SpecScorer(spec_path)
    
    total_score = scorer.score()
    
    # Exit with appropriate code
    if total_score >= 90:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Needs improvement

if __name__ == "__main__":
    main()