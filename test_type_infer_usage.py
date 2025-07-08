"""
Test script to verify if type_infer is used in the codebase.
"""
import os
import sys
import subprocess

def check_type_infer_usage():
    """Check if type_infer is used in the codebase."""
    # Check if type_infer is in requirements.txt
    with open('requirements/requirements.txt', 'r') as f:
        requirements = f.read()
        if 'type_infer' in requirements:
            print("type_infer is listed in requirements/requirements.txt")
        else:
            print("type_infer is NOT listed in requirements/requirements.txt")
    
    # Check if type_infer is imported in any Python files
    result = subprocess.run(
        "grep -r 'from type_infer' --include='*.py' .",
        shell=True, capture_output=True, text=True
    )
    
    if result.stdout:
        print("\ntype_infer is imported in the following files:")
        print(result.stdout)
    else:
        print("\ntype_infer is NOT imported in any Python files")
    
    # Check if any handler requirements include type_infer
    handler_requirements = []
    for root, dirs, files in os.walk('mindsdb/integrations/handlers'):
        for file in files:
            if file.startswith('requirements') and file.endswith('.txt'):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    if 'type_infer' in content:
                        handler_requirements.append(os.path.join(root, file))
    
    if handler_requirements:
        print("\ntype_infer is listed in the following handler requirements files:")
        for req_file in handler_requirements:
            print(f"- {req_file}")
    else:
        print("\ntype_infer is NOT listed in any handler requirements files")

if __name__ == "__main__":
    check_type_infer_usage()