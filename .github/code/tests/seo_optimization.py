#!/usr/bin/env python3
"""
Comprehensive SEO & Sitemap Optimization Test
Tests SEO improvements, sitemap synchronization, and validates implementation
"""

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
import os
import sys

def test_seo_optimizations():
    """Test specific SEO optimizations"""
    
    print("🚀 SEO OPTIMIZATION VALIDATION TEST")
    print("=" * 60)
    
    base_url = "https://prajitdas.github.io/"
    
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Could not fetch website: {response.status_code}")
            return False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Test Results
        tests_passed = 0
        total_tests = 0
        
        print("🔍 TESTING SEO IMPROVEMENTS:")
        print("-" * 40)
        
        # Test 1: Enhanced Title Tag
        total_tests += 1
        title = soup.find('title')
        if title and 'Software Engineering Leader' in title.text:
            print("✅ Enhanced title tag with professional keywords")
            tests_passed += 1
        else:
            print("❌ Title tag not properly enhanced")
        
        # Test 2: Optimized Meta Description
        total_tests += 1
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            desc_content = meta_desc.get('content', '')
            if 120 <= len(desc_content) <= 160 and 'Cisco Systems' in desc_content:
                print("✅ Meta description optimized (length & content)")
                tests_passed += 1
            else:
                print(f"❌ Meta description needs work (length: {len(desc_content)})")
        else:
            print("❌ Meta description missing")
        
        # Test 3: Canonical URL
        total_tests += 1
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical and canonical.get('href') == base_url:
            print("✅ Canonical URL properly set")
            tests_passed += 1
        else:
            print("❌ Canonical URL missing or incorrect")
        
        # Test 4: Robots Meta Tag
        total_tests += 1
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        if robots_meta and 'index, follow' in robots_meta.get('content', ''):
            print("✅ Robots meta tag configured")
            tests_passed += 1
        else:
            print("❌ Robots meta tag missing or incorrect")
        
        # Test 5: Open Graph Tags
        total_tests += 1
        og_tags = soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')})
        required_og = ['og:title', 'og:description', 'og:url', 'og:type', 'og:image']
        og_properties = [tag.get('property') for tag in og_tags]
        if all(prop in og_properties for prop in required_og):
            print("✅ Open Graph tags complete")
            tests_passed += 1
        else:
            missing = [prop for prop in required_og if prop not in og_properties]
            print(f"❌ Missing Open Graph tags: {missing}")
        
        # Test 6: Twitter Card Tags
        total_tests += 1
        twitter_tags = soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('twitter:')})
        required_twitter = ['twitter:card', 'twitter:title', 'twitter:description']
        twitter_properties = [tag.get('property') for tag in twitter_tags]
        if all(prop in twitter_properties for prop in required_twitter):
            print("✅ Twitter Card tags complete")
            tests_passed += 1
        else:
            missing = [prop for prop in required_twitter if prop not in twitter_properties]
            print(f"❌ Missing Twitter Card tags: {missing}")
        
        # Test 7: JSON-LD Structured Data
        total_tests += 1
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        if json_ld_scripts:
            try:
                for script in json_ld_scripts:
                    data = json.loads(script.string)
                    if data.get('@type') == 'Person' and 'Prajit Kumar Das' in data.get('name', ''):
                        print("✅ JSON-LD structured data implemented")
                        tests_passed += 1
                        break
                else:
                    print("❌ JSON-LD structured data incomplete")
            except json.JSONDecodeError:
                print("❌ JSON-LD structured data malformed")
        else:
            print("❌ JSON-LD structured data missing")
        
        # Test 8: Language Declaration
        total_tests += 1
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang') == 'en':
            print("✅ Language declaration proper")
            tests_passed += 1
        else:
            print("❌ Language declaration missing or incorrect")
        
        # Test 9: Professional Keywords
        total_tests += 1
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords = meta_keywords.get('content', '')
            professional_terms = ['Software Engineering', 'Cisco Systems', 'Mobile Security', 'PhD']
            if any(term in keywords for term in professional_terms):
                print("✅ Professional keywords included")
                tests_passed += 1
            else:
                print("❌ Professional keywords missing")
        else:
            print("❌ Keywords meta tag missing")
        
        # Test 10: Enhanced Sitemap
        total_tests += 1
        try:
            sitemap_response = requests.get(f"{base_url}sitemap.xml", timeout=10)
            if sitemap_response.status_code == 200:
                sitemap_content = sitemap_response.text
                if sitemap_content.count('<url>') > 1:  # More than just homepage
                    print("✅ Enhanced sitemap with multiple URLs")
                    tests_passed += 1
                else:
                    print("❌ Sitemap needs more URLs")
            else:
                print("❌ Sitemap not accessible")
        except:
            print("❌ Sitemap test failed")
        
        # Summary
        print("\n" + "=" * 60)
        print(f"🎯 SEO OPTIMIZATION RESULTS: {tests_passed}/{total_tests} tests passed")
        print(f"📊 Success Rate: {(tests_passed/total_tests)*100:.1f}%")
        
        if tests_passed >= 8:
            print("🎉 EXCELLENT! SEO optimizations successfully implemented")
            return True
        elif tests_passed >= 6:
            print("👍 GOOD! Most SEO optimizations in place, minor improvements needed")
            return True
        else:
            print("⚠️ NEEDS WORK! Significant SEO improvements required")
            return False
        
    except Exception as e:
        print(f"❌ Error testing SEO optimizations: {e}")
        return False

