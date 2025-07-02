#!/usr/bin/env python3
"""
Script to reproduce the type_infer dependency issue.
This script runs the same check that fails in CI.
"""

import subprocess
import sys
import os

def main():
    print("=== Reproducing type_infer dependency issue ===")
    print()
    
    # Change to the repository directory
    os.chdir('/lca-workspace/repos/mindsdb__mindsdb')
    
    print("Running dependency check script...")
    result = subprocess.run([
        sys.executable, 'tests/scripts/check_requirements.py'
    ], capture_output=True, text=True)
    
    print("STDOUT:")
    print(result.stdout)
    print("\nSTDERR:")
    print(result.stderr)
    print(f"\nReturn code: {result.returncode}")
    
    # Check if the specific error is present
    if "DEP002 'type_infer' defined as a dependency but not used in the codebase" in result.stdout:
        print("\n✓ Successfully reproduced the issue!")
        return True
    else:
        print("\n✗ Could not reproduce the issue")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)