#!/usr/bin/env python3
"""
Critical Request Chain Optimization Test
Validates that critical request chains have been optimized for improved LCP performance.
"""

import requests
import time
import re
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def analyze_critical_request_chain():
    """Analyze the critical request chain optimization"""
    
    print("🔗 CRITICAL REQUEST CHAIN OPTIMIZATION ANALYSIS")
    print("="*60)
    
    base_url = "https://prajitdas.github.io/"
    
    try:
        # Fetch the main page
        start_time = time.time()
        response = requests.get(base_url, timeout=15)
        load_time = time.time() - start_time
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch website: {response.status_code}")
            return
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print(f"📊 Page Load Time: {load_time:.2f}s")
        print(f"📏 HTML Size: {len(html_content)/1024:.1f}KB")
        
        # Analysis results
        results = {
            'inline_css_size': 0,
            'external_css_count': 0,
            'render_blocking_css': 0,
            'render_blocking_js': 0,
            'async_js_count': 0,
            'preload_count': 0,
            'font_optimization': False,
            'critical_path_optimized': False
        }
        
        print(f"\n🎯 CRITICAL PATH ANALYSIS:")
        
        # 1. Check for inline CSS (critical path optimization)
        inline_styles = soup.find_all('style')
        if inline_styles:
            inline_css_content = ''.join([style.string or '' for style in inline_styles])
            results['inline_css_size'] = len(inline_css_content)
            print(f"✅ Inline Critical CSS: {len(inline_css_content)/1024:.1f}KB inlined")
        else:
            print(f"❌ No inline CSS found - missing critical path optimization")
        
        # 2. Analyze CSS loading strategy
        css_links = soup.find_all('link', rel='stylesheet')
        preload_css = soup.find_all('link', rel='preload', attrs={'as': 'style'})
        
        # Filter out CSS links that are inside noscript tags (not render-blocking)
        noscript_sections = soup.find_all('noscript')
        noscript_css = []
        for noscript in noscript_sections:
            noscript_css.extend(noscript.find_all('link', rel='stylesheet'))
        
        # Only count CSS outside of noscript as potentially render-blocking
        render_blocking_css = [link for link in css_links 
                              if link not in noscript_css and 
                              (not link.get('media') or link.get('media') == 'all')]
        
        results['external_css_count'] = len(css_links)
        results['render_blocking_css'] = len(render_blocking_css)
        results['preload_count'] = len(preload_css)
        
        print(f"📄 External CSS Files: {len(css_links)}")
        print(f"🚫 Render-blocking CSS: {results['render_blocking_css']}")
        print(f"⚡ CSS Preloads: {len(preload_css)}")
        
        # 3. Analyze JavaScript loading
        script_tags = soup.find_all('script', src=True)
        
        # Filter out scripts inside noscript tags
        noscript_scripts = []
        for noscript in noscript_sections:
            noscript_scripts.extend(noscript.find_all('script', src=True))
        
        actual_scripts = [s for s in script_tags if s not in noscript_scripts]
        async_scripts = [s for s in actual_scripts if s.get('async') or s.get('defer')]
        blocking_scripts = [s for s in actual_scripts if not (s.get('async') or s.get('defer'))]
        
        results['async_js_count'] = len(async_scripts)
        results['render_blocking_js'] = len(blocking_scripts)
        
        print(f"📜 External JavaScript Files: {len(script_tags)}")
        print(f"🚫 Render-blocking JS: {len(blocking_scripts)}")
        print(f"⚡ Async/Defer JS: {len(async_scripts)}")
        
        # 4. Check for dynamic CSS loading
        dynamic_css_loading = ('loadCSS' in html_content or 
                              'createElement' in html_content and 
                              'stylesheet' in html_content)
        if dynamic_css_loading:
            print(f"✅ Dynamic CSS Loading: Implemented")
            results['critical_path_optimized'] = True
        else:
            print(f"❌ Dynamic CSS Loading: Not detected")
        
        # 5. Font loading optimization
        font_display_optional = 'display=optional' in html_content
        font_fallbacks = '@font-face' in html_content
        results['font_optimization'] = font_display_optional and font_fallbacks
        
        if results['font_optimization']:
            print(f"✅ Font Optimization: display=optional + fallbacks")
        else:
            print(f"❌ Font Optimization: Incomplete")
        
        # 6. Check for resource hints
        dns_prefetch = soup.find_all('link', rel='dns-prefetch')
        preconnect = soup.find_all('link', rel='preconnect')
        preload = soup.find_all('link', rel='preload')
        
        print(f"\n🔮 RESOURCE HINTS:")
        print(f"🌐 DNS Prefetch: {len(dns_prefetch)} domains")
        print(f"🔗 Preconnect: {len(preconnect)} origins")
        print(f"⚡ Preload: {len(preload)} resources")
        
        # 7. Analyze critical request chain depth
        print(f"\n📊 CRITICAL REQUEST CHAIN ANALYSIS:")
        
        chain_depth = 1  # HTML is always depth 1
        
        # Check if CSS is inline (depth 1) or external (depth 2+)
        if results['inline_css_size'] > 0:
            print(f"✅ CSS Chain Depth: 1 (inlined)")
        else:
            chain_depth = max(chain_depth, 2)
            print(f"⚠️ CSS Chain Depth: 2+ (external)")
        
        # Check JavaScript loading strategy
        if results['render_blocking_js'] == 0:
            print(f"✅ JS Chain Depth: Non-blocking")
        else:
            chain_depth = max(chain_depth, 2)
            print(f"⚠️ JS Chain Depth: 2+ (render-blocking)")
        
        # Font loading impact
        if results['font_optimization']:
            print(f"✅ Font Chain Impact: Minimized (optional + fallbacks)")
        else:
            print(f"⚠️ Font Chain Impact: Potential blocking")
        
        print(f"\n🎯 OPTIMIZATION SCORE:")
        
        # Calculate optimization score
        score_factors = {
            'inline_css': 25 if results['inline_css_size'] > 1000 else 0,
            'non_blocking_css': 20 if results['render_blocking_css'] <= 1 else 0,
            'non_blocking_js': 20 if results['render_blocking_js'] == 0 else 0,
            'font_optimization': 15 if results['font_optimization'] else 0,
            'dynamic_loading': 10 if results['critical_path_optimized'] else 0,
            'resource_hints': 10 if len(preload) >= 2 else 5 if len(preload) >= 1 else 0
        }
        
        total_score = sum(score_factors.values())
        max_score = 100
        
        print(f"📈 Critical Path Score: {total_score}/{max_score} ({total_score/max_score*100:.1f}%)")
        
        for factor, score in score_factors.items():
            status = "✅" if score > 0 else "❌"
            print(f"   {status} {factor.replace('_', ' ').title()}: {score} points")
        
        # 8. Performance recommendations
        print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
        
        if results['inline_css_size'] == 0:
            print(f"   📄 Inline critical CSS to eliminate render-blocking requests")
        
        if results['render_blocking_css'] > 1:
            print(f"   🔄 Use async CSS loading for non-critical stylesheets")
        
        if results['render_blocking_js'] > 0:
            print(f"   ⚡ Load JavaScript asynchronously to prevent render blocking")
        
        if not results['font_optimization']:
            print(f"   🔤 Optimize font loading with display=optional and fallbacks")
        
        if len(preload) < 2:
            print(f"   🚀 Add resource preloading for LCP candidates")
        
        # 9. Expected performance impact
        print(f"\n📊 EXPECTED PERFORMANCE IMPACT:")
        
        if total_score >= 80:
            print(f"   🎉 EXCELLENT: Significant LCP improvement expected (20-40%)")
            print(f"   🚀 Critical request chain optimally configured")
        elif total_score >= 60:
            print(f"   ✅ GOOD: Moderate LCP improvement expected (10-25%)")
            print(f"   🔧 Some optimizations still possible")
        else:
            print(f"   ⚠️ NEEDS WORK: Limited improvement without further optimization")
            print(f"   🛠️ Critical request chain needs significant optimization")
        
        # 10. Technical details
        print(f"\n🔧 TECHNICAL DETAILS:")
        print(f"   📦 HTML Payload: {len(html_content)/1024:.1f}KB")
        print(f"   🎨 Inline CSS: {results['inline_css_size']/1024:.1f}KB")
        print(f"   📄 External CSS: {results['external_css_count']} files")
        print(f"   📜 External JS: {len(script_tags)} files")
        print(f"   ⚡ Resource Hints: {len(dns_prefetch) + len(preconnect) + len(preload)} total")
        
        return {
            'score': total_score,
            'max_score': max_score,
            'optimizations': len([s for s in score_factors.values() if s > 0]),
            'total_optimizations': len(score_factors)
        }
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        return None

