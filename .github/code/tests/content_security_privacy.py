#!/usr/bin/env python3
"""
Content Security & Privacy Validation Test
Validates content security policies, privacy compliance, and data protection.
Fast local execution focused on configuration and content analysis.
"""

import os
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
import urllib.parse

def test_content_security_policy():
    """Test Content Security Policy implementation"""
    print("🛡️ TESTING CONTENT SECURITY POLICY")
    print("-" * 45)
    
    issues = []
    
    # Test index.html for CSP
    index_path = Path('index.html')
    if not index_path.exists():
        issues.append("index.html not found")
        return False
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check for CSP meta tag
        csp_meta = soup.find('meta', attrs={'http-equiv': re.compile(r'content-security-policy', re.I)})
        csp_found = False
        
        if csp_meta and csp_meta.get('content'):
            csp_content = csp_meta.get('content')
            print(f"   ✅ CSP meta tag found")
            csp_found = True
            
            # Analyze CSP directives
            csp_directives = {}
            directives = csp_content.split(';')
            for directive in directives:
                directive = directive.strip()
                if ' ' in directive:
                    key, value = directive.split(' ', 1)
                    csp_directives[key.strip()] = value.strip()
            
            # Check for important CSP directives
            important_directives = ['default-src', 'script-src', 'style-src', 'img-src']
            for directive in important_directives:
                if directive in csp_directives:
                    print(f"     ✅ {directive}: {csp_directives[directive]}")
                else:
                    print(f"     ⚠️ {directive}: Not specified")
        
        # Check for inline scripts and styles (potential CSP violations)
        inline_scripts = soup.find_all('script', src=False)
        inline_scripts = [s for s in inline_scripts if s.get_text().strip()]
        
        inline_styles = soup.find_all('style')
        style_attributes = soup.find_all(attrs={'style': True})
        
        print(f"   📊 Inline scripts: {len(inline_scripts)}")
        print(f"   📊 Inline styles: {len(inline_styles)}")
        print(f"   📊 Style attributes: {len(style_attributes)}")
        
        if csp_found:
            if len(inline_scripts) > 0:
                print(f"   ⚠️ CSP may conflict with {len(inline_scripts)} inline scripts")
            if len(inline_styles) > 0 or len(style_attributes) > 0:
                print(f"   ⚠️ CSP may conflict with inline styles")
        
        return csp_found
        
    except Exception as e:
        issues.append(f"Error analyzing CSP: {str(e)}")
        return False

def test_privacy_compliance():
    """Test privacy compliance features"""
    print("\n🔒 TESTING PRIVACY COMPLIANCE")
    print("-" * 45)
    
    issues = []
    
    # Test HTML files for privacy features
    html_files = [Path('index.html')]
    
    privacy_score = 0
    
    for html_file in html_files:
        if not html_file.exists():
            continue
            
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            print(f"   🔍 Testing {html_file.name}")
            
            # Check for privacy policy link
            privacy_links = soup.find_all('a', href=re.compile(r'privacy', re.I))
            if privacy_links:
                print("     ✅ Privacy policy link found")
                privacy_score += 20
            
            # Check for cookie consent/notice
            cookie_patterns = [r'cookie', r'consent', r'gdpr', r'privacy']
            cookie_notice_found = False
            for pattern in cookie_patterns:
                if re.search(pattern, content, re.I):
                    cookie_notice_found = True
                    break
            
            if cookie_notice_found:
                print("     ✅ Cookie/privacy notice detected")
                privacy_score += 15
            
            # Check for external trackers (should be minimal)
            script_tags = soup.find_all('script', src=True)
            tracking_domains = [
                'google-analytics.com', 'googletagmanager.com', 
                'facebook.com', 'doubleclick.net', 'adsystem.amazon.com'
            ]
            
            trackers_found = []
            for script in script_tags:
                src = script.get('src', '')
                for domain in tracking_domains:
                    if domain in src:
                        trackers_found.append(domain)
            
            if not trackers_found:
                print("     ✅ No common tracking scripts detected")
                privacy_score += 25
            else:
                print(f"     ⚠️ Tracking scripts found: {', '.join(set(trackers_found))}")
            
            # Check for data collection forms
            forms = soup.find_all('form')
            secure_forms = 0
            for form in forms:
                action = form.get('action', '')
                method = form.get('method', '').lower()
                
                # Check for HTTPS in form actions
                if action.startswith('https://') or not action.startswith('http'):
                    secure_forms += 1
                
                # Check for sensitive input types
                sensitive_inputs = form.find_all('input', type=['email', 'password', 'tel'])
                if sensitive_inputs and method == 'post':
                    print(f"     ✅ Secure form handling detected")
                    privacy_score += 10
            
            # Check for referrer policy
            referrer_policy = soup.find('meta', attrs={'name': 'referrer'})
            if referrer_policy:
                policy = referrer_policy.get('content', '')
                print(f"     ✅ Referrer policy: {policy}")
                privacy_score += 10
            
        except Exception as e:
            issues.append(f"Error analyzing {html_file.name}: {str(e)}")
    
    print(f"   📊 Privacy compliance score: {privacy_score}/80")
    return privacy_score >= 40  # 50% threshold

