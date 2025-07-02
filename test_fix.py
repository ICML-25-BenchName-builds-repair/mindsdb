#!/usr/bin/env python3
"""
Script to test if the type_infer fix worked.
"""

import subprocess
import sys
import os

def main():
    print("=== Testing type_infer fix ===")
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
    
    # Check if the type_infer error is gone
    if "DEP002 'type_infer' defined as a dependency but not used in the codebase" in result.stdout:
        print("\n✗ type_infer issue still exists!")
        return False
    else:
        print("\n✓ type_infer issue is fixed!")
        
    # Check if there are any other errors
    if result.returncode != 0:
        print("⚠️  There are still other dependency issues to resolve")
        return False
    else:
        print("✓ All dependency checks passed!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)