def test_lcp_optimization():
    """Test specific LCP optimization factors"""
    
    print(f"\n🎯 LCP OPTIMIZATION TEST:")
    print("="*40)
    
    base_url = "https://prajitdas.github.io/"
    
    try:
        response = requests.get(base_url, timeout=10)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        lcp_factors = []
        
        # 1. Check for image preloading (LCP candidate)
        img_preloads = soup.find_all('link', rel='preload', attrs={'as': 'image'})
        if img_preloads:
            lcp_factors.append("✅ Image preloading for LCP candidate")
        else:
            lcp_factors.append("⚠️ No image preloading detected")
        
        # 2. Check for critical CSS inlining
        inline_styles = soup.find_all('style')
        if inline_styles and len(''.join([s.string or '' for s in inline_styles])) > 1000:
            lcp_factors.append("✅ Substantial critical CSS inlined")
        else:
            lcp_factors.append("❌ Insufficient critical CSS inlining")
        
        # 3. Check for non-blocking JavaScript
        script_tags = soup.find_all('script', src=True)
        blocking_scripts = [s for s in script_tags if not (s.get('async') or s.get('defer'))]
        if len(blocking_scripts) == 0:
            lcp_factors.append("✅ No render-blocking JavaScript")
        else:
            lcp_factors.append(f"❌ {len(blocking_scripts)} render-blocking scripts")
        
        # 4. Check for font optimization
        if 'display=optional' in html_content and '@font-face' in html_content:
            lcp_factors.append("✅ Font loading optimized")
        else:
            lcp_factors.append("❌ Font loading not optimized")
        
        for factor in lcp_factors:
            print(f"   {factor}")
        
        passed = sum(1 for f in lcp_factors if f.startswith("✅"))
        total = len(lcp_factors)
        
        print(f"\n📊 LCP Optimization Score: {passed}/{total} ({passed/total*100:.1f}%)")
        
        return passed, total
        
    except Exception as e:
        print(f"❌ LCP test failed: {str(e)}")
        return 0, 0

