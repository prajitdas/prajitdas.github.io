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
    if 'display=swap' in content:
        results.append("✅ Font-display swap optimization: Implemented")
    else:
        results.append("❌ Font-display swap optimization: Missing")
    
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
    
    # Check for jQuery core library deduplication (exclude plugins)
    jquery_core_scripts = re.findall(r'<script[^>]*src="[^"]*jquery-[0-9][^"]*"[^>]*>', content)
    if len(jquery_core_scripts) <= 1:  # Allow only one jQuery core version
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
    """Test font loading optimization"""
    print("🔤 Testing Font Optimization...")
    
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    results = []
    
    # Check for consolidated font requests
    font_requests = len(re.findall(r'fonts\.googleapis\.com/css', content))
    if font_requests <= 1:
        results.append(f"✅ Font request consolidation: {font_requests} request (optimized)")
    else:
        results.append(f"⚠️ Font request consolidation: {font_requests} requests")
    
    # Check for font-display: swap
    if 'display=swap' in content:
        results.append("✅ Font-display swap: Implemented")
    else:
        results.append("❌ Font-display swap: Missing")
    
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
    
    # Estimate improvements
    estimated_lcp_improvement = min(30, preconnects * 5 + preloads * 8 + async_scripts * 3)
    estimated_fcp_improvement = min(25, preconnects * 3 + deferred_scripts * 4)
    
    results = [
        f"📈 Estimated LCP improvement: {estimated_lcp_improvement}%",
        f"📈 Estimated FCP improvement: {estimated_fcp_improvement}%",
        f"🔗 Preconnect hints: {preconnects}",
        f"🚀 Resource preloads: {preloads}",
        f"⏱️ Deferred scripts: {deferred_scripts}",
        f"⚡ Async scripts: {async_scripts}"
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