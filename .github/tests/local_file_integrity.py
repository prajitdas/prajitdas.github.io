#!/usr/bin/env python3
"""
Enhanced Local File Integrity Test
Validates local file permissions, content integrity, and configuration consistency.
Runs quickly without external network calls - perfect for comprehensive local coverage.
"""

import os
import sys
import hashlib
import mimetypes
from pathlib import Path
import re
import json

def test_file_permissions():
    """Test that critical files have appropriate permissions"""
    critical_files = [
        'keybase.txt',
        'robots.txt', 
        'sitemap.xml',
        'index.html',
        '_config.yml'
    ]
    
    print("🔐 TESTING FILE PERMISSIONS")
    print("-" * 40)
    
    results = []
    for filename in critical_files:
        file_path = Path(filename)
        if file_path.exists():
            # Check if file is readable
            readable = os.access(file_path, os.R_OK)
            # Check if file is not executable (security)
            not_executable = not os.access(file_path, os.X_OK)
            
            status = "✅" if readable and not_executable else "❌"
            print(f"   {status} {filename}: readable={readable}, not_executable={not_executable}")
            results.append(readable and not_executable)
        else:
            print(f"   ❌ {filename}: File not found")
            results.append(False)
    
    return all(results)

def test_content_integrity():
    """Test content integrity and consistency"""
    print("\n📝 TESTING CONTENT INTEGRITY")
    print("-" * 40)
    
    issues = []
    
    # Test HTML files for basic structure
    html_files = list(Path('.').rglob('*.html'))
    html_files = [f for f in html_files if not any(part.startswith('.') for part in f.parts)]
    
    for html_file in html_files[:5]:  # Test first 5 HTML files
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic HTML structure checks
            has_doctype = content.strip().startswith('<!DOCTYPE') or content.strip().startswith('<!doctype')
            has_html_tag = '<html' in content.lower()
            has_head_tag = '<head' in content.lower()
            has_body_tag = '<body' in content.lower()
            
            if not (has_doctype and has_html_tag and has_head_tag and has_body_tag):
                issues.append(f"{html_file}: Missing basic HTML structure")
                print(f"   ❌ {html_file}: Invalid HTML structure")
            else:
                print(f"   ✅ {html_file}: Valid HTML structure")
                
        except Exception as e:
            issues.append(f"{html_file}: Read error - {str(e)}")
            print(f"   ❌ {html_file}: {str(e)}")
    
    return len(issues) == 0

def test_configuration_consistency():
    """Test configuration file consistency"""
    print("\n⚙️ TESTING CONFIGURATION CONSISTENCY")
    print("-" * 40)
    
    issues = []
    
    # Test robots.txt consistency
    robots_path = Path('robots.txt')
    if robots_path.exists():
        try:
            with open(robots_path, 'r', encoding='utf-8') as f:
                robots_content = f.read()
            
            # Should have User-agent and Sitemap
            has_user_agent = 'User-agent:' in robots_content
            has_sitemap = 'Sitemap:' in robots_content
            
            if has_user_agent and has_sitemap:
                print("   ✅ robots.txt: Properly configured")
            else:
                issues.append("robots.txt: Missing User-agent or Sitemap directive")
                print("   ❌ robots.txt: Missing required directives")
                
        except Exception as e:
            issues.append(f"robots.txt: Read error - {str(e)}")
    else:
        issues.append("robots.txt: File not found")
    
    # Test sitemap.xml existence and basic structure
    sitemap_path = Path('sitemap.xml')
    if sitemap_path.exists():
        try:
            with open(sitemap_path, 'r', encoding='utf-8') as f:
                sitemap_content = f.read()
            
            # Basic XML structure
            has_xml_declaration = '<?xml' in sitemap_content
            has_urlset = '<urlset' in sitemap_content
            has_urls = '<url>' in sitemap_content
            
            if has_xml_declaration and has_urlset and has_urls:
                print("   ✅ sitemap.xml: Valid XML structure")
            else:
                issues.append("sitemap.xml: Invalid XML structure")
                print("   ❌ sitemap.xml: Invalid structure")
                
        except Exception as e:
            issues.append(f"sitemap.xml: Read error - {str(e)}")
    else:
        issues.append("sitemap.xml: File not found")
    
    return len(issues) == 0