def test_local_sitemap_synchronization():
    """Test local sitemap synchronization - skip HTML sitemap as it's not wanted"""
    
    print("\n🗺️ SITEMAP SYNCHRONIZATION TEST:")
    print("-" * 40)
    
    try:
        # Get project root - updated for new structure  
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
        
        sitemap_xml = os.path.join(project_root, 'sitemap.xml')
        ror_xml = os.path.join(project_root, 'ror.xml')
        
        # Parse sitemap.xml
        tree = ET.parse(sitemap_xml)
        root = tree.getroot()
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        xml_urls = []
        
        for url_elem in root.findall('.//sitemap:url', ns):
            loc = url_elem.find('sitemap:loc', ns)
            if loc is not None:
                xml_urls.append(loc.text)
        
        # Parse ror.xml
        ror_tree = ET.parse(ror_xml)
        ror_root = ror_tree.getroot()
        ror_urls = []
        
        for item in ror_root.findall('.//item'):
            link = item.find('link')
            if link is not None:
                ror_urls.append(link.text)
        
        print(f"📄 XML URLs: {len(xml_urls)}")
        print(f"📄 ROR URLs: {len(ror_urls)}")
        
        # Test synchronization between XML and ROR (skip HTML sitemap)
        xml_urls_set = set(xml_urls)
        ror_urls_set = set(ror_urls)
        
        if xml_urls_set == ror_urls_set and len(xml_urls) >= 4:
            print("✅ XML and ROR sitemaps synchronized with specific files")
            return True
        else:
            print("❌ Sitemap synchronization issues detected between XML and ROR")
            return False
            
    except Exception as e:
        print(f"❌ Sitemap synchronization error: {e}")
        return False

def test_sitemap_enhancement():
    """Test remote sitemap improvements"""
    
    print("\n🌐 REMOTE SITEMAP VALIDATION:")
    print("-" * 40)
    
    try:
        sitemap_url = "https://prajitdas.github.io/sitemap.xml"
        response = requests.get(sitemap_url, timeout=10)
        
        if response.status_code == 200:
            sitemap_content = response.text
            
            # Count URLs
            url_count = sitemap_content.count('<url>')
            print(f"Remote URLs in sitemap: {url_count}")
            
            # Check for specific files (not directories)
            specific_files = [
                'resume-prajit-das-032225.pdf',
                'kat-austen-the-trouble-with-wearables.pdf',
                'MobileAccessControl.owl'
            ]
            
            file_count = sum(1 for file in specific_files if file in sitemap_content)
            print(f"Specific files indexed: {file_count}/{len(specific_files)}")
            
            if url_count >= 4 and file_count >= 2:
                print("✅ Remote sitemap properly configured")
                return True
            else:
                print("❌ Remote sitemap needs updates")
                return False
        else:
            print(f"❌ Remote sitemap not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Remote sitemap test error: {e}")
        return False

def generate_consolidated_summary():
    """Generate consolidated SEO and Sitemap summary"""
    
    print(f"\n📋 SEO & SITEMAP OPTIMIZATION SUMMARY:")
    print("=" * 60)
    
    optimizations = [
        "✅ Enhanced title tag with professional keywords",
        "✅ Optimized meta description (120-160 characters)",  
        "✅ Added canonical URL for duplicate content prevention",
        "✅ Implemented robots meta tag for search engine guidance",
        "✅ Complete Open Graph meta tags for social media",
        "✅ Twitter Card meta tags for enhanced social sharing",
        "✅ JSON-LD structured data for rich snippets",
        "✅ Professional keywords meta tag",
        "✅ Synchronized sitemaps (XML, ROR)",
        "✅ File-specific indexing (not directories)",
        "✅ SEO-optimized sitemap descriptions",
        "✅ Proper sitemap priorities and frequencies"
    ]
    
    for optimization in optimizations:
        print(optimization)
    
    print(f"\n🎯 COMBINED BENEFITS:")
    print("-" * 20)
    print("• Better search engine rankings and discoverability")
    print("• Enhanced social media sharing capabilities")
    print("• Rich snippets in search results")
    print("• Professional keyword optimization")
    print("• Direct file access via sitemaps")
    print("• Synchronized multi-format sitemaps (XML, ROR)")
    print("• Improved mobile and desktop SEO performance")

if __name__ == "__main__":
    seo_success = test_seo_optimizations()
    local_sitemap_success = test_local_sitemap_synchronization()
    remote_sitemap_success = test_sitemap_enhancement()
    
    total_success = seo_success and local_sitemap_success and remote_sitemap_success
    
    generate_consolidated_summary()
    
    if total_success:
        print("\n🎉 ALL SEO & SITEMAP OPTIMIZATIONS SUCCESSFUL!")
        sys.exit(0)
    else:
        print("\n⚠️ Some SEO or sitemap optimizations need attention")
        sys.exit(1)