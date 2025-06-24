#!/usr/bin/env python3
"""
Script to reproduce the CI requirements check issue.
"""

import subprocess
import sys
import os

def run_requirements_check():
    """Run the requirements check script and capture output."""
    print("Running requirements check...")
    
    try:
        result = subprocess.run(
            [sys.executable, "tests/scripts/check_requirements.py"],
            capture_output=True,
            text=True,
            cwd="/lca-workspace/repos/mindsdb__mindsdb"
        )
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running requirements check: {e}")
        return False

if __name__ == "__main__":
    print("=== Reproducing CI Requirements Check Issue ===")
    success = run_requirements_check()
    
    if success:
        print("\n✅ Requirements check passed!")
    else:
        print("\n❌ Requirements check failed!")
        
    sys.exit(0 if success else 1)