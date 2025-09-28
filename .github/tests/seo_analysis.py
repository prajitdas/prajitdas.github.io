#!/usr/bin/env python3
"""
SEO Analysis and Improvement Tool
Analyzes current SEO status and provides recommendations
"""

import requests
import re
from bs4 import BeautifulSoup
import sys

def analyze_seo(base_url):
    """Analyze current SEO status of the website"""
    
    print("🔍 SEO ANALYSIS REPORT")
    print("=" * 60)
    print(f"🎯 Analyzing: {base_url}")
    print("=" * 60)
    
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Could not fetch website: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Basic SEO Elements
        print("\n📋 BASIC SEO ELEMENTS:")
        print("-" * 30)
        
        # Title Tag
        title = soup.find('title')
        title_text = title.text if title else "Not found"
        title_length = len(title_text)
        print(f"📝 Title: {title_text}")
        print(f"   Length: {title_length} chars ({'✅ Good' if 30 <= title_length <= 60 else '⚠️ Needs adjustment'})")
        
        # Meta Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            desc_text = meta_desc.get('content', '')
            desc_length = len(desc_text)
            print(f"📄 Meta Description: {desc_text[:100]}{'...' if len(desc_text) > 100 else ''}")
            print(f"   Length: {desc_length} chars ({'✅ Good' if 120 <= desc_length <= 160 else '⚠️ Needs adjustment'})")
        else:
            print("📄 Meta Description: ❌ Missing")
        
        # Meta Keywords (deprecated but sometimes used)
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            print(f"🏷️ Meta Keywords: {meta_keywords.get('content', '')[:100]}...")
        else:
            print("🏷️ Meta Keywords: Not set (good - deprecated)")
        
        # Heading Structure
        print("\n📊 HEADING STRUCTURE:")
        print("-" * 30)
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            if headings:
                print(f"H{i}: {len(headings)} found")
                for j, heading in enumerate(headings[:3], 1):  # Show first 3
                    text = heading.get_text(strip=True)[:60]
                    print(f"   {j}. {text}{'...' if len(heading.get_text(strip=True)) > 60 else ''}")
                if len(headings) > 3:
                    print(f"   ... and {len(headings) - 3} more")
        
        # Images Alt Text
        print("\n🖼️ IMAGE OPTIMIZATION:")
        print("-" * 30)
        images = soup.find_all('img')
        total_images = len(images)
        images_with_alt = len([img for img in images if img.get('alt')])
        print(f"Total Images: {total_images}")
        print(f"Images with Alt Text: {images_with_alt}/{total_images} ({(images_with_alt/total_images*100):.1f}%)")
        
        # Internal Links
        print("\n🔗 LINK ANALYSIS:")
        print("-" * 30)
        links = soup.find_all('a', href=True)
        internal_links = [link for link in links if not link['href'].startswith(('http://', 'https://', '#', 'mailto:', 'tel:'))]
        external_links = [link for link in links if link['href'].startswith(('http://', 'https://')) and 'prajitdas.github.io' not in link['href']]
        
        print(f"Total Links: {len(links)}")
        print(f"Internal Links: {len(internal_links)}")
        print(f"External Links: {len(external_links)}")
        
        # Schema Markup
        print("\n🏗️ STRUCTURED DATA:")
        print("-" * 30)
        json_ld = soup.find_all('script', type='application/ld+json')
        microdata = soup.find_all(attrs={'itemscope': True})
        print(f"JSON-LD Scripts: {len(json_ld)}")
        print(f"Microdata Elements: {len(microdata)}")
        
        # Open Graph Tags
        print("\n📱 SOCIAL MEDIA (Open Graph):")
        print("-" * 30)
        og_tags = soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')})
        twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
        print(f"Open Graph Tags: {len(og_tags)}")
        print(f"Twitter Card Tags: {len(twitter_tags)}")
        
        # Technical SEO
        print("\n⚙️ TECHNICAL SEO:")
        print("-" * 30)
        
        # Check for robots meta
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        print(f"Robots Meta: {'✅ ' + robots_meta.get('content') if robots_meta else '⚠️ Not set'}")
        
        # Check for canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        print(f"Canonical URL: {'✅ ' + canonical.get('href') if canonical else '⚠️ Not set'}")
        
        # Check language declaration
        html_lang = soup.find('html', attrs={'lang': True})
        print(f"Language Declaration: {'✅ ' + html_lang.get('lang') if html_lang else '⚠️ Not set'}")
        
        # Performance indicators
        print("\n⚡ PERFORMANCE INDICATORS:")
        print("-" * 30)
        css_files = len(soup.find_all('link', rel='stylesheet'))
        js_files = len(soup.find_all('script', src=True))
        print(f"CSS Files: {css_files} {'⚠️ Consider combining' if css_files > 5 else '✅ Good'}")
        print(f"JavaScript Files: {js_files} {'⚠️ Consider combining' if js_files > 5 else '✅ Good'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing SEO: {e}")
        return False

def generate_seo_recommendations():
    """Generate SEO improvement recommendations"""
    
    print("\n\n🚀 SEO IMPROVEMENT RECOMMENDATIONS")
    print("=" * 60)
    
    recommendations = [
        {
            "category": "📝 CONTENT OPTIMIZATION",
            "items": [
                "Update title tag to be more descriptive (30-60 chars)",
                "Optimize meta description (120-160 chars)",
                "Add location-based keywords (if relevant)",
                "Include target keywords in headings",
                "Add more descriptive alt text to images"
            ]
        },
        {
            "category": "🏗️ STRUCTURED DATA",
            "items": [
                "Add JSON-LD structured data for Person schema",
                "Include organization/professional schema markup",
                "Add breadcrumb navigation schema",
                "Implement article schema for blog posts/publications"
            ]
        },
        {
            "category": "📱 SOCIAL MEDIA",
            "items": [
                "Add Open Graph meta tags",
                "Include Twitter Card meta tags",
                "Add social media profile links",
                "Optimize images for social sharing"
            ]
        },
        {
            "category": "⚙️ TECHNICAL SEO",
            "items": [
                "Add canonical URL tags",
                "Implement robots meta tags",
                "Add hreflang for international targeting",
                "Optimize URL structure",
                "Add XML sitemap with more pages"
            ]
        },
        {
            "category": "⚡ PERFORMANCE",
            "items": [
                "Optimize image sizes and formats",
                "Minimize CSS and JavaScript",
                "Enable compression",
                "Add proper cache headers",
                "Consider lazy loading for images"
            ]
        }
    ]
    
    for rec in recommendations:
        print(f"\n{rec['category']}:")
        print("-" * (len(rec['category']) - 2))
        for item in rec['items']:
            print(f"• {item}")
    
    print(f"\n🎯 PRIORITY ACTIONS:")
    print("-" * 20)
    print("1. Add structured data (JSON-LD)")
    print("2. Optimize meta description")
    print("3. Add Open Graph tags")
    print("4. Improve heading structure")
    print("5. Add canonical URLs")

if __name__ == "__main__":
    base_url = "https://prajitdas.github.io/"
    
    success = analyze_seo(base_url)
    if success:
        generate_seo_recommendations()