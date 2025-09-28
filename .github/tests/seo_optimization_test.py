#!/usr/bin/env python3
"""
SEO Optimization Test
Tests specific SEO improvements and validates implementation
"""

import requests
from bs4 import BeautifulSoup
import json
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

def test_sitemap_enhancement():
    """Test sitemap improvements"""
    
    print("\n🗺️ SITEMAP ENHANCEMENT TEST:")
    print("-" * 40)
    
    try:
        sitemap_url = "https://prajitdas.github.io/sitemap.xml"
        response = requests.get(sitemap_url, timeout=10)
        
        if response.status_code == 200:
            sitemap_content = response.text
            
            # Count URLs
            url_count = sitemap_content.count('<url>')
            print(f"URLs in sitemap: {url_count}")
            
            # Check for priority tags
            priority_count = sitemap_content.count('<priority>')
            print(f"Priority tags: {priority_count}")
            
            # Check for changefreq tags
            changefreq_count = sitemap_content.count('<changefreq>')
            print(f"Change frequency tags: {changefreq_count}")
            
            # Check for lastmod tags
            lastmod_count = sitemap_content.count('<lastmod>')
            print(f"Last modified tags: {lastmod_count}")
            
            if url_count >= 5 and priority_count >= 5:
                print("✅ Sitemap properly enhanced")
                return True
            else:
                print("❌ Sitemap needs more URLs or priority tags")
                return False
        else:
            print(f"❌ Sitemap not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Sitemap test error: {e}")
        return False

if __name__ == "__main__":
    seo_success = test_seo_optimizations()
    sitemap_success = test_sitemap_enhancement()
    
    if seo_success and sitemap_success:
        print("\n🎉 ALL SEO IMPROVEMENTS SUCCESSFULLY IMPLEMENTED!")
        sys.exit(0)
    else:
        print("\n⚠️ Some SEO improvements need attention")
        sys.exit(1)