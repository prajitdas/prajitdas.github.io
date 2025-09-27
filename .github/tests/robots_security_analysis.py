#!/usr/bin/env python3
"""
robots.txt Security Analysis
Tests if robots.txt is inadvertently exposing sensitive file locations
"""

import requests
import re

def analyze_robots_txt():
    """Analyze robots.txt for security implications"""
    
    base_url = "https://prajitdas.github.io/"
    robots_url = f"{base_url}robots.txt"
    
    print("🤖 ROBOTS.TXT SECURITY ANALYSIS")
    print("=" * 50)
    
    try:
        # Get robots.txt content
        response = requests.get(robots_url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Could not fetch robots.txt (Status: {response.status_code})")
            return
            
        robots_content = response.text
        print(f"📄 robots.txt content ({len(robots_content)} chars):")
        print("-" * 30)
        print(robots_content)
        print("-" * 30)
        
        # Extract all Disallow entries
        disallow_pattern = r'Disallow:\s*(.+)'
        disallowed_paths = re.findall(disallow_pattern, robots_content)
        
        print(f"\n🚫 DISALLOWED PATHS REVEALED ({len(disallowed_paths)}):")
        
        exposed_files = []
        protected_files = []
        nonexistent_files = []
        
        for path in disallowed_paths:
            path = path.strip()
            if not path or path == '/':
                continue
                
            # Test if file actually exists
            test_url = f"{base_url}{path.lstrip('/')}"
            try:
                test_response = requests.get(test_url, timeout=5)
                status = test_response.status_code
                
                if status == 200:
                    print(f"❌ EXPOSED: {path:<30} → Still accessible!")
                    exposed_files.append(path)
                elif status == 404:
                    print(f"✅ SAFE: {path:<30} → Not found (404)")
                    nonexistent_files.append(path)
                elif status == 403:
                    print(f"🔒 PROTECTED: {path:<30} → Access forbidden")
                    protected_files.append(path)
                else:
                    print(f"❓ UNKNOWN: {path:<30} → Status {status}")
                    
            except requests.RequestException as e:
                print(f"⚠️ ERROR: {path:<30} → {str(e)[:50]}")
        
        # Security assessment
        print(f"\n📊 SECURITY ASSESSMENT:")
        print(f"   Exposed files: {len(exposed_files)} (BAD - accessible despite robots.txt)")
        print(f"   Protected files: {len(protected_files)} (GOOD - properly blocked)")  
        print(f"   Non-existent files: {len(nonexistent_files)} (CONCERN - revealing non-existent paths)")
        
        # Information disclosure risk
        total_disclosed = len(disallowed_paths)
        if total_disclosed > 0:
            print(f"\n🚨 INFORMATION DISCLOSURE RISK:")
            print(f"   robots.txt reveals {total_disclosed} sensitive file/directory paths")
            print(f"   Attackers can use this as a reconnaissance map!")
            
        # Check for redundant entries (files that don't exist)
        if nonexistent_files:
            print(f"\n🧹 CLEANUP NEEDED ({len(nonexistent_files)} entries):")
            for path in nonexistent_files[:10]:  # Show first 10
                print(f"   - {path} (file doesn't exist - remove from robots.txt)")
            if len(nonexistent_files) > 10:
                print(f"   ... and {len(nonexistent_files) - 10} more")
        
        # Overall recommendation
        print(f"\n🎯 RECOMMENDATION:")
        if exposed_files:
            print("   ❌ CRITICAL: robots.txt is not effective - files still accessible")
        if nonexistent_files:
            print("   ⚠️ WARNING: robots.txt reveals non-existent files unnecessarily")
        if total_disclosed > 5:
            print("   📝 SUGGESTION: Minimize robots.txt entries to reduce information disclosure")
            
        return {
            'exposed': len(exposed_files),
            'protected': len(protected_files),
            'nonexistent': len(nonexistent_files),
            'total_disclosed': total_disclosed
        }
        
    except requests.RequestException as e:
        print(f"❌ Error fetching robots.txt: {e}")
        return None

if __name__ == "__main__":
    results = analyze_robots_txt()
    if results:
        # Exit code based on security findings
        if results['exposed'] > 0:
            exit(2)  # Critical - files exposed despite robots.txt
        elif results['nonexistent'] > 3:
            exit(1)  # Warning - too much information disclosure
        else:
            exit(0)  # OK
    else:
        exit(1)  # Error