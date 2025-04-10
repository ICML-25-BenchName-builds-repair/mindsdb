#!/usr/bin/env python3
"""
Test script to verify the requirements issue.
"""

import os
import re
import subprocess

def get_requirements_from_file(path):
    """Takes a requirements file path and extracts only the package names from it"""
    pattern = r'=|~|>|<| |\n|#|\['
    with open(path, 'r') as main_f:
        reqs = [
            re.split(pattern, line)[0]
            for line in main_f.readlines()
            if re.split(pattern, line)[0]
        ]
    return reqs

def find_imports_using_grep(package_name, directory='.', exclude_dirs=None):
    """Use grep to find imports of a specific package"""
    if exclude_dirs:
        exclude_args = ' '.join([f'--exclude-dir={d}' for d in exclude_dirs])
    else:
        exclude_args = ''
    
    cmd = f"grep -r 'from {package_name}' --include='*.py' {exclude_args} {directory}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        imports_from = result.stdout.strip().split('\n') if result.stdout.strip() else []
    except Exception as e:
        print(f"Error running grep for 'from {package_name}': {e}")
        imports_from = []
    
    cmd = f"grep -r 'import {package_name}' --include='*.py' {exclude_args} {directory}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        imports_import = result.stdout.strip().split('\n') if result.stdout.strip() else []
    except Exception as e:
        print(f"Error running grep for 'import {package_name}': {e}")
        imports_import = []
    
    return imports_from + imports_import

def main():
    # Path to the main requirements file
    main_reqs_path = "requirements/requirements.txt"
    
    # Get the list of packages from the main requirements file
    main_reqs = get_requirements_from_file(main_reqs_path)
    
    # Check for 'type_infer' in the requirements
    if 'type_infer' in main_reqs:
        print("'type_infer' is in the main requirements.txt file")
    else:
        print("'type_infer' is NOT in the main requirements.txt file")
    
    # Find all files that import 'type_infer' in the core codebase
    core_imports = find_imports_using_grep('type_infer', 'mindsdb', ['mindsdb/integrations/handlers'])
    
    if core_imports and core_imports != ['']:
        print("\nFound 'type_infer' imports in core codebase:")
        for line in core_imports:
            if line:  # Skip empty lines
                print(f"  - {line}")
    else:
        print("\nNo 'type_infer' imports found in core codebase")
    
    # Find all files in handlers that import 'type_infer'
    handler_imports = find_imports_using_grep('type_infer', 'mindsdb/integrations/handlers')
    
    if handler_imports and handler_imports != ['']:
        print("\nFound 'type_infer' imports in handlers:")
        for line in handler_imports:
            if line:  # Skip empty lines
                print(f"  - {line}")
    else:
        print("\nNo 'type_infer' imports found in handlers")

if __name__ == "__main__":
    main()