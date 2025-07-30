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