#!/usr/bin/env python3
"""
Comprehensive Web Security Scanner
Identifies all files that are accessible via web but shouldn't be for security reasons.
"""

import requests
import sys
import os
from urllib.parse import urljoin

def test_file_access(base_url, file_path):
    """Test if a file is accessible via web"""
    url = urljoin(base_url, file_path)
    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except requests.RequestException:
        return 0  # Network error

def find_sensitive_files():
    """Find all potentially sensitive files in the repository"""
    sensitive_patterns = [
        # Documentation files
        "*.md", "*.txt", "*.rst",
        # Configuration files  
        "*.json", "*.yml", "*.yaml", "*.xml", "*.cfg", "*.ini", "*.conf",
        # Development files
        "*.sh", "*.py", "*.js", "Gruntfile*", "bower.json", "LICENSE*",
        # Build/source files
        "src/*", "dev-*", "*config*", "*setup*"
    ]
    
    # Comprehensive list of files that should NOT be web accessible
    sensitive_files = [
        # Root level files
        "README.md", "LICENSE", "SECURITY.md", "_config.yml", ".codacy.yml", ".trivyignore",
        ".gitignore", ".gitattributes", ".htaccess",
        
        # GitHub directory (should all be protected)
        ".github/workflows/codacy.yml", ".github/workflows/static.yml", 
        ".github/workflows/validate-website.yml", ".github/workflows/label.yml",
        ".github/dependabot.yml", ".github/labeler.yml",
        ".github/config/requirements.txt", ".github/config/genWordCloud.py", ".github/config/genPubHTML.sh",
        
        # Assets documentation and config files
        "assets/HELP-US-OUT.txt", "assets/img/Developer-ReadMe.txt", "assets/img/faviconit-instructions.txt",
        "assets/docs/publications/README.md", "assets/docs/publications/generate.sh", 
        "assets/js/README.md", "assets/js/dev-package.json", "assets/js/dev-Gruntfile.js",
        "assets/plugins/github-activity/README.md", "assets/plugins/github-activity/LICENSE.md",
        "assets/plugins/github-activity/dev-package.json", "assets/plugins/github-activity/bower.json",
        "assets/plugins/github-activity/Gruntfile.js",
        
        # Configuration and build files
        "assets/img/browserconfig.xml", "package.json", "composer.json", ".env",
        
        # Source files (should be minified versions only)
        "assets/js/src/csi.js", "assets/plugins/github-activity/src/github-activity.js"
    ]
    
    return sensitive_files

def categorize_files(files):
    """Categorize files by type for better analysis"""
    categories = {
        "documentation": [],
        "configuration": [], 
        "development": [],
        "source_code": [],
        "build_files": [],
        "other": []
    }
    
    for file in files:
        if any(x in file.lower() for x in ["readme", "license", "help", "instruction"]):
            categories["documentation"].append(file)
        elif any(x in file.lower() for x in ["config", "yml", "yaml", "json", "xml", "ini", "cfg"]):
            categories["configuration"].append(file)
        elif any(x in file.lower() for x in ["dev-", "grunt", "bower", "package"]):
            categories["development"].append(file)
        elif "src/" in file or file.endswith((".py", ".sh")):
            categories["source_code"].append(file)
        elif any(x in file.lower() for x in ["build", "dist", "generate"]):
            categories["build_files"].append(file)
        else:
            categories["other"].append(file)
    
    return categories

def main():
    """Run comprehensive security scan"""
    base_url = "https://prajitdas.github.io/"
    sensitive_files = find_sensitive_files()
    
    print("🔍 COMPREHENSIVE WEB SECURITY SCANNER")
    print("=" * 60)
    print(f"Target: {base_url}")
    print(f"Files to test: {len(sensitive_files)}")
    print("=" * 60)
    
    accessible_files = []
    protected_files = []
    
    # Test each file
    for file_path in sensitive_files:
        status_code = test_file_access(base_url, file_path)
        
        if status_code == 200:
            print(f"❌ {file_path:<50} -> {status_code} (ACCESSIBLE - SECURITY RISK!)")
            accessible_files.append(file_path)
        elif status_code == 404 or status_code == 403:
            print(f"✅ {file_path:<50} -> {status_code} (Protected)")
            protected_files.append(file_path)
        else:
            print(f"⚠️  {file_path:<50} -> {status_code} (Unknown/Error)")
    
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE SECURITY ANALYSIS")
    print("=" * 60)
    
    # Categorize accessible files for analysis
    if accessible_files:
        categories = categorize_files(accessible_files)
        
        print("\n🚨 ACCESSIBLE FILES BY CATEGORY:")
        for category, files in categories.items():
            if files:
                print(f"\n📁 {category.upper().replace('_', ' ')} ({len(files)} files):")
                for file in files:
                    print(f"   - {file}")
    
    print(f"\n📈 SECURITY SUMMARY:")
    print(f"   ✅ Protected files: {len(protected_files)}")
    print(f"   ❌ Accessible files: {len(accessible_files)}")
    print(f"   📊 Total tested: {len(sensitive_files)}")
    print(f"   🛡️ Protection rate: {len(protected_files)/len(sensitive_files)*100:.1f}%")
    
    if accessible_files:
        print(f"\n⚠️  WARNING: {len(accessible_files)} files are accessible and may need protection!")
        return 1
    else:
        print(f"\n🎉 EXCELLENT: All sensitive files are properly protected!")
        return 0

if __name__ == "__main__":
    sys.exit(main())