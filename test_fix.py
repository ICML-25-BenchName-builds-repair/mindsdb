#!/usr/bin/env python3
"""
Test script to verify the sentence-transformers fix
"""

import subprocess
import sys

def test_fix():
    """Test that the sentence-transformers issue is fixed"""
    print("Testing that sentence-transformers issue is fixed...")
    
    try:
        result = subprocess.run(
            [sys.executable, "tests/scripts/check_requirements.py"],
            capture_output=True,
            text=True,
            cwd="/lca-workspace/repos/mindsdb__mindsdb"
        )
        
        # Check if the specific error is NOT present
        if "DEP002 'sentence-transformers' defined as a dependency but not used in the codebase" in result.stdout:
            print("❌ FAIL: sentence-transformers error still present")
            return False
        else:
            print("✅ PASS: sentence-transformers error is gone")
            
        # Check that sentence-transformers is still in the requirements file
        with open("/lca-workspace/repos/mindsdb__mindsdb/mindsdb/integrations/handlers/rag_handler/requirements.txt", "r") as f:
            content = f.read()
            if "sentence-transformers" in content:
                print("✅ PASS: sentence-transformers still in requirements.txt")
            else:
                print("❌ FAIL: sentence-transformers removed from requirements.txt")
                return False
                
        # Check that sentence-transformers is in the OPTIONAL_HANDLER_DEPS list
        with open("/lca-workspace/repos/mindsdb__mindsdb/tests/scripts/check_requirements.py", "r") as f:
            content = f.read()
            if '"sentence-transformers"' in content and "OPTIONAL_HANDLER_DEPS" in content:
                print("✅ PASS: sentence-transformers added to OPTIONAL_HANDLER_DEPS")
            else:
                print("❌ FAIL: sentence-transformers not properly added to OPTIONAL_HANDLER_DEPS")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing sentence-transformers fix ===")
    
    success = test_fix()
    
    if success:
        print("\n🎉 All tests passed! The fix is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. The fix needs more work.")
        sys.exit(1)