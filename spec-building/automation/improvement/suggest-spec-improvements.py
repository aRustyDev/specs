#!/usr/bin/env python3
"""
Suggest Spec Improvements
Analyzes a spec and provides specific, actionable improvement suggestions.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

class ImprovementAnalyzer:
    def __init__(self, spec_path: str):
        self.spec_path = Path(spec_path)
        self.content = ""
        self.suggestions = {
            "high_priority": [],
            "medium_priority": [],
            "low_priority": []
        }
        
    def analyze(self):
        """Run improvement analysis"""
        print(f"🔍 Analyzing spec for improvements: {self.spec_path}")
        
        with open(self.spec_path, 'r') as f:
            self.content = f.read()
            
        # Run various checks
        self._check_quantification()
        self._check_testability()
        self._check_visual_aids()
        self._check_acceptance_criteria()
        self._check_risk_coverage()
        self._check_architecture_detail()
        self._check_timeline_detail()
        self._check_success_metrics()
        
        # Generate report
        self._generate_report()
        
    def _check_quantification(self):
        """Check for vague vs quantified statements"""
        print("\n📊 Checking quantification...")
        
        vague_patterns = [
            (r'\b(fast|slow|quick|good|bad|many|few|some)\b', 
             "Replace vague term '{0}' with specific metric"),
            (r'\b(improve|enhance|optimize)\b(?!.*\d+%)',
             "Quantify improvement - add specific percentage or metric"),
            (r'\b(high|low|medium)\s+(performance|availability|quality)\b(?!.*\d+)',
             "Define what '{0}' means with specific thresholds")
        ]
        
        for pattern, suggestion in vague_patterns:
            matches = re.finditer(pattern, self.content, re.IGNORECASE)
            for match in matches:
                line_num = self.content[:match.start()].count('\n') + 1
                self.suggestions["high_priority"].append({
                    "line": line_num,
                    "issue": f"Vague term: '{match.group(0)}'",
                    "suggestion": suggestion.format(match.group(0)),
                    "example": "Instead of 'fast response', use 'response time <200ms'"
                })
                
    def _check_testability(self):
        """Check for testable requirements"""
        print("\n🧪 Checking testability...")
        
        # Find requirements without clear acceptance criteria
        req_pattern = r'^#{3,4}\s+(FR|NFR)-\d+[:\s]+(.+?)(?=^#{1,4}|\Z)'
        requirements = re.finditer(req_pattern, self.content, re.MULTILINE | re.DOTALL)
        
        for req in requirements:
            req_text = req.group(2)
            req_id = req.group(1) + "-" + req.group(0).split('-')[1].split(':')[0]
            
            # Check for measurable criteria
            if not re.search(r'\d+\s*(ms|s|%|MB|GB|users?)', req_text):
                line_num = self.content[:req.start()].count('\n') + 1
                self.suggestions["high_priority"].append({
                    "line": line_num,
                    "issue": f"Requirement {req_id} lacks measurable criteria",
                    "suggestion": "Add specific, measurable acceptance criteria",
                    "example": "Add: 'Must handle X requests/second with Y ms response time'"
                })
                
    def _check_visual_aids(self):
        """Check for missing diagrams"""
        print("\n🎨 Checking visual aids...")
        
        # Check architecture section
        arch_section = re.search(r'#{1,2}\s+System Architecture(.+?)(?=^#{1,2}|\Z)', 
                                self.content, re.MULTILINE | re.DOTALL)
        
        if arch_section:
            arch_content = arch_section.group(1)
            if not re.search(r'```(?:mermaid|diagram|ascii)', arch_content):
                line_num = self.content[:arch_section.start()].count('\n') + 1
                self.suggestions["medium_priority"].append({
                    "line": line_num,
                    "issue": "Architecture section lacks diagrams",
                    "suggestion": "Add system architecture diagram",
                    "example": """Add a Mermaid diagram:
```mermaid
graph TD
    A[Client] --> B[API Gateway]
    B --> C[Service 1]
    B --> D[Service 2]
```"""
                })
                
        # Check for data flow diagrams
        if "data flow" in self.content.lower() and "```" not in self.content[max(0, self.content.lower().find("data flow")-100):self.content.lower().find("data flow")+100]:
            self.suggestions["medium_priority"].append({
                "line": 0,
                "issue": "Data flow mentioned but not visualized",
                "suggestion": "Add data flow diagram",
                "example": "Show how data moves through the system components"
            })
            
    def _check_acceptance_criteria(self):
        """Check for missing acceptance criteria"""
        print("\n✅ Checking acceptance criteria...")
        
        if self.content.count("Acceptance Criteria") < 3:
            self.suggestions["high_priority"].append({
                "line": 0,
                "issue": "Limited acceptance criteria sections",
                "suggestion": "Add acceptance criteria for each major requirement",
                "example": """For each requirement add:
**Acceptance Criteria**:
- [ ] Specific measurable criterion 1
- [ ] Specific measurable criterion 2
- [ ] Performance threshold met"""
            })
            
    def _check_risk_coverage(self):
        """Check risk analysis completeness"""
        print("\n⚠️  Checking risk coverage...")
        
        risk_section = re.search(r'#{1,2}\s+Risk(.+?)(?=^#{1,2}|\Z)', 
                                self.content, re.MULTILINE | re.DOTALL)
        
        if risk_section:
            risks = len(re.findall(r'\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|', risk_section.group(1)))
            if risks < 5:
                line_num = self.content[:risk_section.start()].count('\n') + 1
                self.suggestions["medium_priority"].append({
                    "line": line_num,
                    "issue": f"Only {risks} risks identified",
                    "suggestion": "Consider additional risk categories",
                    "example": """Common risks to consider:
