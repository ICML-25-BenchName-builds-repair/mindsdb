import subprocess
import sys

def check_dependency_usage():
    """Check if sentence-transformers is used in the rag_handler code."""
    try:
        # Run grep to check for imports of sentence-transformers
        result = subprocess.run(
            "grep -r 'sentence-transformers\|sentence_transformers' mindsdb/integrations/handlers/rag_handler/ --include='*.py'",
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Check if there are any matches in Python files
        if result.stdout:
            print("Found usage of sentence-transformers in Python files:")
            print(result.stdout.decode())
            return True
        else:
            print("No direct usage of sentence-transformers found in Python files.")
            return False
    except Exception as e:
        print(f"Error checking dependency: {e}")
        return False

if __name__ == "__main__":
    if not check_dependency_usage():
        print("The dependency 'sentence-transformers' is listed in requirements.txt but not used directly in the code.")
        sys.exit(1)
    else:
        print("The dependency 'sentence-transformers' is used in the code.")
        sys.exit(0)