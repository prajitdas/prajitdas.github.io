#!/usr/bin/env python3
"""
Website Functionality Test
Tests that the website remains fully functional after security modifications.
Verifies that all essential assets, pages, and features are accessible.
"""

import requests
import sys
from urllib.parse import urljoin
import time

def test_url_accessibility(base_url, path, description=""):
    """Test if a URL is accessible and returns expected status code"""
    try:
        url = urljoin(base_url, path)
        response = requests.get(url, timeout=10, allow_redirects=True)
        return response.status_code, response.headers.get('content-type', 'unknown')
    except requests.RequestException as e:
        return 0, f"Error: {str(e)}"

def website_functionality_test():
    """Run comprehensive website functionality test"""
    
    base_url = "https://prajitdas.github.io/"
    
    print("🌐 WEBSITE FUNCTIONALITY TEST")
    print("=" * 60)
    print(f"🎯 Target: {base_url}")
    print("🔍 Testing all essential website components...")
    print("=" * 60)
    
    # Define essential components for website functionality
    essential_tests = {
        # Main pages
        "": {"type": "Main Website", "expected": 200, "critical": True},
        "index.html": {"type": "Index Page", "expected": 200, "critical": True},
        
        # Core JavaScript libraries (required for functionality)
        "assets/js/jquery-1.11.2.min.js": {"type": "jQuery Library", "expected": 200, "critical": True},
        "assets/js/bootstrap.min.js": {"type": "Bootstrap JS", "expected": 200, "critical": True},
        "assets/js/custom.js": {"type": "Custom JavaScript", "expected": 200, "critical": True},
        "assets/js/main.js": {"type": "Main JavaScript", "expected": 200, "critical": True},
        "assets/js/github-activity-0.1.1.min.js": {"type": "GitHub Activity", "expected": 200, "critical": False},
        
        # Core CSS stylesheets
        "assets/css/bootstrap.min.css": {"type": "Bootstrap CSS", "expected": 200, "critical": True},
        "assets/css/main.css": {"type": "Main CSS", "expected": 200, "critical": True},
        "assets/css/style.css": {"type": "Style CSS", "expected": 200, "critical": True},
        "assets/css/font-awesome.min.css": {"type": "Font Awesome", "expected": 200, "critical": False},
        
        # Essential images
        "assets/img/Profile.jpg": {"type": "Profile Image", "expected": 200, "critical": True},
        "assets/img/favicon.ico": {"type": "Favicon", "expected": 200, "critical": False},
        
        # Important documents
        "assets/docs/resume/resume-prajit-das-032225.pdf": {"type": "Resume PDF", "expected": 200, "critical": True},
        
        # SEO and meta files (should be accessible)
        "robots.txt": {"type": "Robots File", "expected": 200, "critical": False},
        "sitemap.xml": {"type": "Sitemap", "expected": 200, "critical": False},
        "ror.xml": {"type": "ROR XML", "expected": 200, "critical": False},
        
        # Google verification (should be accessible)
        "google1733973a1d4ccc6c.html": {"type": "Google Verification", "expected": 200, "critical": False},
        
        # Error pages
        "assets/error-pages/404/404.html": {"type": "404 Error Page", "expected": 200, "critical": False},
    }
    
    # Test results tracking
    results = {
        "critical_passed": 0,
        "critical_total": 0,
        "optional_passed": 0,
        "optional_total": 0,
        "failed_tests": []
    }
    
    print("🧪 TESTING ESSENTIAL WEBSITE COMPONENTS:")
    print()
    
    for path, config in essential_tests.items():
        status_code, content_type = test_url_accessibility(base_url, path)
        test_type = config["type"]
        expected = config["expected"]
        is_critical = config["critical"]
        
        if is_critical:
            results["critical_total"] += 1
        else:
            results["optional_total"] += 1
        
        if status_code == expected:
            if is_critical:
                results["critical_passed"] += 1
                status_icon = "✅"
                status_text = "WORKING"
            else:
                results["optional_passed"] += 1
                status_icon = "✅"
                status_text = "Available"
        else:
            results["failed_tests"].append({
                "path": path,
                "type": test_type,
                "expected": expected,
                "actual": status_code,
                "critical": is_critical
            })
            
            if is_critical:
                status_icon = "❌"
                status_text = f"FAILED ({status_code})"
            else:
                status_icon = "⚠️"
                status_text = f"Unavailable ({status_code})"
        
        # Show content type for successful requests
        content_info = ""
        if status_code == 200 and content_type != "unknown":
            content_info = f" [{content_type.split(';')[0]}]"
        
        critical_marker = " [CRITICAL]" if is_critical else ""
        print(f"{status_icon} {test_type:<25} → {status_text}{content_info}{critical_marker}")
        
        time.sleep(0.1)  # Rate limiting
    
    # Additional functionality tests
    print("\n🔧 SECURITY VERIFICATION NOTE:")
    print("   Security file testing moved to comprehensive_security_scan.py")
    print("   Run that test for detailed security validation.")
    
    # Quick security check - just verify a few key moved files
    key_moved_files = ["SECURITY.md", "assets/HELP-US-OUT.txt"]
    security_passed = 0
    
    for file_path in key_moved_files:
        status_code, _ = test_url_accessibility(base_url, file_path)
        if status_code == 404:
            security_passed += 1
    
    # Final assessment
    print("\n" + "=" * 60)
    print("📊 WEBSITE FUNCTIONALITY SUMMARY")
    print("=" * 60)
    
    critical_success_rate = (results["critical_passed"] / results["critical_total"]) * 100 if results["critical_total"] > 0 else 100
    optional_success_rate = (results["optional_passed"] / results["optional_total"]) * 100 if results["optional_total"] > 0 else 100
    security_success_rate = (security_passed / len(key_moved_files)) * 100 if key_moved_files else 100
    
    print(f"🎯 CRITICAL COMPONENTS: {results['critical_passed']}/{results['critical_total']} ({critical_success_rate:.1f}%)")
    print(f"📋 OPTIONAL COMPONENTS: {results['optional_passed']}/{results['optional_total']} ({optional_success_rate:.1f}%)")
    print(f"🔒 SECURITY VERIFICATION: {security_passed}/{len(key_moved_files)} ({security_success_rate:.1f}%)")
    
    # Show failed tests
    if results["failed_tests"]:
        print(f"\n❌ FAILED TESTS ({len(results['failed_tests'])}):")
        for test in results["failed_tests"]:
            critical_text = " [CRITICAL]" if test["critical"] else ""
            print(f"   • {test['type']}: {test['path']} (Expected: {test['expected']}, Got: {test['actual']}){critical_text}")
    
    # Overall assessment
    print(f"\n🏆 OVERALL WEBSITE STATUS:")
    if critical_success_rate == 100:
        print("   ✅ FULLY FUNCTIONAL - All critical components working")
        if optional_success_rate >= 80:
            print("   🌟 EXCELLENT - Most optional features available")
        else:
            print("   ⚠️ DEGRADED - Some optional features unavailable")
    else:
        print("   ❌ IMPAIRED - Critical functionality issues detected")
    
    if security_success_rate >= 80:
        print("   🔒 SECURE - Key development files properly protected")
    else:
        print("   ⚠️ SECURITY CONCERN - Some key files still accessible")
    
    print(f"\n🔗 Test the website: {base_url}")
    
    # Return appropriate exit code
    if critical_success_rate == 100:
        return 0  # Success
    elif critical_success_rate >= 80:
        return 1  # Warning
    else:
        return 2  # Error

if __name__ == "__main__":
    exit_code = website_functionality_test()
    sys.exit(exit_code)