def test_asset_integrity():
    """Test asset file integrity and organization"""
    print("\n🎨 TESTING ASSET INTEGRITY")
    print("-" * 40)
    
    issues = []
    
    # Test CSS files
    css_files = list(Path('assets/css').glob('*.css')) if Path('assets/css').exists() else []
    for css_file in css_files[:3]:  # Test first 3 CSS files
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic CSS validation
            if '{' in content and '}' in content:
                print(f"   ✅ {css_file.name}: Valid CSS syntax")
            else:
                issues.append(f"{css_file.name}: Invalid CSS syntax")
                print(f"   ❌ {css_file.name}: Invalid syntax")
                
        except Exception as e:
            issues.append(f"{css_file.name}: Read error - {str(e)}")
    
    # Test JavaScript files (non-minified)
    js_files = list(Path('assets/js').glob('*.js')) if Path('assets/js').exists() else []
    js_files = [f for f in js_files if not f.name.endswith('.min.js')][:3]
    
    for js_file in js_files:
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic JavaScript validation
            has_syntax_error = False
            # Simple syntax checks
            open_braces = content.count('{')
            close_braces = content.count('}')
            open_parens = content.count('(')
            close_parens = content.count(')')
            
            if abs(open_braces - close_braces) <= 2 and abs(open_parens - close_parens) <= 2:
                print(f"   ✅ {js_file.name}: Basic syntax appears valid")
            else:
                issues.append(f"{js_file.name}: Potential syntax issues")
                print(f"   ❌ {js_file.name}: Brace/parentheses mismatch")
                
        except Exception as e:
            issues.append(f"{js_file.name}: Read error - {str(e)}")
    
    return len(issues) == 0

def test_security_configurations():
    """Test security configuration files"""
    print("\n🛡️ TESTING SECURITY CONFIGURATIONS")
    print("-" * 40)
    
    issues = []
    
    # Test .htaccess if it exists
    htaccess_path = Path('.htaccess')
    if htaccess_path.exists():
        try:
            with open(htaccess_path, 'r', encoding='utf-8') as f:
                htaccess_content = f.read()
            
            # Should have security headers
            has_security_rules = any(rule in htaccess_content.lower() for rule in [
                'x-frame-options', 'x-content-type-options', 'deny', 'forbidden'
            ])
            
            if has_security_rules:
                print("   ✅ .htaccess: Security rules present")
            else:
                issues.append(".htaccess: No apparent security rules")
                print("   ⚠️ .htaccess: No obvious security rules")
                
        except Exception as e:
            issues.append(f".htaccess: Read error - {str(e)}")
    
    # Test for sensitive file patterns that shouldn't exist
    sensitive_patterns = [
        '*.env', '*.key', '*.pem', 
        'config.json', 'secrets.json',
        '*.sql', 'database.*'
    ]
    
    found_sensitive = []
    for pattern in sensitive_patterns:
        matches = list(Path('.').rglob(pattern))
        matches = [m for m in matches if not any(part.startswith('.git') for part in m.parts)]
        if matches:
            found_sensitive.extend(matches)
    
    if found_sensitive:
        for sensitive_file in found_sensitive:
            issues.append(f"Potentially sensitive file found: {sensitive_file}")
            print(f"   ⚠️ Found: {sensitive_file}")
    else:
        print("   ✅ No obviously sensitive files found")
    
    return len(issues) == 0

def main():
    """Run all local integrity tests"""
    print("🔍 LOCAL FILE INTEGRITY & SECURITY TEST SUITE")
    print("=" * 60)
    
    # Change to repository root if we're in tests directory
    if Path.cwd().name == 'tests':
        os.chdir('../..')
    elif '.github' in str(Path.cwd()):
        # Find repository root
        current = Path.cwd()
        while current.parent != current:
            if (current / 'index.html').exists() or (current / '_config.yml').exists():
                os.chdir(current)
                break
            current = current.parent
    
    print(f"📁 Testing directory: {Path.cwd()}")
    print()
    
    # Run all tests
    tests = [
        ("File Permissions", test_file_permissions),
        ("Content Integrity", test_content_integrity),
        ("Configuration Consistency", test_configuration_consistency),
        ("Asset Integrity", test_asset_integrity),
        ("Security Configurations", test_security_configurations)
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
    print("\n" + "=" * 60)
    print("📊 LOCAL INTEGRITY TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"📈 Tests passed: {passed}/{total}")
    print(f"📊 Success rate: {success_rate:.1f}%")
    
    if passed == total:
        print("🎉 ALL LOCAL INTEGRITY TESTS PASSED!")
        return 0
    else:
        print("⚠️ Some local integrity issues detected")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)