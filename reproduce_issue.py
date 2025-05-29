#!/usr/bin/env python3
"""
Script to reproduce the sentence-transformers dependency issue in rag_handler
"""

import subprocess
import sys
import os

def run_check_requirements():
    """Run the check_requirements.py script and capture output"""
    print("Running check_requirements.py script...")
    
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
        
        # Check if the specific error is present
        if "DEP002 'sentence-transformers' defined as a dependency but not used in the codebase" in result.stdout:
            print("\n✓ Successfully reproduced the issue!")
            return True
        else:
            print("\n✗ Issue not reproduced")
            return False
            
    except Exception as e:
        print(f"Error running script: {e}")
        return False

def test_sentence_transformers_usage():
    """Test if sentence-transformers is actually needed by HuggingFaceEmbeddings"""
    print("\nTesting if sentence-transformers is actually needed...")
    
    try:
        # Try to use HuggingFaceEmbeddings without sentence-transformers
        test_code = """
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    model = HuggingFaceEmbeddings(model_name='BAAI/bge-base-en')
    print('SUCCESS: HuggingFaceEmbeddings works without sentence-transformers')
except Exception as e:
    if 'sentence_transformers' in str(e):
        print('CONFIRMED: sentence-transformers is required by HuggingFaceEmbeddings')
        print(f'Error: {e}')
    else:
        print(f'OTHER ERROR: {e}')
"""
        
        result = subprocess.run(
            [sys.executable, "-c", test_code],
            capture_output=True,
            text=True
        )
        
        print("Test output:")
        print(result.stdout)
        if result.stderr:
            print("Test stderr:")
            print(result.stderr)
            
        return "sentence_transformers is required" in result.stdout or "CONFIRMED: sentence-transformers is required" in result.stdout
        
    except Exception as e:
        print(f"Error testing sentence-transformers usage: {e}")
        return False

if __name__ == "__main__":
    print("=== Reproducing sentence-transformers dependency issue ===")
    
    # Test 1: Reproduce the CI failure
    issue_reproduced = run_check_requirements()
    
    # Test 2: Confirm sentence-transformers is actually needed
    actually_needed = test_sentence_transformers_usage()
    
    print("\n=== Summary ===")
    print(f"Issue reproduced: {issue_reproduced}")
    print(f"sentence-transformers actually needed: {actually_needed}")
    
    if issue_reproduced and actually_needed:
        print("\n✓ Issue confirmed: sentence-transformers is needed but not directly imported")
        sys.exit(1)  # Exit with error to indicate issue exists
    else:
        print("\n✗ Issue not confirmed")
        sys.exit(0)