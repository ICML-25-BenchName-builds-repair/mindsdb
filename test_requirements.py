#!/usr/bin/env python3
"""
This script tests if the requirements.txt file contains any dependencies that are not used in the codebase.
"""

import subprocess
import sys
import json
import os

def main():
    print("Running deptry to check for unused dependencies...")
    
    # Create a temporary file for deptry output
    if os.path.exists("deptry.json"):
        os.remove("deptry.json")
    
    result = subprocess.run(
        "deptry -o deptry.json --no-ansi --known-first-party mindsdb --requirements-txt requirements/requirements.txt --extend-exclude \"mindsdb/integrations/handlers/.*_handler|pryproject.toml\" .",
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    
    stderr = result.stderr.decode('utf-8')
    if stderr:
        print(f"Error: {stderr}")
    
    if not os.path.exists("deptry.json"):
        print("Error: deptry.json not created")
        return 1
    
    with open("deptry.json", "r") as f:
        deptry_results = json.loads(f.read())
    
    for r in deptry_results:
        print(f"{r['location']['line']}:{r['location']['column']}: {r['error']['code']} {r['error']['message']}")
    
    # Check if type_infer is in the unused dependencies
    type_infer_unused = False
    for r in deptry_results:
        if r['error']['code'] == 'DEP002' and 'type_infer' in r['error']['message']:
            type_infer_unused = True
            print("Issue found: 'type_infer' is defined as a dependency but not used in the codebase")
    
    # Clean up
    if os.path.exists("deptry.json"):
        os.remove("deptry.json")
    
    return 1 if type_infer_unused else 0

if __name__ == "__main__":
    sys.exit(main())