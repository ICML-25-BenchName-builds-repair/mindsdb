#!/usr/bin/env python3
"""
This script checks if the type_infer package is used in the core codebase.
"""

import os
import re
import sys

def check_imports(directory, exclude_dirs=None):
    """
    Check if type_infer is imported in any Python files in the given directory.
    
    Args:
        directory (str): Directory to search in
        exclude_dirs (list): List of directories to exclude
        
    Returns:
        list: List of files that import type_infer
    """
    if exclude_dirs is None:
        exclude_dirs = []
    
    files_with_imports = []
    
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if re.search(r'import\s+type_infer|from\s+type_infer', content):
                        files_with_imports.append(file_path)
    
    return files_with_imports

def main():
    # Check core codebase (excluding handlers)
    core_files = check_imports('mindsdb', exclude_dirs=['mindsdb/integrations/handlers'])
    
    # Check handlers
    handler_files = check_imports('mindsdb/integrations/handlers')
    
    print("Files in core codebase that import type_infer:")
    for file in core_files:
        print(f"  - {file}")
    
    print("\nFiles in handlers that import type_infer:")
    for file in handler_files:
        print(f"  - {file}")
    
    # Check if type_infer is in main requirements.txt
    with open('requirements/requirements.txt', 'r') as f:
        requirements = f.read()
        if 'type_infer' in requirements:
            print("\ntype_infer is listed in requirements/requirements.txt")
    
    # Check if type_infer is in handler requirements.txt files
    for file in handler_files:
        handler_dir = os.path.dirname(file)
        req_file = os.path.join(handler_dir, 'requirements.txt')
        if os.path.exists(req_file):
            with open(req_file, 'r') as f:
                requirements = f.read()
                if 'type_infer' not in requirements:
                    print(f"\nHandler {handler_dir} uses type_infer but doesn't list it in requirements.txt")

if __name__ == "__main__":
    main()