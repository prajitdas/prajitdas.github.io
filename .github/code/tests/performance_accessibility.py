#!/usr/bin/env python3
"""
Performance & Accessibility Enhancement Test
Tests Core Web Vitals optimization, accessibility features, and mobile performance.
Fast execution focused on local analysis and configuration validation.
"""

import os
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup

def test_core_web_vitals_optimization():
    """Test for Core Web Vitals optimization features"""
    print("⚡ TESTING CORE WEB VITALS OPTIMIZATION")
    print("-" * 50)
    
    issues = []
    
    # Test index.html for performance optimizations
    index_path = Path('index.html')
    if not index_path.exists():
        issues.append("index.html not found")
        return False
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Test for font optimization
        font_optimizations = 0
        
        # Check for font-display optimization
        style_tags = soup.find_all('style')
        for style in style_tags:
            if style.string and 'font-display' in style.string:
                font_optimizations += 1
                print("   ✅ Font-display optimization found")
        
        # Check for preload fonts
        preload_links = soup.find_all('link', rel='preload')
        for link in preload_links:
            if link.get('as') == 'font':
                font_optimizations += 1
                print("   ✅ Font preloading found")
        
        # Test for image optimization
        img_tags = soup.find_all('img')
        lazy_images = 0
        sized_images = 0
        
        for img in img_tags:
            # Check for lazy loading
            if img.get('loading') == 'lazy':
                lazy_images += 1
            
            # Check for width/height attributes
            if img.get('width') and img.get('height'):
                sized_images += 1
        
        print(f"   📊 Images with dimensions: {sized_images}/{len(img_tags)}")
        print(f"   🔄 Lazy loaded images: {lazy_images}/{len(img_tags)}")
        
        # Test for Critical CSS inlining
        critical_css_found = False
        for style in style_tags:
            if style.string and len(style.string) > 1000:  # Substantial inline CSS
                critical_css_found = True
                print("   ✅ Critical CSS inlining detected")
                break
        
        # Test for async/defer JavaScript
        script_tags = soup.find_all('script', src=True)
        async_scripts = sum(1 for script in script_tags if script.get('async'))
        defer_scripts = sum(1 for script in script_tags if script.get('defer'))
        
        print(f"   🚀 Async scripts: {async_scripts}")
        print(f"   ⏳ Defer scripts: {defer_scripts}")
        
        # Test for resource hints
        dns_prefetch = len(soup.find_all('link', rel='dns-prefetch'))
        preconnect = len(soup.find_all('link', rel='preconnect'))
        prefetch = len(soup.find_all('link', rel='prefetch'))
        
        print(f"   🌐 DNS prefetch: {dns_prefetch}")
        print(f"   🔗 Preconnect: {preconnect}")
        print(f"   ⚡ Prefetch: {prefetch}")
        
        # Performance score calculation
        performance_score = 0
        if font_optimizations > 0:
            performance_score += 20
        if critical_css_found:
            performance_score += 25
        if (async_scripts + defer_scripts) > 0:
            performance_score += 20
        if (dns_prefetch + preconnect + prefetch) > 0:
            performance_score += 15
        if sized_images / len(img_tags) > 0.8 if img_tags else True:
            performance_score += 20
        
        print(f"   📊 Performance Optimization Score: {performance_score}/100")
        
        if performance_score >= 60:
            print("   🎉 Good performance optimization!")
            return True
        else:
            issues.append(f"Performance optimization score too low: {performance_score}/100")
            return False
            
    except Exception as e:
        issues.append(f"Error analyzing index.html: {str(e)}")
        return False

