#!/usr/bin/env python3
"""
This script checks if the sentence-transformers package is actually used in the RAG handler.
"""

import os
import sys
import importlib.util

def check_import_in_file(file_path, import_name):
    """Check if a specific import is used in a file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check for direct imports
    if f"import {import_name}" in content or f"from {import_name}" in content:
        return True
    
    return False

def check_directory_for_import(directory, import_name):
    """Check all Python files in a directory for a specific import."""
    found_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if check_import_in_file(file_path, import_name):
                    found_files.append(file_path)
    
    return found_files

def check_if_package_used_by_dependency(package_name, dependency_name):
    """Check if a package is used by a dependency."""
    try:
        # Try to import the dependency
        dependency_spec = importlib.util.find_spec(dependency_name)
        if dependency_spec is None:
            return False, f"Dependency {dependency_name} not found"
        
        # Import the dependency
        dependency = importlib.import_module(dependency_name)
        
        # Check if the package is in the dependency's __file__ content
        with open(dependency.__file__, 'r') as f:
            content = f.read()
            if package_name in content:
                return True, f"Package {package_name} is used by {dependency_name}"
        
        return False, f"Package {package_name} is not directly imported by {dependency_name}"
    except Exception as e:
        return False, f"Error checking dependency: {str(e)}"

if __name__ == "__main__":
    rag_handler_dir = "mindsdb/integrations/handlers/rag_handler"
    import_name = "sentence_transformers"
    
    # Check if sentence_transformers is directly imported in any RAG handler files
    found_files = check_directory_for_import(rag_handler_dir, import_name)
    
    if found_files:
        print(f"Found direct imports of {import_name} in the following files:")
        for file in found_files:
            print(f"  - {file}")
    else:
        print(f"No direct imports of {import_name} found in {rag_handler_dir}")
        
        # Check if it's used by HuggingFaceEmbeddings
        try:
            from langchain.embeddings.huggingface import HuggingFaceEmbeddings
            print("Checking if HuggingFaceEmbeddings uses sentence_transformers...")
            
            # Check the source code
            import inspect
            source = inspect.getsource(HuggingFaceEmbeddings)
            if "sentence_transformers" in source:
                print("HuggingFaceEmbeddings uses sentence-transformers")
                print("\nRelevant code snippets:")
                for line in source.split('\n'):
                    if "sentence_transformers" in line:
                        print(f"  {line.strip()}")
            else:
                print("HuggingFaceEmbeddings does not directly use sentence-transformers")
        except ImportError:
            print("Could not import HuggingFaceEmbeddings from langchain")
            
            # Try with langchain_community
            try:
                from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
                print("Checking if HuggingFaceEmbeddings from langchain_community uses sentence_transformers...")
                
                # Check the source code
                import inspect
                source = inspect.getsource(HuggingFaceEmbeddings)
                if "sentence_transformers" in source:
                    print("HuggingFaceEmbeddings uses sentence-transformers")
                    print("\nRelevant code snippets:")
                    for line in source.split('\n'):
                        if "sentence_transformers" in line:
                            print(f"  {line.strip()}")
                else:
                    print("HuggingFaceEmbeddings does not directly use sentence-transformers")
            except ImportError:
                print("Could not import HuggingFaceEmbeddings from langchain_community")
    
    # Check requirements.txt
    requirements_file = f"{rag_handler_dir}/requirements.txt"
    with open(requirements_file, 'r') as f:
        requirements = f.read()
    
    if "sentence-transformers" in requirements:
        print(f"\nFound 'sentence-transformers' in {requirements_file}")
        print("This package is listed but not directly imported in the code.")
        print("It might be used indirectly through HuggingFaceEmbeddings.")
    else:
        print(f"\nDid not find 'sentence-transformers' in {requirements_file}")