#!/usr/bin/env python3
"""
Quick test runner for local development
Run website validation tests with simple output
"""

import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run the website validation tests"""
    test_dir = Path(__file__).parent
    test_file = test_dir / "test_website_validation.py"
    
    if not test_file.exists():
        print("❌ Test file not found!")
        return 1
    
    print("🔍 Running Website Validation Tests...")
    print("=" * 50)
    
    try:
        # Try to run with pytest first
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            str(test_file), "-v", "--tb=short"
        ], cwd=test_dir)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed!")
            
        return result.returncode
        
    except FileNotFoundError:
        # Fallback to unittest if pytest not available
        print("pytest not found, using unittest...")
        result = subprocess.run([
            sys.executable, str(test_file)
        ], cwd=test_dir)
        
        return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)