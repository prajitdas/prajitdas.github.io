#!/usr/bin/env python3
"""
Web security test to verify sensitive files are not accessible
"""

import requests
import sys
from urllib.parse import urljoin

def test_file_access(base_url, files_to_test):
    """Test that sensitive files return 403/404 errors"""
    
    print(f"🔐 Testing file access security for: {base_url}")
    print("=" * 60)
    print("ℹ️  Note: GitHub Pages may override some .htaccess rules")
    print("=" * 60)
    
    results = []
    
    for file_path in files_to_test:
        url = urljoin(base_url, file_path)
        
        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code
            
            if status_code in [403, 404]:
                results.append((file_path, status_code, "✅ PROTECTED"))
                print(f"✅ {file_path:<25} -> {status_code} (Protected)")
            elif status_code == 200:
                # Check if it's actually blocked by content
                content = response.text.lower()
                if any(block_indicator in content for block_indicator in [
                    'forbidden', 'access denied', '404', 'not found'
                ]):
                    results.append((file_path, status_code, "✅ BLOCKED"))
                    print(f"✅ {file_path:<25} -> {status_code} (Content blocked)")
                else:
                    results.append((file_path, status_code, "❌ ACCESSIBLE"))
                    print(f"❌ {file_path:<25} -> {status_code} (ACCESSIBLE - SECURITY RISK!)")
            else:
                results.append((file_path, status_code, "⚠️ UNKNOWN"))
                print(f"⚠️ {file_path:<25} -> {status_code} (Unknown response)")
                
        except requests.RequestException as e:
            results.append((file_path, "ERROR", f"⚠️ {str(e)[:50]}..."))
            print(f"⚠️ {file_path:<25} -> Error: {e}")
    
    print("\n" + "=" * 60)
    
    # Summary
    protected = sum(1 for _, _, status in results if status.startswith("✅"))
    accessible = sum(1 for _, _, status in results if status.startswith("❌"))
    
    print(f"📊 SECURITY SUMMARY:")
    print(f"   Protected files: {protected}")
    print(f"   Accessible files: {accessible}")
    print(f"   Total tested: {len(results)}")
    
    if accessible == 0:
        print(f"\n🎉 All sensitive files are properly protected!")
        return 0
    else:
        print(f"\n⚠️ WARNING: {accessible} files are accessible and need protection!")
        return 1

def main():
    """Main function to test file access"""
    
    # Files that should NOT be accessible via web
    sensitive_files = [
        "README.md",
        ".gitattributes",
        ".gitignore",
        ".htaccess",
        ".trivyignore",
        
        # ALL YAML configuration files (development configurations)
        "_config.yml",
        ".codacy.yml", 
        ".github/dependabot.yml",
        ".github/labeler.yml",
        ".github/workflows/codacy.yml",
        ".github/workflows/label.yml",
        ".github/workflows/static.yml",
        ".github/workflows/validate-website.yml",

        ".github/config/requirements.txt",
        ".github/config/genWordCloud.py",
        ".github/config/genPubHTML.sh",
        "assets/docs/publications/generate.sh",
        
        # Configuration files in assets directories
        "assets/js/package.json",
        "assets/js/Gruntfile.js",
        "assets/plugins/github-activity/package.json",
        
        # Developer documentation files
        "assets/HELP-US-OUT.txt",
        "assets/img/Developer-ReadMe.txt",
        "assets/img/faviconit-instructions.txt",
        
        ".env",
        "package.json",
        "composer.json",
    ]
    
    # Test with your domain
    base_url = "https://prajitdas.github.io/"
    
    print("🔍 Web Security File Access Test")
    print(f"Testing URL: {base_url}")
    print(f"Files to test: {len(sensitive_files)} (including all YAML configs)")
    print()
    
    return test_file_access(base_url, sensitive_files)

if __name__ == "__main__":
    sys.exit(main())