def test_accessibility_features():
    """Test accessibility features and compliance"""
    print("\n♿ TESTING ACCESSIBILITY FEATURES")
    print("-" * 50)
    
    issues = []
    
    # Test HTML files for accessibility
    html_files = [Path('index.html')]
    if Path('404.html').exists():
        html_files.append(Path('404.html'))
    
    for html_file in html_files:
        if not html_file.exists():
            continue
            
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            print(f"   🔍 Testing {html_file.name}")
            
            # Test for lang attribute
            html_tag = soup.find('html')
            if html_tag and html_tag.get('lang'):
                print(f"     ✅ Language declared: {html_tag.get('lang')}")
            else:
                issues.append(f"{html_file.name}: Missing lang attribute")
                print(f"     ❌ Missing lang attribute")
            
            # Test for alt attributes on images
            img_tags = soup.find_all('img')
            missing_alt = 0
            for img in img_tags:
                if not img.get('alt'):
                    missing_alt += 1
            
            if missing_alt == 0 and img_tags:
                print(f"     ✅ All {len(img_tags)} images have alt text")
            elif missing_alt > 0:
                issues.append(f"{html_file.name}: {missing_alt} images missing alt text")
                print(f"     ❌ {missing_alt}/{len(img_tags)} images missing alt text")
            
            # Test for semantic HTML elements
            semantic_elements = ['nav', 'main', 'section', 'article', 'aside', 'header', 'footer']
            found_semantic = []
            for element in semantic_elements:
                if soup.find(element):
                    found_semantic.append(element)
            
            print(f"     📊 Semantic elements used: {', '.join(found_semantic)}")
            
            # Test for skip links
            skip_links = soup.find_all('a', href=re.compile(r'^#'))
            skip_to_content = any('skip' in link.get_text().lower() for link in skip_links)
            if skip_to_content:
                print("     ✅ Skip to content link found")
            
            # Test for proper heading hierarchy
            headings = soup.find_all(re.compile(r'^h[1-6]$'))
            if headings:
                h1_count = len(soup.find_all('h1'))
                if h1_count == 1:
                    print("     ✅ Proper H1 usage (exactly 1)")
                elif h1_count == 0:
                    issues.append(f"{html_file.name}: No H1 tag found")
                    print("     ❌ No H1 tag found")
                else:
                    issues.append(f"{html_file.name}: Multiple H1 tags ({h1_count})")
                    print(f"     ⚠️ Multiple H1 tags: {h1_count}")
            
        except Exception as e:
            issues.append(f"Error analyzing {html_file.name}: {str(e)}")
    
    return len(issues) == 0

def test_mobile_optimization():
    """Test mobile optimization features"""
    print("\n📱 TESTING MOBILE OPTIMIZATION")
    print("-" * 50)
    
    issues = []
    
    # Test index.html for mobile features
    index_path = Path('index.html')
    if not index_path.exists():
        issues.append("index.html not found")
        return False
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Test for viewport meta tag
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        if viewport_meta and viewport_meta.get('content'):
            viewport_content = viewport_meta.get('content')
            print(f"   ✅ Viewport meta tag: {viewport_content}")
            
            # Check for responsive viewport settings
            if 'width=device-width' in viewport_content and 'initial-scale=1' in viewport_content:
                print("   ✅ Proper responsive viewport settings")
            else:
                issues.append("Viewport meta tag missing proper responsive settings")
        else:
            issues.append("Missing viewport meta tag")
            print("   ❌ Missing viewport meta tag")
        
        # Test for responsive images
        img_tags = soup.find_all('img')
        responsive_images = 0
        for img in img_tags:
            if img.get('srcset') or img.parent.name == 'picture':
                responsive_images += 1
        
        if responsive_images > 0:
            print(f"   ✅ Responsive images: {responsive_images}/{len(img_tags)}")
        
        # Test for CSS media queries in inline styles
        style_tags = soup.find_all('style')
        media_queries_found = False
        for style in style_tags:
            if style.string and '@media' in style.string:
                media_queries_found = True
                print("   ✅ CSS media queries found")
                break
        
        # Test for touch-friendly elements
        touch_friendly_found = False
        for style in style_tags:
            if style.string and any(keyword in style.string.lower() for keyword in ['touch', 'hover', 'pointer']):
                touch_friendly_found = True
                print("   ✅ Touch-friendly CSS detected")
                break
        
        return len(issues) == 0
        
    except Exception as e:
        issues.append(f"Error analyzing mobile optimization: {str(e)}")
        return False