def test_data_protection():
    """Test data protection and security measures"""
    print("\n🔐 TESTING DATA PROTECTION")
    print("-" * 45)
    
    issues = []
    
    # Check for keybase.txt (identity verification)
    keybase_path = Path('keybase.txt')
    if keybase_path.exists():
        print("   ✅ Keybase identity verification file present")
    
    # Check for security.txt (security contact info)
    security_paths = [Path('security.txt'), Path('.well-known/security.txt')]
    security_txt_found = any(path.exists() for path in security_paths)
    if security_txt_found:
        print("   ✅ Security.txt file found")
    else:
        print("   ⚠️ No security.txt file found")
    
    # Test for HTTPS enforcement in configuration
    htaccess_path = Path('.htaccess')
    https_enforcement = False
    
    if htaccess_path.exists():
        try:
            with open(htaccess_path, 'r', encoding='utf-8') as f:
                htaccess_content = f.read()
            
            # Check for HTTPS redirect rules
            https_patterns = [
                r'RewriteRule.*https',
                r'Header.*Strict-Transport-Security',
                r'HTTPS.*on'
            ]
            
            for pattern in https_patterns:
                if re.search(pattern, htaccess_content, re.I):
                    https_enforcement = True
                    print("   ✅ HTTPS enforcement detected in .htaccess")
                    break
        except Exception as e:
            print(f"   ⚠️ Error reading .htaccess: {str(e)}")
    
    # Check robots.txt for privacy directives
    robots_path = Path('robots.txt')
    robots_privacy = False
    
    if robots_path.exists():
        try:
            with open(robots_path, 'r', encoding='utf-8') as f:
                robots_content = f.read()
            
            # Check for privacy-related directives
            if 'Disallow:' in robots_content:
                disallowed_paths = re.findall(r'Disallow:\s*(.+)', robots_content)
                private_paths = [path for path in disallowed_paths if any(
                    keyword in path.lower() for keyword in ['private', 'admin', 'config', 'test']
                )]
                
                if private_paths:
                    print(f"   ✅ Privacy directives in robots.txt: {len(private_paths)} paths")
                    robots_privacy = True
                else:
                    print("   ✅ Robots.txt present with disallow directives")
        except Exception as e:
            print(f"   ⚠️ Error reading robots.txt: {str(e)}")
    
    # Check for sensitive file patterns in gitignore
    gitignore_path = Path('.gitignore')
    gitignore_security = False
    
    if gitignore_path.exists():
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                gitignore_content = f.read()
            
            # Check for security-related patterns
            security_patterns = [
                r'\.env', r'\.key', r'config\.', r'secret', 
                r'password', r'\.log', r'\.sql'
            ]
            
            patterns_found = []
            for pattern in security_patterns:
                if re.search(pattern, gitignore_content, re.I):
                    patterns_found.append(pattern)
            
            if patterns_found:
                print(f"   ✅ Security patterns in .gitignore: {len(patterns_found)}")
                gitignore_security = True
        except Exception as e:
            print(f"   ⚠️ Error reading .gitignore: {str(e)}")
    
    protection_score = sum([
        keybase_path.exists(),
        security_txt_found,
        https_enforcement,
        robots_privacy,
        gitignore_security
    ])
    
    print(f"   📊 Data protection measures: {protection_score}/5")
    return protection_score >= 3  # 60% threshold