if __name__ == "__main__":
    print("🚀 Critical Request Chain Optimization Analysis")
    print("="*60)
    print("Testing: https://prajitdas.github.io/")
    print("="*60)
    
    # Run comprehensive analysis
    analysis_result = analyze_critical_request_chain()
    
    # Run LCP-specific tests
    lcp_passed, lcp_total = test_lcp_optimization()
    
    # Final summary
    if analysis_result:
        print(f"\n🏆 FINAL SUMMARY:")
        print(f"📊 Critical Path Score: {analysis_result['score']}/{analysis_result['max_score']} ({analysis_result['score']/analysis_result['max_score']*100:.1f}%)")
        print(f"🎯 LCP Optimization: {lcp_passed}/{lcp_total} ({lcp_passed/lcp_total*100:.1f}%)")
        print(f"✅ Optimizations Applied: {analysis_result['optimizations']}/{analysis_result['total_optimizations']}")
        
        if analysis_result['score'] >= 80 and lcp_passed >= 3:
            print(f"\n🎉 EXCELLENT: Critical request chain highly optimized!")
            print(f"🚀 Expected LCP improvement: 20-40%")
        elif analysis_result['score'] >= 60:
            print(f"\n✅ GOOD: Solid critical path optimization")
            print(f"📈 Expected LCP improvement: 10-25%")
        else:
            print(f"\n⚠️ NEEDS IMPROVEMENT: More optimization needed")
            print(f"🔧 Focus on inlining critical CSS and eliminating render-blocking resources")