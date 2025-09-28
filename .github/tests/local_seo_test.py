#!/usr/bin/env python3
"""
Local SEO Validation Test
Tests SEO improvements in local files before deployment
"""

import os
from bs4 import BeautifulSoup
import json
import xml.etree.ElementTree as ET
import sys

def test_local_seo_improvements():
    """Test SEO improvements in local files"""
    
    print("🚀 LOCAL SEO OPTIMIZATION VALIDATION")
    print("=" * 60)
    
    # Get the script directory and find the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    index_file = os.path.join(project_root, 'index.html')
    sitemap_file = os.path.join(project_root, 'sitemap.xml')
    
    if not os.path.exists(index_file):
        print(f"❌ index.html not found at: {index_file}")
        return False
    
    # Read and parse index.html
    with open(index_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Test Results
    tests_passed = 0
    total_tests = 0
    
    print("🔍 TESTING LOCAL SEO IMPROVEMENTS:")
    print("-" * 40)
    
    # Test 1: Enhanced Title Tag
    total_tests += 1
    title = soup.find('title')
    if title and 'Software Engineering Leader' in title.text and 'Dr. Prajit Kumar Das' in title.text:
        print("✅ Enhanced title tag with professional keywords")
        tests_passed += 1
    else:
        print(f"❌ Title tag not properly enhanced: {title.text if title else 'Missing'}")
    
    # Test 2: Optimized Meta Description
    total_tests += 1
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        desc_content = meta_desc.get('content', '')
        if 120 <= len(desc_content) <= 160 and 'Cisco Systems' in desc_content:
            print(f"✅ Meta description optimized (length: {len(desc_content)} chars)")
            tests_passed += 1
        else:
            print(f"❌ Meta description needs work (length: {len(desc_content)} chars)")
    else:
        print("❌ Meta description missing")
    
    # Test 3: Canonical URL
    total_tests += 1
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical and 'prajitdas.github.io' in canonical.get('href', ''):
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
                if script.string:
                    data = json.loads(script.string.strip())
                    if data.get('@type') == 'Person' and 'Prajit Kumar Das' in data.get('name', ''):
                        print("✅ JSON-LD structured data implemented")
                        tests_passed += 1
                        break
            else:
                print("❌ JSON-LD structured data incomplete")
        except json.JSONDecodeError as e:
            print(f"❌ JSON-LD structured data malformed: {e}")
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
    if os.path.exists(sitemap_file):
        try:
            tree = ET.parse(sitemap_file)
            root = tree.getroot()
            
            # Count URL elements
            ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = root.findall('.//sitemap:url', ns)
            priorities = root.findall('.//sitemap:priority', ns)
            changefreqs = root.findall('.//sitemap:changefreq', ns)
            
            if len(urls) >= 5 and len(priorities) >= 5:
                print(f"✅ Enhanced sitemap with {len(urls)} URLs and priorities")
                tests_passed += 1
            else:
                print(f"❌ Sitemap needs improvement (URLs: {len(urls)}, Priorities: {len(priorities)})")
        except Exception as e:
            print(f"❌ Sitemap parsing error: {e}")
    else:
        print(f"❌ Sitemap file not found: {sitemap_file}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"🎯 LOCAL SEO RESULTS: {tests_passed}/{total_tests} tests passed")
    print(f"📊 Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed >= 8:
        print("🎉 EXCELLENT! Local SEO optimizations successfully implemented")
        return True
    elif tests_passed >= 6:
        print("👍 GOOD! Most SEO optimizations in place locally")
        return True
    else:
        print("⚠️ NEEDS WORK! Local SEO improvements incomplete")
        return False

def generate_seo_implementation_summary():
    """Generate summary of SEO improvements made"""
    
    print("\n📋 SEO IMPROVEMENTS IMPLEMENTED:")
    print("=" * 60)
    
    improvements = [
        "✅ Enhanced title tag with professional keywords",
        "✅ Optimized meta description (120-160 characters)",
        "✅ Added canonical URL for duplicate content prevention",
        "✅ Implemented robots meta tag for search engine guidance",
        "✅ Complete Open Graph meta tags for social media",
        "✅ Twitter Card meta tags for enhanced social sharing",
        "✅ JSON-LD structured data for rich snippets",
        "✅ Professional keywords meta tag",
        "✅ Enhanced XML sitemap with priorities and change frequencies",
        "✅ Proper language declaration"
    ]
    
    for improvement in improvements:
        print(improvement)
    
    print(f"\n🎯 KEY SEO BENEFITS:")
    print("-" * 20)
    print("• Better search engine rankings")
    print("• Enhanced social media sharing")
    print("• Rich snippets in search results")
    print("• Professional keyword optimization")
    print("• Improved click-through rates")
    print("• Better user experience")
    
    print(f"\n📈 NEXT STEPS:")
    print("-" * 20)
    print("• Deploy changes to GitHub Pages")
    print("• Monitor search engine rankings")
    print("• Add more content pages to sitemap")
    print("• Consider adding blog/news section")
    print("• Implement performance optimizations")

if __name__ == "__main__":
    success = test_local_seo_improvements()
    generate_seo_implementation_summary()
    
    if success:
        print("\n🎉 LOCAL SEO VALIDATION SUCCESSFUL!")
        sys.exit(0)
    else:
        print("\n⚠️ Local SEO validation needs attention")
        sys.exit(1)