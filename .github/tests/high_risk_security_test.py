#!/usr/bin/env python3
"""
High-Risk File Protection Analysis
Identifies and tests protection for files that definitely shouldn't be web-accessible
"""

import requests
import sys
from urllib.parse import urljoin

def test_high_risk_files():
    """Test specifically high-risk files that should be protected"""
    
    base_url = "https://prajitdas.github.io/"
    
    # Files that DEFINITELY should not be accessible
    high_risk_files = [
        # Jekyll configuration
        "_config.yml",
        
        # Build and development files
        "assets/MANIFEST",
        "assets/docs/publications/generate.sh",
        
        # Renamed development files (dev-* prefix)
        "assets/js/dev-package.json",
        "assets/js/dev-Gruntfile.js",
        "assets/plugins/github-activity/dev-package.json",
        
        # Build configuration files
        "assets/plugins/github-activity/Gruntfile.js",
        "assets/plugins/github-activity/bower.json",
        
        # Development documentation that reveals internal structure
        "assets/HELP-US-OUT.txt",
        "assets/img/Developer-ReadMe.txt", 
        "assets/img/faviconit-instructions.txt",
        
        # Internal README files that might reveal sensitive info
        "assets/docs/publications/README.md",
        "assets/js/README.md",
        "assets/plugins/github-activity/README.md",
    ]
    
    print("🔴 HIGH-RISK FILE PROTECTION TEST")
    print("=" * 50)
    print(f"Testing {len(high_risk_files)} high-risk files...")
    print("=" * 50)
    
    accessible_high_risk = []
    protected_files = []
    
    for file_path in high_risk_files:
        url = urljoin(base_url, file_path)
        
        try:
            response = requests.get(url, timeout=10)
            status = response.status_code
            
            if status == 200:
                print(f"🚨 {file_path:<50} -> {status} (CRITICAL: NEEDS PROTECTION!)")
                accessible_high_risk.append(file_path)
            elif status in [403, 404]:
                print(f"✅ {file_path:<50} -> {status} (Protected)")
                protected_files.append(file_path)
            else:
                print(f"⚠️  {file_path:<50} -> {status} (Unexpected)")
            
        except requests.RequestException as e:
            print(f"❓ {file_path:<50} -> ERROR")
    
    print("\n" + "=" * 50)
    print("📊 HIGH-RISK SECURITY SUMMARY:")
    print(f"   🔴 Accessible high-risk files: {len(accessible_high_risk)}")
    print(f"   ✅ Protected high-risk files: {len(protected_files)}")
    
    if accessible_high_risk:
        print(f"\n🚨 CRITICAL: {len(accessible_high_risk)} high-risk files need immediate protection:")
        for file in accessible_high_risk:
            print(f"   - {file}")
        
        print("\n💡 RECOMMENDED ACTIONS:")
        print("   1. Move dev-* files to .github/dev/ directory")
        print("   2. Add .htaccess files to assets subdirectories")
        print("   3. Update Jekyll _config.yml exclusions")
        print("   4. Consider renaming exposed build files")
        
        return False
    else:
        print("\n🎉 SUCCESS: All high-risk files are properly protected!")
        return True

if __name__ == "__main__":
    success = test_high_risk_files()
    sys.exit(0 if success else 1)