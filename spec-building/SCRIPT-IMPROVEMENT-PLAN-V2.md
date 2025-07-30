# Automation Script Improvement Plan v2.0

## Overview

This plan takes a pragmatic, MVP-first approach to improving the spec-building automation scripts. We focus on high-impact improvements that can be implemented quickly while maintaining backward compatibility.

## Core Principles

1. **Preserve What Works** - Don't break existing functionality
2. **MVP First** - Get basic improvements working before advanced features
3. **Incremental Enhancement** - Each script should be independently improved
4. **Practical Over Perfect** - 80/20 rule applies

## Priority Matrix

| Script | Current Grade | Target Grade | Impact | Effort | Priority |
|--------|--------------|--------------|--------|--------|----------|
| generate-spec-template.py | C (70) | B+ (88) | HIGH | LOW | P1 |
| score-spec-quality.py | B (80) | A- (90) | HIGH | MEDIUM | P1 |
| validate-spec-structure.py | B- (78) | B+ (88) | MEDIUM | LOW | P2 |
| suggest-spec-improvements.py | C (70) | B (85) | HIGH | MEDIUM | P2 |
| validate-alignment.py | C+ (75) | B (85) | LOW | LOW | P3 |

## Implementation Phases

### Phase 1: Quick Wins (Day 1-2)
**Goal**: Add basic CLI and error handling to all scripts

1. **Create Minimal Base Class** (`automation/lib/base.py`):
```python
#!/usr/bin/env python3
"""Base utilities for spec automation tools."""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

class SpecTool:
    """Minimal base class for spec tools."""
    
    VERSION = "1.0.0"
    DESCRIPTION = "Spec automation tool"
    
    def __init__(self):
        self.args = None
        
    def create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with common options."""
        parser = argparse.ArgumentParser(
            description=self.DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self.get_examples()
        )
        parser.add_argument('--version', action='version', 
                          version=f'%(prog)s {self.VERSION}')
        return parser
    
    def get_examples(self) -> str:
        """Override to provide usage examples."""
        return ""
        
    def setup_logging(self):
        """Configure logging based on verbosity."""
        # Simple print-based logging for now
        pass
        
    def run(self, argv: Optional[List[str]] = None) -> int:
        """Main entry point."""
        try:
            parser = self.create_parser()
            self.args = parser.parse_args(argv)
            return self.execute()
        except KeyboardInterrupt:
            print("\n✗ Cancelled by user", file=sys.stderr)
            return 130
        except FileNotFoundError as e:
            print(f"✗ File not found: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            return 1
            
    def execute(self) -> int:
        """Override this method in subclasses."""
        raise NotImplementedError()
```

2. **Update Each Script** with:
   - Proper argument parsing
   - Basic error handling
   - Help text and examples
   - Progress indicators

### Phase 2: Core Improvements (Day 3-4)
**Goal**: Improve the most impactful scripts

1. **generate-spec-template.py**:
   - Move templates to separate files (plain markdown, not Jinja2)
   - Add template selection (--template basic|standard|comprehensive)
   - Better progress output
   - Create .gitignore and README automatically

2. **score-spec-quality.py**:
   - Add --format json|markdown option
   - Show specific improvement suggestions
   - Add --strict mode (90+ required)
   - Better scoring explanations

### Phase 3: Enhanced Functionality (Day 5)
**Goal**: Add the most requested features

1. **All Scripts**:
   - Add --output-file option
   - Support reading from stdin
   - Add --quiet and --verbose modes
   - Consistent exit codes

2. **validate-all.py**:
   - Show combined summary
   - Run scripts in parallel
   - Generate unified report

## Concrete Implementation Example

Here's how we'll improve `generate-spec-template.py`:

