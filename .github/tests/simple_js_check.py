#!/usr/bin/env python3
"""
Simple JavaScript Runtime Test
==============================
Quick test to verify JavaScript runtime error detection works
"""

import sys
import subprocess

def test_chrome_availability():
    """Test if Chrome/Chromium is available for Selenium"""
    try:
        # Check for Chrome
        result = subprocess.run(['which', 'google-chrome'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Found Chrome at: {result.stdout.strip()}")
            return True
        
        # Check for Chromium
        result = subprocess.run(['which', 'chromium'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Found Chromium at: {result.stdout.strip()}")
            return True
        
        # Check for Safari (WebKit)
        result = subprocess.run(['which', 'safaridriver'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Found Safari WebDriver at: {result.stdout.strip()}")
            return True
            
        print("❌ No suitable browser found for Selenium testing")
        return False
        
    except Exception as e:
        print(f"❌ Error checking browser availability: {e}")
        return False

def simple_js_test():
    """Simple test without browser - just check if JS files have syntax errors"""
    import os
    import re
    from pathlib import Path
    
    print("🔍 Checking JavaScript files for obvious syntax issues...")
    
    base_path = Path(__file__).parent.parent.parent
    js_files = [
        base_path / 'assets' / 'js' / 'critical.js',
        base_path / 'assets' / 'js' / 'deferred.js'
    ]
    
    errors = []
    
    for js_file in js_files:
        if js_file.exists():
            print(f"  📄 Checking {js_file.name}...")
            
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic syntax checks
            issues = []
            
            # Check for const reassignment patterns
            const_pattern = r'const\s+(\w+)\s*='
            const_matches = re.findall(const_pattern, content)
            
            for const_var in const_matches:
                reassign_pattern = rf'{const_var}\s*='
                if len(re.findall(reassign_pattern, content)) > 1:
                    issues.append(f"Potential const reassignment: {const_var}")
            
            # Check for common error patterns
            error_patterns = [
                (r'insertBefore\([^,]+,\s*null\)', "insertBefore with null reference"),
                (r'\.remove\(\).*?\w+\s*=', "Using variable after removal"),
                (r'undefined\s*\.\s*\w+', "Accessing property of undefined"),
            ]
            
            for pattern, description in error_patterns:
                if re.search(pattern, content):
                    issues.append(description)
            
            if issues:
                errors.extend([(js_file.name, issue) for issue in issues])
                print(f"    ⚠️ Found {len(issues)} potential issues")
            else:
                print(f"    ✅ No obvious syntax issues found")
        else:
            print(f"  ❌ File not found: {js_file}")
            errors.append((js_file.name, "File not found"))
    
    return errors

def main():
    """Main test function"""
    print("🧪 JavaScript Runtime Testing Check")
    print("=" * 50)
    
    # Check if browsers are available for full testing
    browser_available = test_chrome_availability()
    
    # Run basic syntax checking
    syntax_errors = simple_js_test()
    
    print("\n" + "=" * 50)
    print("📊 RESULTS:")
    
    if syntax_errors:
        print(f"❌ Found {len(syntax_errors)} JavaScript issues:")
        for file, issue in syntax_errors:
            print(f"  - {file}: {issue}")
        return False
    else:
        print("✅ No JavaScript syntax issues detected")
    
    if not browser_available:
        print("⚠️ Browser testing unavailable - install Chrome/Chromium for full JS runtime testing")
        print("\nTo enable full JavaScript runtime error detection:")
        print("  brew install --cask google-chrome")
        print("  # or")
        print("  brew install chromium")
        return True  # Don't fail if browser unavailable
    
    print("✅ Ready for full JavaScript runtime testing with browser")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)