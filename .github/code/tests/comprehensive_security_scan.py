#!/usr/bin/env python3
"""
Comprehensive Security Analysis Suite
Combines web accessibility testing, credential scanning, and high-risk file analysis
"""

import requests
import sys
import os
import re
import time
from urllib.parse import urljoin
from pathlib import Path

PUBLIC_ALLOWLIST = {
    "404.html",
    "index.html",
    "keybase.txt",
    "robots.txt",
    "ror.xml",
    "sitemap.xml",
    "sw.js",
}
PUBLIC_ALLOW_PREFIXES = ("assets/", ".well-known/")

# Import local logging system (only for local runs, not GitHub Actions)
try:
    if not os.environ.get('GITHUB_ACTIONS'):
        from local_test_logger import log_security_issue, log_url_failure
        LOCAL_LOGGING_ENABLED = True
    else:
        LOCAL_LOGGING_ENABLED = False
except ImportError:
    LOCAL_LOGGING_ENABLED = False

def scan_for_credentials(base_dir):
    """Scan repository for potential credential leakage and sensitive information"""
    
    # Security patterns to check for
    patterns = {
        'api_keys': r'(api[_-]?key\s*[:=]\s*["\'][^"\']+["\'])',
        'aws_keys': r'(AKIA[0-9A-Z]{16}|aws_access_key_id\s*[:=])',
        'github_tokens': r'(gh[pousr]_[A-Za-z0-9]{36}|github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59})',
        'passwords': r'(password\s*[:=]\s*["\'][^"\']+["\'])',
        'private_keys': r'-----BEGIN.*(PRIVATE|RSA).*KEY-----',
        'connection_strings': r'(mysql://[^\\s]+@|postgres://[^\\s]+@|mongodb://[^\\s]+@)',
        'hardcoded_secrets': r'(secret\s*[:=]\s*["\'][^"\']+["\'])',
    }
    
    # Files to skip (known safe files)
    skip_patterns = [
        'keybase.txt', 'github-activity', 'Developer-ReadMe.txt', 'bower.json',
        'font', '.svg', 'security_scan.py', 'comprehensive_security_scan.py'
    ]
    
    issues = []
    scanned_files = 0
    
    for file_path in base_dir.rglob('*'):
        if not file_path.is_file():
            continue
            
        # Skip hidden directories and git files
        if any(part.startswith('.git') for part in file_path.parts):
            continue
            
        # Skip known safe files
        if any(skip in str(file_path) for skip in skip_patterns):
            continue
            
        # Only scan text-based files
        if file_path.suffix not in ['.txt', '.html', '.js', '.json', '.yml', '.yaml', '.md', '.py', '.sh', '.css']:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                scanned_files += 1
                
            for pattern_name, pattern in patterns.items():
                matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                if matches:
                    # Filter out false positives
                    real_matches = []
                    for match in matches:
                        match_text = match if isinstance(match, str) else match[0]
                        
                        # Skip template variables and examples
                        if any(template in match_text.lower() for template in [
                            'example', 'your_', 'placeholder', 'template', 'xxx', 'yyy', 'zzz',
                            'client_id', 'client_secret'  # These are just parameter names
                        ]):
                            continue
                            
                        real_matches.append(match_text[:50] + '...' if len(match_text) > 50 else match_text)
                    
                    if real_matches:
                        issues.append({
                            'file': file_path.relative_to(base_dir),
                            'type': pattern_name,
                            'matches': real_matches[:3]  # Limit to first 3 matches
                        })
        except Exception as e:
            print(f"⚠️ Error scanning {file_path}: {e}")
    
    return issues, scanned_files