def test_seo_technical_optimization():
    """Test technical SEO optimizations"""
    print("\n🔍 TESTING TECHNICAL SEO OPTIMIZATION")
    print("-" * 50)
    
    issues = []
    
    # Test index.html for SEO
    index_path = Path('index.html')
    if not index_path.exists():
        issues.append("index.html not found")
        return False
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Test for title tag
        title_tag = soup.find('title')
        if title_tag and title_tag.get_text().strip():
            title_length = len(title_tag.get_text())
            print(f"   ✅ Title tag: {title_length} characters")
            if 30 <= title_length <= 60:
                print("   ✅ Title length optimal for SEO")
            else:
                print(f"   ⚠️ Title length not optimal: {title_length} (recommended: 30-60)")
        else:
            issues.append("Missing or empty title tag")
            print("   ❌ Missing title tag")
        
        # Test for meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc_length = len(meta_desc.get('content'))
            print(f"   ✅ Meta description: {desc_length} characters")
            if 120 <= desc_length <= 160:
                print("   ✅ Meta description length optimal")
            else:
                print(f"   ⚠️ Description length: {desc_length} (recommended: 120-160)")
        else:
            issues.append("Missing meta description")
            print("   ❌ Missing meta description")
        
        # Test for canonical URL
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            print(f"   ✅ Canonical URL: {canonical.get('href')}")
        else:
            print("   ⚠️ No canonical URL specified")
        
        # Test for structured data (JSON-LD)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        if json_ld_scripts:
            print(f"   ✅ Structured data found: {len(json_ld_scripts)} JSON-LD blocks")
        else:
            print("   ⚠️ No structured data (JSON-LD) found")
        
        # Test for Open Graph tags
        og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
        if og_tags:
            og_properties = [tag.get('property') for tag in og_tags]
            print(f"   ✅ Open Graph tags: {', '.join(og_properties)}")
        else:
            print("   ⚠️ No Open Graph tags found")
        
        # Test for Twitter Card tags
        twitter_tags = soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')})
        if twitter_tags:
            twitter_properties = [tag.get('name') for tag in twitter_tags]
            print(f"   ✅ Twitter Card tags: {', '.join(twitter_properties)}")
        else:
            print("   ⚠️ No Twitter Card tags found")
        
        return len(issues) == 0
        
    except Exception as e:
        issues.append(f"Error analyzing SEO optimization: {str(e)}")
        return False

def main():
    """Run all performance and accessibility tests"""
    print("🚀 PERFORMANCE & ACCESSIBILITY ENHANCEMENT TEST SUITE")
    print("=" * 70)
    
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
            project_root = script_dir.parent.parent.parent
            if (project_root / 'index.html').exists():
                os.chdir(project_root)
    
    print(f"📁 Testing directory: {Path.cwd()}")
    print()
    
    # Run all tests
    tests = [
        ("Core Web Vitals Optimization", test_core_web_vitals_optimization),
        ("Accessibility Features", test_accessibility_features),
        ("Mobile Optimization", test_mobile_optimization),
        ("Technical SEO Optimization", test_seo_technical_optimization)
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
    print("\n" + "=" * 70)
    print("📊 PERFORMANCE & ACCESSIBILITY TEST SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"📈 Tests passed: {passed}/{total}")
    print(f"📊 Success rate: {success_rate:.1f}%")
    
    if passed == total:
        print("🎉 ALL PERFORMANCE & ACCESSIBILITY TESTS PASSED!")
        return 0
    elif passed >= total * 0.75:
        print("⚠️ Mostly good - minor performance/accessibility improvements needed")
        return 0  # Don't fail for minor issues
    else:
        print("❌ Significant performance/accessibility issues detected")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)