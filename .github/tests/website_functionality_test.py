#!/usr/bin/env python3
"""
Website Functionality Test
Tests that the website remains fully functional after security modifications.
Verifies that all essential assets, pages, and features are accessible.
"""

import requests
import sys
import re
from urllib.parse import urljoin, urlparse
import time
import re
from bs4 import BeautifulSoup

def test_url_accessibility(base_url, path, description=""):
    """Test if a URL is accessible and returns expected status code"""
    try:
        url = urljoin(base_url, path)
        response = requests.get(url, timeout=10, allow_redirects=True)
        return response.status_code, response.headers.get('content-type', 'unknown')
    except requests.RequestException as e:
        return 0, f"Error: {str(e)}"

def extract_links_from_html(html_content, base_url):
    """Extract all links from HTML content"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        # Extract href links
        for tag in soup.find_all(['a', 'link'], href=True):
            href = tag['href']
            if href and not href.startswith('#'):  # Skip anchors
                links.append(href)
        
        # Extract src links (images, scripts)
        for tag in soup.find_all(['img', 'script'], src=True):
            src = tag['src']
            if src:
                links.append(src)
        
        # Extract CSS background images
        for tag in soup.find_all(style=True):
            style = tag['style']
            bg_images = re.findall(r'url\(["\']?([^"\']+)["\']?\)', style)
            links.extend(bg_images)
        
        return links
    except Exception as e:
        print(f"⚠️ Error parsing HTML: {e}")
        return []

def test_website_links(base_url, max_links=50):
    """Test links found on the main website page"""
    print("\n🔗 TESTING WEBSITE LINKS:")
    print("-" * 40)
    
    try:
        # Get main page content
        response = requests.get(base_url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Could not fetch main page: {response.status_code}")
            return {"total": 0, "working": 0, "broken": 0, "external": 0}
        
        # Extract links
        links = extract_links_from_html(response.text, base_url)
        
        # Filter and categorize links
        internal_links = []
        external_links = []
        
        for link in links[:max_links]:  # Limit to prevent excessive testing
            parsed = urlparse(link)
            
            # Skip data URLs, javascript, mailto, etc.
            if link.startswith(('data:', 'javascript:', 'mailto:', 'tel:')):
                continue
                
            if parsed.netloc == '' or 'prajitdas.github.io' in parsed.netloc:
                # Internal link
                if not link.startswith('http'):
                    link = urljoin(base_url, link)
                internal_links.append(link)
            else:
                # External link
                external_links.append(link)
        
        print(f"📊 Found {len(internal_links)} internal links and {len(external_links)} external links")
        
        # Test internal links
        working_internal = 0
        broken_internal = []
        
        print(f"\n🏠 Testing {len(internal_links)} internal links:")
        for i, link in enumerate(internal_links[:20], 1):  # Limit internal testing
            try:
                response = requests.get(link, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    working_internal += 1
                    print(f"  ✅ [{i:2d}] {link.replace(base_url, '')}")
                else:
                    broken_internal.append({"url": link, "status": response.status_code})
                    print(f"  ❌ [{i:2d}] {link.replace(base_url, '')} ({response.status_code})")
            except requests.RequestException as e:
                broken_internal.append({"url": link, "status": "error"})
                print(f"  ❌ [{i:2d}] {link.replace(base_url, '')} (Error)")
            
            time.sleep(0.2)  # Rate limiting
        
        # Test external links with special handling for specific domains
        working_external = 0
        broken_external = []
        
        # Filter out problematic base domains and replace with actual working URLs
        filtered_external = []
        google_fonts_css_found = False
        
        for link in external_links[:10]:  # Check more links to find actual CSS URLs
            # Skip base domains that are expected to return 404
            if link in ['https://fonts.googleapis.com', 'https://fonts.gstatic.com']:
                continue
            # Check if we found the actual Google Fonts CSS URL
            elif 'fonts.googleapis.com/css' in link:
                google_fonts_css_found = True
                filtered_external.append(link)
            else:
                filtered_external.append(link)
        
        # If we didn't find the CSS URL in links, add it manually for testing
        if not google_fonts_css_found:
            # Extract the actual Google Fonts CSS URL from the HTML
            google_fonts_match = re.search(r'https://fonts\.googleapis\.com/css2\?[^"\']*', response.text)
            if google_fonts_match:
                filtered_external.insert(0, google_fonts_match.group(0))
        
        sample_external = filtered_external[:5]  # Test only first 5 filtered external links
        
        if sample_external:
            print(f"\n🌐 Testing {len(sample_external)} sample external links:")
            for i, link in enumerate(sample_external, 1):
                try:
                    # Special handling for different link types
                    if 'fonts.googleapis.com/css' in link:
                        # Test Google Fonts CSS specifically
                        response = requests.get(link, timeout=10, allow_redirects=True)
                        if response.status_code == 200:
                            working_external += 1
                            print(f"  ✅ [{i}] Google Fonts CSS")
                        else:
                            broken_external.append({"url": link, "status": response.status_code})
                            print(f"  ❌ [{i}] Google Fonts CSS ({response.status_code})")
                    else:
                        # Test other external links normally
                        response = requests.head(link, timeout=10, allow_redirects=True)  # Use HEAD for faster testing
                        if response.status_code == 200:
                            working_external += 1
                            domain = urlparse(link).netloc
                            print(f"  ✅ [{i}] {domain}")
                        else:
                            broken_external.append({"url": link, "status": response.status_code})
                            domain = urlparse(link).netloc
                            print(f"  ❌ [{i}] {domain} ({response.status_code})")
                except requests.RequestException:
                    broken_external.append({"url": link, "status": "error"})
                    domain = urlparse(link).netloc if link.startswith('http') else link[:30]
                    print(f"  ⚠️ [{i}] {domain} (Timeout/Error)")
                
                time.sleep(0.5)  # More conservative rate limiting for external
        
        # Summary
        total_tested = len(internal_links) + len(sample_external)
        total_working = working_internal + working_external
        total_broken = len(broken_internal) + len(broken_external)
        
        print(f"\n📊 LINK TEST SUMMARY:")
        print(f"   🔗 Internal Links: {working_internal}/{len(internal_links)} working")
        if sample_external:
            print(f"   🌐 External Links: {working_external}/{len(sample_external)} working (sample)")
        print(f"   📈 Overall: {total_working}/{total_tested} links working ({(total_working/total_tested*100):.1f}%)")
        
        if broken_internal:
            print(f"\n❌ BROKEN INTERNAL LINKS ({len(broken_internal)}):")
            for link_info in broken_internal[:10]:  # Show first 10
                print(f"   • {link_info['url'].replace(base_url, '')} [{link_info['status']}]")
        
        return {
            "total": total_tested,
            "working": total_working,
            "broken": total_broken,
            "internal": {"total": len(internal_links), "working": working_internal},
            "external": {"total": len(sample_external), "working": working_external}
        }
        
    except Exception as e:
        print(f"❌ Error testing links: {e}")
        return {"total": 0, "working": 0, "broken": 0, "external": 0}

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
    
    # Link Testing
    link_results = test_website_links(base_url)
    
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
    link_success_rate = (link_results["working"] / link_results["total"]) * 100 if link_results["total"] > 0 else 100
    
    print(f"🎯 CRITICAL COMPONENTS: {results['critical_passed']}/{results['critical_total']} ({critical_success_rate:.1f}%)")
    print(f"📋 OPTIONAL COMPONENTS: {results['optional_passed']}/{results['optional_total']} ({optional_success_rate:.1f}%)")
    print(f"🔗 LINK VALIDATION: {link_results['working']}/{link_results['total']} ({link_success_rate:.1f}%)")
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
    
    if link_success_rate >= 90:
        print("   🔗 EXCELLENT LINKS - All tested links working properly")
    elif link_success_rate >= 80:
        print("   🔗 GOOD LINKS - Most links working properly")
    else:
        print("   ⚠️ LINK ISSUES - Some broken links detected")
    
    if security_success_rate >= 80:
        print("   🔒 SECURE - Key development files properly protected")
    else:
        print("   ⚠️ SECURITY CONCERN - Some key files still accessible")
    
    print(f"\n🔗 Test the website: {base_url}")
    
    # Return appropriate exit code (prioritize critical functionality)
    if critical_success_rate == 100:
        if link_success_rate >= 80:
            return 0  # Success
        else:
            return 1  # Warning (links broken but core functionality works)
    elif critical_success_rate >= 80:
        return 1  # Warning
    else:
        return 2  # Error

if __name__ == "__main__":
    exit_code = website_functionality_test()
    sys.exit(exit_code)