```python
#!/usr/bin/env python3
"""
Generate comprehensive spec templates for new projects.

This tool creates a complete specification structure with all required
templates and documentation to ensure high-quality specs from the start.
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.base import SpecTool

class SpecTemplateGenerator(SpecTool):
    """Generate spec templates with best practices built in."""
    
    VERSION = "2.0.0"
    DESCRIPTION = "Generate comprehensive spec templates for new projects"
    
    # Template sets available
    TEMPLATES = {
        'basic': 'Minimal spec structure for simple projects',
        'standard': 'Standard spec with all recommended sections (default)',
        'comprehensive': 'Full enterprise spec with compliance sections'
    }
    
    def create_parser(self):
        parser = super().create_parser()
        parser.add_argument('project_name', 
                          help='Name of the project')
        parser.add_argument('-o', '--output-dir', default='.',
                          help='Output directory (default: current directory)')
        parser.add_argument('-t', '--template', 
                          choices=list(self.TEMPLATES.keys()),
                          default='standard',
                          help='Template set to use')
        parser.add_argument('--list-templates', action='store_true',
                          help='List available templates and exit')
        parser.add_argument('--force', action='store_true',
                          help='Overwrite existing directory')
        return parser
        
    def get_examples(self):
        return """
Examples:
  # Create standard spec for "My API"
  %(prog)s "My API"
  
  # Use comprehensive template in specific directory
  %(prog)s "Enterprise System" -o ./specs -t comprehensive
  
  # List available templates
  %(prog)s --list-templates
"""
    
    def execute(self) -> int:
        if self.args.list_templates:
            return self.list_templates()
            
        # Validate inputs
        project_dir = Path(self.args.output_dir) / self.args.project_name.lower().replace(' ', '-')
        
        if project_dir.exists() and not self.args.force:
            print(f"✗ Directory already exists: {project_dir}")
            print("  Use --force to overwrite")
            return 1
            
        # Create structure
        print(f"🚀 Creating {self.args.template} spec structure for: {self.args.project_name}")
        self.create_structure(project_dir)
        
        print(f"\n✅ Spec structure created successfully!")
        print(f"\n📝 Next steps:")
        print(f"  1. cd {project_dir}")
        print(f"  2. Review README.md for guidance")
        print(f"  3. Complete templates in order")
        print(f"  4. Run validation: python3 {Path(__file__).parent}/validate-all.py .")
        
        return 0
        
    def list_templates(self) -> int:
        print("Available template sets:\n")
        for name, desc in self.TEMPLATES.items():
            default = " (default)" if name == "standard" else ""
            print(f"  {name}{default}")
            print(f"    {desc}\n")
        return 0
        
    def create_structure(self, project_dir: Path):
        # Load template files from automation/templates/{template_name}/
        template_dir = Path(__file__).parent / 'templates' / self.args.template
        
        if not template_dir.exists():
            # Fallback to embedded templates for now
            self.create_embedded_structure(project_dir)
        else:
            # Copy template structure
            shutil.copytree(template_dir, project_dir, dirs_exist_ok=True)
            
        # Customize with project name
        self.customize_templates(project_dir)
            
    def create_embedded_structure(self, project_dir: Path):
        """Create structure with embedded templates."""
        # ... existing implementation but organized better
        pass
        
    def customize_templates(self, project_dir: Path):
        """Replace placeholders with project-specific values."""
        replacements = {
            '{{PROJECT_NAME}}': self.args.project_name,
            '{{DATE}}': datetime.now().strftime('%Y-%m-%d'),
            '{{TEMPLATE_TYPE}}': self.args.template
        }
        
        for md_file in project_dir.glob('**/*.md'):
            content = md_file.read_text()
            for old, new in replacements.items():
                content = content.replace(old, new)
            md_file.write_text(content)

def main():
    tool = SpecTemplateGenerator()
    sys.exit(tool.run())

if __name__ == '__main__':
    main()
```

## Success Criteria

Each improved script must:

1. **Functionality** ✓
   - Preserves all current features
   - Adds requested improvements
   - No regressions

2. **Usability** ✓
   - Has --help with examples
   - Clear error messages
   - Progress indicators for long operations

3. **Code Quality** ✓
   - Docstrings for module and classes
   - Type hints on public methods
   - Error handling for common cases

4. **Testing** ✓
   - Manual test checklist provided
   - Key functions have unit tests
   - Integration test script

## Validation Checklist

For each script, verify:

- [ ] `python3 script.py --help` shows useful help
- [ ] `python3 script.py --version` shows version
- [ ] Missing file error is handled gracefully
- [ ] Ctrl+C exits cleanly
- [ ] Output is professional and clear
- [ ] Exit codes are consistent (0=success, 1=error)

## Quick Start Implementation

Day 1 Morning:
1. Create lib/base.py (30 min)
2. Update generate-spec-template.py (2 hours)
3. Test thoroughly (30 min)

Day 1 Afternoon:
1. Update score-spec-quality.py (2 hours)
2. Update validate-spec-structure.py (1 hour)
3. Test all changes (1 hour)

Day 2:
1. Update remaining scripts (3 hours)
2. Create template files (2 hours)
3. Write integration tests (2 hours)
4. Documentation updates (1 hour)

Total: ~16 hours of focused work

## Notes

- Start with generate-spec-template.py as it's the entry point
- Keep changes backward compatible
- Test each script independently
- Document behavior changes in each script's docstring