- Technical: Performance, scalability, integration
- Schedule: Dependencies, resource availability
- Security: Data breaches, vulnerabilities
- Business: Market changes, user adoption"""
                })
                
    def _check_architecture_detail(self):
        """Check architecture section detail"""
        print("\n🏗️  Checking architecture detail...")
        
        # Check for deployment architecture
        if "deploy" not in self.content.lower():
            self.suggestions["medium_priority"].append({
                "line": 0,
                "issue": "No deployment architecture described",
                "suggestion": "Add deployment architecture section",
                "example": """Add section:
### Deployment Architecture
- Environment strategy (dev/staging/prod)
- Container orchestration
- Scaling approach
- Monitoring and logging"""
            })
            
    def _check_timeline_detail(self):
        """Check timeline specificity"""
        print("\n📅 Checking timeline detail...")
        
        # Look for vague timeline terms
        vague_timeline = re.findall(r'\b(soon|later|eventually|future)\b', self.content, re.IGNORECASE)
        if vague_timeline:
            self.suggestions["high_priority"].append({
                "line": 0,
                "issue": f"Vague timeline terms found: {', '.join(set(vague_timeline))}",
                "suggestion": "Replace with specific dates or durations",
                "example": "Instead of 'future enhancement', use 'Phase 2 (Month 4-6)'"
            })
            
    def _check_success_metrics(self):
        """Check success metrics completeness"""
        print("\n📈 Checking success metrics...")
        
        metrics_section = re.search(r'#{1,2}\s+Success Metrics(.+?)(?=^#{1,2}|\Z)', 
                                   self.content, re.MULTILINE | re.DOTALL)
        
        if metrics_section:
            metrics_content = metrics_section.group(1)
            
            # Check for baseline data
            if "current" not in metrics_content.lower():
                line_num = self.content[:metrics_section.start()].count('\n') + 1
                self.suggestions["high_priority"].append({
                    "line": line_num,
                    "issue": "Success metrics lack baseline data",
                    "suggestion": "Add current state metrics for comparison",
                    "example": "For each metric, show: Current → Target"
                })
                
    def _generate_report(self):
        """Generate improvement report"""
        print("\n" + "="*60)
        print("SPEC IMPROVEMENT SUGGESTIONS")
        print("="*60)
        
        total_suggestions = sum(len(self.suggestions[p]) for p in self.suggestions)
        print(f"\n📊 Found {total_suggestions} improvement opportunities")
        
        # High priority
        if self.suggestions["high_priority"]:
            print(f"\n🔴 HIGH PRIORITY ({len(self.suggestions['high_priority'])} items)")
            print("These significantly impact spec quality and should be addressed first:\n")
            
            for i, suggestion in enumerate(self.suggestions["high_priority"], 1):
                print(f"{i}. Line {suggestion['line']}: {suggestion['issue']}")
                print(f"   📝 {suggestion['suggestion']}")
                print(f"   💡 Example: {suggestion['example']}")
                print()
                
        # Medium priority
        if self.suggestions["medium_priority"]:
            print(f"\n🟡 MEDIUM PRIORITY ({len(self.suggestions['medium_priority'])} items)")
            print("These improve clarity and completeness:\n")
            
            for i, suggestion in enumerate(self.suggestions["medium_priority"], 1):
                print(f"{i}. {suggestion['issue']}")
                print(f"   📝 {suggestion['suggestion']}")
                if len(suggestion['example']) < 100:
                    print(f"   💡 Example: {suggestion['example']}")
                print()
                
        # Low priority  
        if self.suggestions["low_priority"]:
            print(f"\n🟢 LOW PRIORITY ({len(self.suggestions['low_priority'])} items)")
            print("Nice to have improvements:\n")
            
            for i, suggestion in enumerate(self.suggestions["low_priority"], 1):
                print(f"{i}. {suggestion['issue']}")
                print(f"   📝 {suggestion['suggestion']}")
                print()
                
        # Quick wins
        print("\n⚡ QUICK WINS (< 30 minutes to implement):")
        print("1. Add specific metrics to all vague terms")
        print("2. Include acceptance criteria for each requirement")
        print("3. Add timeline with specific milestones")
        print("4. Quantify all improvement goals with percentages")
        
        # Save detailed report
        report_path = self.spec_path.parent / "improvement-suggestions.md"
        with open(report_path, 'w') as f:
            f.write(f"# Spec Improvement Suggestions\n\n")
            f.write(f"Generated for: {self.spec_path.name}\n\n")
            
            for priority in ["high_priority", "medium_priority", "low_priority"]:
                if self.suggestions[priority]:
                    f.write(f"## {priority.replace('_', ' ').title()}\n\n")
                    for s in self.suggestions[priority]:
                        f.write(f"- **Issue**: {s['issue']}\n")
                        f.write(f"  - **Suggestion**: {s['suggestion']}\n")
                        f.write(f"  - **Example**: {s['example']}\n\n")
                        
        print(f"\n📄 Detailed suggestions saved to: {report_path}")
        print("="*60)

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python suggest-spec-improvements.py <path-to-SPEC.md>")
        sys.exit(1)
        
    spec_path = sys.argv[1]
    analyzer = ImprovementAnalyzer(spec_path)
    analyzer.analyze()

if __name__ == "__main__":
    main()