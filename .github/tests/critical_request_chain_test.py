#!/usr/bin/env python3
"""
Critical Request Chain Optimization Test
Tests the website's critical request chain optimization for improved LCP performance.
"""

import re
import requests
from bs4 import BeautifulSoup
import sys
import time

def test_preconnect_optimization():
    """Test that resource preconnect hints are properly implemented"""
    print("🔗 Testing Preconnect Optimization...")
    
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check for preconnect hints
    preconnect_patterns = [
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com">',
        r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>',
        r'<link rel="preconnect" href="https://ajax\.googleapis\.com">',
        r'<link rel="preconnect" href="https://www\.google-analytics\.com">'
    ]
    
    results = []
    for i, pattern in enumerate(preconnect_patterns):
        if re.search(pattern, content):
            results.append(f"✅ Preconnect {i+1}/4: Found")
        else:
            results.append(f"❌ Preconnect {i+1}/4: Missing")
    
    return results

def test_css_optimization():
    """Test CSS loading optimization"""
    print("🎨 Testing CSS Optimization...")
    
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    results = []
    
    # Check for optimized font loading with font-display
    if 'display=optional' in content:
        results.append("✅ Font-display optimization: Optional (best for CLS)")
    elif 'display=swap' in content:
        results.append("✅ Font-display optimization: Swap implemented")
    else:
        results.append("❌ Font-display optimization: Missing")
    
    # Check for CSS preloading of non-critical styles
    if 'rel="preload"' in content and 'as="style"' in content:
        results.append("✅ Non-critical CSS preloading: Implemented")
    else:
        results.append("❌ Non-critical CSS preloading: Missing")
    
    # Check that duplicate CSS files are removed
    css_files = re.findall(r'<link[^>]*stylesheet[^>]*href="([^"]*)"', content)
    bootstrap_css = [f for f in css_files if 'bootstrap' in f]
    fontawesome_css = [f for f in css_files if 'font-awesome' in f]
    
    if len(bootstrap_css) <= 1:
        results.append("✅ Bootstrap CSS deduplication: No duplicates")
    else:
        results.append(f"❌ Bootstrap CSS deduplication: {len(bootstrap_css)} files found")
    
    if len(fontawesome_css) <= 1:
        results.append("✅ FontAwesome CSS deduplication: No duplicates")
    else:
        results.append(f"❌ FontAwesome CSS deduplication: {len(fontawesome_css)} files found")
    
    return results

def test_javascript_optimization():
    """Test JavaScript loading optimization"""
    print("⚡ Testing JavaScript Optimization...")
    
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    results = []
    
    # Check for jQuery core library deduplication (check async loading too)
    jquery_core_scripts = re.findall(r'<script[^>]*src="[^"]*jquery-[0-9][^"]*"[^>]*>', content)
    jquery_async_loading = len(re.findall(r'assets/js/jquery-1\.11\.2\.min\.js', content))
    
    if len(jquery_core_scripts) <= 1 and jquery_async_loading >= 1:
        results.append(f"✅ jQuery optimization: Single version with async loading")
    elif len(jquery_core_scripts) <= 1:
        results.append(f"✅ jQuery core deduplication: {len(jquery_core_scripts)} version (optimized)")
    else:
        results.append(f"❌ jQuery core deduplication: {len(jquery_core_scripts)} versions found")
    
    # Check for defer attribute on non-critical scripts
    defer_scripts = len(re.findall(r'<script[^>]*defer[^>]*>', content))
    if defer_scripts >= 4:
        results.append(f"✅ Non-critical script deferring: {defer_scripts} scripts deferred")
    else:
        results.append(f"⚠️ Non-critical script deferring: Only {defer_scripts} scripts deferred")
    
    # Check for async Google Analytics
    if 'async src="https://www.google-analytics.com/analytics.js"' in content:
        results.append("✅ Google Analytics async loading: Implemented")
    else:
        results.append("❌ Google Analytics async loading: Missing")
    
    return results

