#!/usr/bin/env python3
"""
Quick Website Validation Script
===============================

Fast validation for development - skips external link checking.
Use this for rapid feedback during development.

For full validation, use: python website_validation.py
For quick validation, use: python quick_validation.py
"""

import os
import subprocess
import sys
import time

def main():
    """Run quick validation with performance timing."""
    print("🚀 QUICK WEBSITE VALIDATION")
    print("=" * 50)
    print("⚡ Fast mode: Skipping external link validation")
    print("🔧 Use 'python website_validation.py' for full validation")
    print()
    
    # Set fast mode environment variable
    env = os.environ.copy()
    env['FAST_VALIDATION'] = '1'
    
    start_time = time.time()
    
    # Run validation
    result = subprocess.run([sys.executable, 'website_validation.py'], 
                          env=env, capture_output=False)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print()
    print("⏱️  PERFORMANCE SUMMARY:")
    print("-" * 30)
    print(f"⚡ Quick validation: {duration:.1f}s")
    print(f"🐌 Full validation: ~15-150s (depending on external links)")
    print(f"🚀 Speed improvement: {((150-duration)/150)*100:.0f}% faster")
    
    if result.returncode == 0:
        print("✅ Quick validation passed!")
    else:
        print("❌ Quick validation failed!")
        
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())