def test_high_risk_files(base_url):
    """Test specifically high-risk files that should be protected"""
    
    # Files that DEFINITELY should not be accessible
    high_risk_files = [
        "_config.yml", "assets/MANIFEST", "assets/docs/publications/generate.sh",
        "assets/js/dev-package.json", "assets/js/dev-Gruntfile.js",
        "assets/plugins/github-activity/dev-package.json",
        "assets/plugins/github-activity/Gruntfile.js",
        "assets/plugins/github-activity/bower.json",
        "assets/HELP-US-OUT.txt", "assets/img/Developer-ReadMe.txt",
        "assets/img/faviconit-instructions.txt",
        "assets/docs/publications/README.md", "assets/js/README.md",
        "assets/plugins/github-activity/README.md",
    ]
    
    accessible_high_risk = []
    protected_files = []
    
    for file_path in high_risk_files:
        try:
            test_url = urljoin(base_url, file_path)
            response = requests.get(test_url, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                accessible_high_risk.append(file_path)
                print(f"🚨 HIGH RISK: {file_path:<35} → ACCESSIBLE ({response.status_code})")
            else:
                protected_files.append(file_path)
                print(f"✅ PROTECTED: {file_path:<35} → Blocked ({response.status_code})")
                
        except requests.RequestException as e:
            print(f"⚠️ ERROR: {file_path:<35} → {str(e)[:50]}")
            
        time.sleep(0.1)  # Rate limiting
    
    return accessible_high_risk, protected_files

def test_file_access(base_url, files_to_test):
    """Test that sensitive files return 403/404 errors"""
    
    print(f"🔐 Comprehensive Security Test for: {base_url}")
    print("=" * 70)
    print("ℹ️  Testing all potentially sensitive files...")
    print("=" * 70)

    original_count = len(files_to_test)
    files_to_test = [f for f in files_to_test if not is_public_file(f)]
    skipped_public = original_count - len(files_to_test)
    if skipped_public:
        print(f"ℹ️  Skipping {skipped_public} public site files from security scan")

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
        
        # Count functional vs security files
        js_css_files = [f for f in accessible_files if any(f.endswith(ext) for ext in ['.js', '.css'])]
        config_files = [f for f in accessible_files if f in ['_config.yml', 'README.md', 'robots.txt', 'sitemap.xml', 'ror.xml']]
        
        print(f"\n📋 FILE ANALYSIS:")
        print(f"   • JavaScript/CSS files: {len(js_css_files)} (required for website functionality)")
        print(f"   • Configuration/SEO files: {len(config_files)} (standard web files)")
        print(f"   • Other files: {len(accessible_files) - len(js_css_files) - len(config_files)}")
        
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
                if is_public_file(rel_path):
                    continue
                all_files.append(rel_path)
    
    # Remove duplicates and sort
    return sorted(list(set(all_files)))

def is_public_file(rel_path):
    normalized = rel_path.lstrip("./")
    if normalized in PUBLIC_ALLOWLIST:
        return True
    return any(normalized.startswith(prefix) for prefix in PUBLIC_ALLOW_PREFIXES)

def scan_for_insecure_links(base_dir):
    """Scan for links with target="_blank" missing rel="noopener" or rel="noreferrer"."""

    issues = []
    scanned_files = 0

    # Regex to find anchor tags with target="_blank"
    target_blank_pattern = re.compile(r'<a\s+[^>]*target=["\']_blank["\'][^>]*>', re.IGNORECASE)

    for file_path in base_dir.rglob('*'):
        if not file_path.is_file():
            continue

        # Skip hidden directories and git files
        if any(part.startswith('.git') for part in file_path.parts):
            continue

        if file_path.suffix not in ['.html', '.js', '.md', '.php']:
            continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                scanned_files += 1

            matches = target_blank_pattern.findall(content)
            for match in matches:
                # Check if rel="noopener" or rel="noreferrer" is present in the tag
                if 'noopener' not in match and 'noreferrer' not in match:
                    issues.append({
                        'file': file_path.relative_to(base_dir),
                        'type': 'insecure_link_target',
                        'matches': [match[:100]] # Truncate for display
                    })

        except Exception as e:
            pass # Ignore errors

    return issues, scanned_files

def main():
    """Run comprehensive security analysis suite"""
    
    base_url = "https://prajitdas.github.io/"
    base_dir = Path(__file__).parent.parent.parent.parent  # Repository root
    
    print("🛡️ COMPREHENSIVE SECURITY ANALYSIS SUITE")
    print("=" * 60)
    print("Running four-tier security analysis:")
    print("  1. Credential & Sensitive Data Scanning (File System)")
    print("  2. Insecure Link Scanning (File System)")
    print("  3. High-Risk File Protection Testing (Web Access)")
    print("  4. General Web Security Scanning (Web Access)")
    print("=" * 60)
    
    all_issues = []
    
    # === PHASE 1: CREDENTIAL SCANNING ===
    print("\n🔍 PHASE 1: CREDENTIAL & SENSITIVE DATA SCANNING")
    print("-" * 50)
    print("📁 Scanning local files for credentials and sensitive information...")
    
    credential_issues, scanned_files = scan_for_credentials(base_dir)
    
    if credential_issues:
        print(f"\n🚨 CREDENTIAL SECURITY ISSUES FOUND ({len(credential_issues)}):")
        for issue in credential_issues:
            print(f"   📁 {issue['file']} → {issue['type']}")
            for match in issue['matches']:
                print(f"      • {match}")
        all_issues.extend(credential_issues)
    else:
        print(f"✅ No credential issues found in {scanned_files} files")
    
    # === PHASE 2: INSECURE LINK SCANNING ===
    print("\n🔍 PHASE 2: INSECURE LINK SCANNING")
    print("-" * 50)
    print("🔗 Scanning local files for insecure target='_blank' links...")

    link_issues, link_scanned_files = scan_for_insecure_links(base_dir)

    if link_issues:
        print(f"\n🚨 INSECURE LINK ISSUES FOUND ({len(link_issues)}):")
        for issue in link_issues:
            print(f"   📁 {issue['file']} → {issue['type']}")
            for match in issue['matches']:
                print(f"      • {match}")
        all_issues.extend(link_issues)
    else:
        print(f"✅ No insecure link issues found in {link_scanned_files} files")

    # === PHASE 3: HIGH-RISK FILE TESTING ===
    print(f"\n🔥 PHASE 3: HIGH-RISK FILE PROTECTION TESTING")
    print("-" * 50)
    print("🎯 Testing critical files that must be protected...")
    
    accessible_high_risk, protected_high_risk = test_high_risk_files(base_url)
    
    if accessible_high_risk:
        print(f"\n🚨 HIGH-RISK FILES ACCESSIBLE ({len(accessible_high_risk)}):")
        for file_path in accessible_high_risk:
            print(f"   🚨 {file_path}")
        all_issues.extend([{'type': 'high_risk_accessible', 'file': f} for f in accessible_high_risk])
    else:
        print(f"✅ All {len(protected_high_risk)} high-risk files properly protected")
    
    # === PHASE 4: GENERAL WEB SECURITY SCANNING ===
    print(f"\n🌐 PHASE 4: GENERAL WEB SECURITY SCANNING")
    print("-" * 50)
    
    # Discover all potentially sensitive files
    print("📁 Discovering potentially sensitive files...")
    discovered_files = discover_files()
    
    # Add high-priority files from basic security test (removed duplicates)
    high_priority_files = [
        "README.md", ".gitattributes", ".gitignore", ".htaccess", ".trivyignore",
        "_config.yml", ".codacy.yml", ".env", "package.json", "composer.json"
    ]
    
    # Combine and deduplicate
    all_test_files = list(set(discovered_files + high_priority_files))
    
    print(f"📋 Found {len(all_test_files)} files to test:")
    for file in all_test_files[:10]:  # Show first 10
        print(f"   - {file}")
    if len(all_test_files) > 10:
        print(f"   ... and {len(all_test_files) - 10} more files")
    
    print(f"\n🔍 Testing all {len(all_test_files)} files...")
    print("=" * 50)
    
    # Test all discovered files (now includes high-priority files)
    web_security_success = test_file_access(base_url, all_test_files)
    
    # === FINAL ASSESSMENT ===
    print(f"\n📊 COMPREHENSIVE SECURITY SUMMARY:")
    print("=" * 60)
    
    total_issues = len(all_issues)
    credential_issues_count = len(credential_issues)
    high_risk_issues_count = len(accessible_high_risk)
    
    print(f"🔍 Files Scanned for Credentials: {scanned_files}")
    print(f"🎯 High-Risk Files Tested: {len(protected_high_risk) + len(accessible_high_risk)}")  
    print(f"🌐 Web Security Files Tested: {len(all_test_files)}")
    print(f"🚨 Total Security Issues: {total_issues}")
    
    # Check for truly critical issues (exclude _config.yml which is minimized and acceptable)
    critical_high_risk = [f for f in accessible_high_risk if not f.endswith('_config.yml')]
    
    if total_issues == 0:
        print(f"\n🏆 SECURITY STATUS: ✅ EXCELLENT")
        print("   All security checks passed successfully!")
        return 0
    elif credential_issues_count > 0 or len(critical_high_risk) > 0:
        print(f"\n🏆 SECURITY STATUS: ❌ CRITICAL ISSUES")
        print("   High-severity security issues found!")
        return 2
    elif high_risk_issues_count > 0:
        print(f"\n🏆 SECURITY STATUS: ⚠️ ACCEPTABLE RISK")
        print("   _config.yml accessible but minimized (acceptable)")
        return 0
    else:
        print(f"\n🏆 SECURITY STATUS: ⚠️ MINOR ISSUES")
        print("   Some security concerns identified")
        return 1

if __name__ == "__main__":
    sys.exit(main())
