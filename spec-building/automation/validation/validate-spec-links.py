#!/usr/bin/env python3
"""
Validate Spec Cross-References
Ensures all internal links and references in spec documents are valid.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple

class LinkValidator:
    def __init__(self, spec_path: str):
        self.spec_path = Path(spec_path)
        self.spec_dir = self.spec_path.parent
        self.errors = []
        self.warnings = []
        self.valid_links = 0
        self.total_links = 0
        
    def validate(self) -> bool:
        """Run link validation"""
        print(f"🔗 Validating links in: {self.spec_path}")
        
        # Find all markdown files
        md_files = self._find_markdown_files()
        
        # Extract and validate links
        for md_file in md_files:
            self._validate_file_links(md_file)
            
        # Report results
        return self._report_results()
        
    def _find_markdown_files(self) -> List[Path]:
        """Find all markdown files in spec directory"""
        md_files = [self.spec_path]
        
        # Add .spec directory files if exists
        spec_subdir = self.spec_dir / ".spec"
        if spec_subdir.exists():
            md_files.extend(spec_subdir.glob("*.md"))
            
        # Add template files
        template_dir = self.spec_dir / "templates"
        if template_dir.exists():
            md_files.extend(template_dir.glob("*.md"))
            
        return md_files
        
    def _validate_file_links(self, file_path: Path):
        """Validate all links in a single file"""
        print(f"\n📄 Checking links in: {file_path.name}")
        
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Find all markdown links [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, content)
        
        for link_text, link_url in matches:
            self.total_links += 1
            self._validate_single_link(file_path, link_text, link_url)
            
        # Find all reference-style links
        ref_pattern = r'\[([^\]]+)\]\[([^\]]+)\]'
        ref_def_pattern = r'^\[([^\]]+)\]:\s*(.+)$'
        
        # Build reference definitions
        ref_defs = {}
        for match in re.finditer(ref_def_pattern, content, re.MULTILINE):
            ref_defs[match.group(1)] = match.group(2)
            
        # Validate reference links
        for link_text, ref_id in re.findall(ref_pattern, content):
            self.total_links += 1
            if ref_id in ref_defs:
                self._validate_single_link(file_path, link_text, ref_defs[ref_id])
            else:
                self.errors.append(f"Undefined reference '{ref_id}' in {file_path.name}")
                
    def _validate_single_link(self, source_file: Path, link_text: str, link_url: str):
        """Validate a single link"""
        # Skip external links
        if link_url.startswith(('http://', 'https://', 'mailto:')):
            self.valid_links += 1
            return
            
        # Handle anchor links
        if link_url.startswith('#'):
            # Check if anchor exists in current file
            anchor = link_url[1:].lower().replace(' ', '-')
            with open(source_file, 'r') as f:
                content = f.read().lower()
                if anchor not in content:
                    self.warnings.append(
                        f"Anchor '{link_url}' not found in {source_file.name}"
                    )
                else:
                    self.valid_links += 1
            return
            
        # Handle relative file links
        if '#' in link_url:
            file_part, anchor_part = link_url.split('#', 1)
        else:
            file_part = link_url
            anchor_part = None
            
        # Resolve relative path
        target_path = (source_file.parent / file_part).resolve()
        
        # Check if file exists
        if not target_path.exists():
            self.errors.append(
                f"Broken link '{link_url}' in {source_file.name} - file not found"
            )
        else:
            # If anchor specified, check it exists
            if anchor_part:
                anchor = anchor_part.lower().replace(' ', '-')
                with open(target_path, 'r') as f:
                    content = f.read().lower()
                    if anchor not in content:
                        self.warnings.append(
                            f"Anchor '#{anchor_part}' not found in {target_path.name}"
                        )
                    else:
                        self.valid_links += 1
            else:
                self.valid_links += 1
                print(f"  ✅ Valid link: {link_text} → {file_part}")
                
    def _report_results(self) -> bool:
        """Report validation results"""
        print("\n" + "="*60)
        print("LINK VALIDATION RESULTS")
        print("="*60)
        
        print(f"\n📊 Statistics:")
        print(f"  Total links found: {self.total_links}")
        print(f"  Valid links: {self.valid_links}")
        print(f"  Invalid links: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
                
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
                
        if not self.errors and not self.warnings:
            print("\n✅ All links are valid!")
            
        print("\n" + "="*60)
        
        # Return True only if no errors
        return len(self.errors) == 0

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python validate-spec-links.py <path-to-SPEC.md>")
        sys.exit(1)
        
    spec_path = sys.argv[1]
    validator = LinkValidator(spec_path)
    
    if validator.validate():
        print("\n✅ Link validation PASSED")
        sys.exit(0)
    else:
        print("\n❌ Link validation FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()