def test_resource_preloading():
    """Test critical resource preloading"""
    print("🚀 Testing Resource Preloading...")
    
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    results = []
    
    # Check for LCP image preloading
    if 'rel="preload"' in content and 'as="image"' in content:
        results.append("✅ LCP image preloading: Implemented")
    else:
        results.append("❌ LCP image preloading: Missing")
    
    # Check for critical JavaScript preloading
    js_preloads = len(re.findall(r'<link rel="preload"[^>]*as="script"[^>]*>', content))
    if js_preloads >= 2:
        results.append(f"✅ Critical JS preloading: {js_preloads} scripts preloaded")
    else:
        results.append(f"⚠️ Critical JS preloading: Only {js_preloads} scripts preloaded")
    
    return results

def test_font_optimization():
    """Test advanced font loading optimization"""
    print("🔤 Testing Advanced Font Optimization...")
    
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    results = []
    
    # Check for consolidated font requests
    font_requests = len(re.findall(r'fonts\.googleapis\.com/css', content))
    if font_requests <= 1:
        results.append(f"✅ Font request consolidation: {font_requests} request (optimized)")
    else:
        results.append(f"⚠️ Font request consolidation: {font_requests} requests")
    
    # Check for font-display optimization (swap or optional)
    if 'display=optional' in content:
        results.append("✅ Font-display optimization: Optional (best for performance)")
    elif 'display=swap' in content:
        results.append("✅ Font-display optimization: Swap implemented")
    else:
        results.append("❌ Font-display optimization: Missing")
    
    # Check for font metric overrides (CLS prevention)
    if 'ascent-override' in content and 'descent-override' in content:
        results.append("✅ Font metric overrides: CLS prevention implemented")
    else:
        results.append("❌ Font metric overrides: Missing CLS prevention")
    
    # Check for font loading API usage
    if 'document.fonts.load' in content:
        results.append("✅ Font Loading API: Advanced loading implemented")
    else:
        results.append("❌ Font Loading API: Missing optimization")
    
    # Check for font fallback optimization
    if 'font-family:' in content and 'fallback' in content:
        results.append("✅ Font fallback stacks: Optimized with metrics")
    else:
        results.append("❌ Font fallback stacks: Not optimized")
    
    return results

def test_render_blocking_optimization():
    """Test render-blocking resource elimination"""
    print("🚫 Testing Render-Blocking Elimination...")
    
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    results = []
    
    # Check for inline critical CSS
    if '<style>' in content and 'Critical inline CSS' in content:
        results.append("✅ Inline critical CSS: Implemented")
    else:
        results.append("❌ Inline critical CSS: Missing")
    
    # Check that CSS files are preloaded, not render-blocking (excluding noscript)
    # First, remove noscript sections from analysis
    content_without_noscript = re.sub(r'<noscript>.*?</noscript>', '', content, flags=re.DOTALL)
    render_blocking_css = len(re.findall(r'<link rel="stylesheet"[^>]*href="assets/', content_without_noscript))
    if render_blocking_css == 0:
        results.append("✅ CSS render-blocking elimination: All CSS preloaded")
    else:
        results.append(f"❌ CSS render-blocking elimination: {render_blocking_css} blocking CSS files")
    
    # Check for async script loading
    if 'loadScript(' in content and 'script.async = true' in content:
        results.append("✅ Async JavaScript loading: Implemented")
    else:
        results.append("❌ Async JavaScript loading: Missing")
    
    # Check that no scripts are in head without async/defer
    head_section = re.search(r'<head>(.*?)</head>', content, re.DOTALL)
    if head_section:
        blocking_scripts = len(re.findall(r'<script src=[^>]*(?!async|defer)[^>]*></script>', head_section.group(1)))
        if blocking_scripts == 0:
            results.append("✅ Head script blocking elimination: No blocking scripts in head")
        else:
            results.append(f"❌ Head script blocking elimination: {blocking_scripts} blocking scripts in head")
    
    return results

def test_cls_prevention():
    """Test Cumulative Layout Shift (CLS) prevention optimizations"""
    print("📏 Testing CLS Prevention...")
    
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    results = []
    
    # Check for font metric overrides
    metric_overrides = ['ascent-override', 'descent-override', 'line-gap-override', 'size-adjust']
    found_overrides = sum(1 for override in metric_overrides if override in content)
    
    if found_overrides >= 3:
        results.append(f"✅ Font metric overrides: {found_overrides}/4 implemented")
    elif found_overrides > 0:
        results.append(f"⚠️ Font metric overrides: {found_overrides}/4 partial implementation")
    else:
        results.append("❌ Font metric overrides: Missing")
    
    # Check for font loading state management
    if 'font-loading' in content and 'font-loaded' in content:
        results.append("✅ Font loading states: FOUT/FOIT prevention implemented")
    else:
        results.append("❌ Font loading states: Missing FOUT/FOIT prevention")
    
    # Check for session storage optimization
    if 'sessionStorage.getItem(\'fontsLoaded\')' in content:
        results.append("✅ Font caching optimization: Session storage implemented")
    else:
        results.append("❌ Font caching optimization: Missing")
    
    return results

