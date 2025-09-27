#!/usr/bin/env python3
"""
Comprehensive Web Security Scanner
Tests all potentially sensitive files for web accessibility
"""

import requests
import sys
import os
from urllib.parse import urljoin
from pathlib import Path

def test_file_access(base_url, files_to_test):
    """Test that sensitive files return 403/404 errors"""
    
    print(f"🔐 Comprehensive Security Test for: {base_url}")
    print("=" * 70)
    print("ℹ️  Testing all potentially sensitive files...")
    print("=" * 70)
    
    results = []
    accessible_files = []
    protected_files = []
    
    for file_path in files_to_test:
        url = urljoin(base_url, file_path)
        
        try:
            response = requests.get(url, timeout=10)
            status = response.status_code
            
            if status == 200:
                print(f"❌ {file_path:<40} -> {status} (ACCESSIBLE - SECURITY RISK!)")
                accessible_files.append(file_path)
            elif status in [403, 404]:
                print(f"✅ {file_path:<40} -> {status} (Protected)")
                protected_files.append(file_path)
            else:
                print(f"⚠️  {file_path:<40} -> {status} (Unexpected response)")
            
            results.append((file_path, status))
            
        except requests.RequestException as e:
            print(f"❓ {file_path:<40} -> ERROR ({str(e)[:30]}...)")
            results.append((file_path, "ERROR"))
    
    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE SECURITY SUMMARY:")
    print(f"   Protected files: {len(protected_files)}")
    print(f"   Accessible files: {len(accessible_files)}")
    print(f"   Total tested: {len(files_to_test)}")
    
    if accessible_files:
        print(f"\n⚠️ WARNING: {len(accessible_files)} files are accessible and may need protection!")
        print("\n🚨 ACCESSIBLE FILES THAT NEED REVIEW:")
        for file in accessible_files:
            print(f"   - {file}")
        return False
    else:
        print("\n🎉 SUCCESS: All sensitive files are properly protected!")
        return True

def discover_files():
    """Discover all potentially sensitive files in the repository"""
    
    # Get current directory
    repo_root = Path(".")
    
    sensitive_patterns = [
        # Development files
        "*.py", "*.sh", "*.js", "*.json", "*.yml", "*.yaml",
        # Documentation that might reveal structure
        "*.md", "*.txt", "*.xml", 
        # Configuration files
        "*.cfg", "*.ini", "*.conf", "*.config",
        # License and security files
        "LICENSE*", "SECURITY*", "MANIFEST*",
        # Build files
        "Gruntfile*", "gulpfile*", "webpack*", "rollup*",
        # Package managers
        "package*.json", "composer.json", "Pipfile*", "setup.py",
    ]
    
    all_files = []
    
    # Find files matching patterns
    for pattern in sensitive_patterns:
        files = list(repo_root.rglob(pattern))
        for file in files:
            # Skip .git directory and other hidden directories we don't serve
            if not any(part.startswith('.git') for part in file.parts):
                # Convert to relative path string
                rel_path = str(file.relative_to(repo_root))
                all_files.append(rel_path)
    
    # Remove duplicates and sort
    return sorted(list(set(all_files)))

def main():
    """Run comprehensive security test"""
    
    # Base URL for testing
    base_url = "https://prajitdas.github.io/"
    
    print("🔍 COMPREHENSIVE WEB SECURITY SCAN")
    print("=" * 50)
    
    # Discover all potentially sensitive files
    print("📁 Discovering potentially sensitive files...")
    discovered_files = discover_files()
    
    print(f"📋 Found {len(discovered_files)} files to test:")
    for file in discovered_files[:10]:  # Show first 10
        print(f"   - {file}")
    if len(discovered_files) > 10:
        print(f"   ... and {len(discovered_files) - 10} more files")
    
    print(f"\n🔍 Testing all {len(discovered_files)} files...")
    print("=" * 50)
    
    # Test all discovered files
    success = test_file_access(base_url, discovered_files)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