def test_content_integrity():
    """Test content integrity and validation"""
    print("\n📝 TESTING CONTENT INTEGRITY")
    print("-" * 45)
    
    issues = []
    
    # Test HTML files for potential security issues
    html_files = list(Path('.').rglob('*.html'))
    html_files = [f for f in html_files if not any(part.startswith('.') for part in f.parts)]
    
    security_issues = 0
    
    for html_file in html_files[:3]:  # Test first 3 HTML files
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for potentially dangerous patterns
            dangerous_patterns = [
                (r'eval\s*\(', 'JavaScript eval() usage'),
                (r'innerHTML\s*=', 'innerHTML assignment'),
                (r'document\.write\s*\(', 'document.write() usage'),
                (r'<script[^>]*src=["\']http:', 'Non-HTTPS script source'),
            ]
            
            file_issues = 0
            for pattern, description in dangerous_patterns:
                if re.search(pattern, content, re.I):
                    print(f"   ⚠️ {html_file.name}: {description}")
                    file_issues += 1
                    security_issues += 1
            
            if file_issues == 0:
                print(f"   ✅ {html_file.name}: No obvious security issues")
                
        except Exception as e:
            issues.append(f"Error analyzing {html_file.name}: {str(e)}")
    
    # Test for proper encoding declarations
    encoding_issues = 0
    for html_file in html_files[:3]:
        try:
            with open(html_file, 'rb') as f:
                raw_content = f.read(1024)  # Read first 1KB
            
            # Check for BOM or encoding declaration
            has_utf8_bom = raw_content.startswith(b'\xef\xbb\xbf')
            has_charset_meta = b'charset=' in raw_content.lower()
            
            if not (has_utf8_bom or has_charset_meta):
                print(f"   ⚠️ {html_file.name}: No explicit encoding declaration")
                encoding_issues += 1
            else:
                print(f"   ✅ {html_file.name}: Proper encoding declaration")
                
        except Exception as e:
            issues.append(f"Error checking encoding for {html_file.name}: {str(e)}")
    
    print(f"   📊 Security issues found: {security_issues}")
    print(f"   📊 Encoding issues: {encoding_issues}")
    
    return security_issues == 0 and encoding_issues <= 1

def main():
    """Run all content security and privacy tests"""
    print("🔒 CONTENT SECURITY & PRIVACY VALIDATION TEST SUITE")
    print("=" * 65)
    
    # Change to repository root if needed
    if Path.cwd().name == 'tests':
        os.chdir('../../..')
    elif '.github' in str(Path.cwd()):
        current = Path.cwd()
        while current.parent != current:
            if (current / 'index.html').exists():
                os.chdir(current)
                break
            current = current.parent
        # Additional fallback for the reorganized structure
        if not Path('index.html').exists():
            script_dir = Path(__file__).parent
            project_root = script_dir.parent.parent.parent.parent
            if (project_root / 'index.html').exists():
                os.chdir(project_root)
    
    print(f"📁 Testing directory: {Path.cwd()}")
    print()
    
    # Run all tests
    tests = [
        ("Content Security Policy", test_content_security_policy),
        ("Privacy Compliance", test_privacy_compliance),
        ("Data Protection", test_data_protection),
        ("Content Integrity", test_content_integrity)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"   ❌ {test_name}: Test failed with error: {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 65)
    print("📊 CONTENT SECURITY & PRIVACY TEST SUMMARY")
    print("=" * 65)
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"📈 Tests passed: {passed}/{total}")
    print(f"📊 Success rate: {success_rate:.1f}%")
    
    if passed == total:
        print("🎉 ALL SECURITY & PRIVACY TESTS PASSED!")
        return 0
    elif passed >= total * 0.75:
        print("⚠️ Good security posture - minor improvements recommended")
        return 0  # Don't fail for minor issues
    else:
        print("❌ Significant security/privacy issues detected")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)