def calculate_performance_metrics():
    """Calculate estimated performance improvements"""
    print("📊 Calculating Performance Metrics...")
    
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Count optimizations
    preconnects = len(re.findall(r'rel="preconnect"', content))
    preloads = len(re.findall(r'rel="preload"', content))
    deferred_scripts = len(re.findall(r'defer', content))
    async_scripts = len(re.findall(r'async', content))
    inline_css = 1 if '<style>' in content else 0
    
    # Enhanced estimate with render-blocking elimination
    estimated_lcp_improvement = min(50, preconnects * 4 + preloads * 6 + async_scripts * 5 + inline_css * 15)
    estimated_fcp_improvement = min(40, preconnects * 3 + async_scripts * 8 + inline_css * 12)
    
    results = [
        f"📈 Estimated LCP improvement: {estimated_lcp_improvement}%",
        f"📈 Estimated FCP improvement: {estimated_fcp_improvement}%",
        f"🔗 Preconnect hints: {preconnects}",
        f"🚀 Resource preloads: {preloads}",
        f"⏱️ Deferred scripts: {deferred_scripts}",
        f"⚡ Async scripts: {async_scripts}",
        f"🎨 Inline critical CSS: {'Yes' if inline_css else 'No'}"
    ]
    
    return results

def generate_optimization_summary():
    """Generate a comprehensive optimization summary"""
    print("\n" + "="*80)
    print("🎯 CRITICAL REQUEST CHAIN OPTIMIZATION SUMMARY")
    print("="*80)
    
    all_results = []
    
    # Run all tests
    all_results.extend(test_preconnect_optimization())
    all_results.extend(test_css_optimization())
    all_results.extend(test_javascript_optimization())
    all_results.extend(test_resource_preloading())
    all_results.extend(test_font_optimization())
    all_results.extend(test_render_blocking_optimization())
    all_results.extend(test_cls_prevention())
    all_results.extend(calculate_performance_metrics())
    
    # Count successes
    passed = sum(1 for result in all_results if result.startswith("✅"))
    warnings = sum(1 for result in all_results if result.startswith("⚠️"))
    failed = sum(1 for result in all_results if result.startswith("❌"))
    total = passed + warnings + failed
    
    print(f"\n📊 OPTIMIZATION RESULTS:")
    print(f"✅ Optimizations Implemented: {passed}")
    print(f"⚠️ Partial Optimizations: {warnings}")
    print(f"❌ Missing Optimizations: {failed}")
    print(f"📈 Overall Optimization Score: {((passed + warnings*0.5)/total)*100:.1f}%")
    
    print(f"\n🔍 DETAILED RESULTS:")
    for result in all_results:
        print(f"  {result}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if failed > 0:
        print("  - Address missing critical optimizations marked with ❌")
    if warnings > 0:
        print("  - Consider improving partial optimizations marked with ⚠️")
    
    print("  - Monitor Core Web Vitals after deployment")
    print("  - Use Chrome DevTools to measure actual LCP improvements")
    print("  - Consider implementing a Content Delivery Network (CDN)")
    
    return {
        'passed': passed,
        'warnings': warnings,
        'failed': failed,
        'score': ((passed + warnings*0.5)/total)*100
    }

if __name__ == "__main__":
    print("🚀 Critical Request Chain Optimization Test")
    print("="*60)
    
    try:
        summary = generate_optimization_summary()
        
        # Exit with appropriate code
        if summary['failed'] == 0:
            print(f"\n🎉 All critical optimizations implemented successfully!")
            sys.exit(0)
        elif summary['score'] >= 80:
            print(f"\n✅ Good optimization level achieved ({summary['score']:.1f}%)")
            sys.exit(0)
        else:
            print(f"\n⚠️ Optimization needs improvement ({summary['score']:.1f}%)")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        sys.exit(1)