#!/usr/bin/env python3
"""
Test Runner for Website Security and Functionality Tests
Executes all security and functionality tests in sequence with summary reporting.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_test(test_name, script_path):
    """Run a test script and return the results"""
    print(f"\n{'='*60}")
    print(f"🧪 RUNNING: {test_name}")
    print(f"{'='*60}")
    
    try:
        # Run the test script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, 
                              text=True, 
                              timeout=60)
        
        # Print the output
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return {
            'name': test_name,
            'exit_code': result.returncode,
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
    
    except subprocess.TimeoutExpired:
        print(f"❌ TEST TIMEOUT: {test_name} exceeded 60 seconds")
        return {
            'name': test_name,
            'exit_code': 124,
            'success': False,
            'output': "",
            'error': "Test timed out after 60 seconds"
        }
    except Exception as e:
        print(f"❌ TEST ERROR: {test_name} failed to run: {str(e)}")
        return {
            'name': test_name,
            'exit_code': 1,
            'success': False,
            'output': "",
            'error': str(e)
        }

def main():
    """Run all tests and provide summary"""
    
    print("🚀 WEBSITE SECURITY & FUNCTIONALITY TEST SUITE")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define test suite
    tests = [
        {
            'name': 'Website Functionality Test',
            'script': os.path.join(script_dir, 'website_functionality_test.py'),
            'description': 'Verifies all critical website components are working'
        },
        {
            'name': 'Critical Request Chain Optimization Test',
            'script': os.path.join(script_dir, 'critical_request_chain_optimization_test.py'),
            'description': 'Validates critical request chain optimization for improved LCP performance'
        },
        {
            'name': 'Comprehensive Security Scan',
            'script': os.path.join(script_dir, 'comprehensive_security_scan.py'),
            'description': 'Scans for potentially sensitive files that should be protected'
        },
        {
            'name': 'SEO & Sitemap Optimization Test',
            'script': os.path.join(script_dir, 'seo_optimization_test.py'),
            'description': 'Comprehensive SEO improvements, sitemap synchronization, and optimization validation'
        },
        {
            'name': 'Vulnerability Assessment',
            'script': os.path.join(script_dir, 'vulnerability_assessment.py'),
            'description': 'Advanced security testing beyond basic file protection'
        },
        {
            'name': 'YouTube Performance Test',
            'script': os.path.join(script_dir, 'youtube_performance_test.py'),
            'description': 'Validates YouTube lazy loading for improved mobile performance'
        }
    ]
    
    # Run all tests
    results = []
    for test in tests:
        if os.path.exists(test['script']):
            print(f"📝 {test['description']}")
            result = run_test(test['name'], test['script'])
            results.append(result)
        else:
            print(f"⚠️ SKIPPED: {test['name']} - Script not found: {test['script']}")
            results.append({
                'name': test['name'],
                'exit_code': 127,
                'success': False,
                'output': "",
                'error': f"Script not found: {test['script']}"
            })
    
    # Generate summary
    print("\n" + "=" * 60)
    print("📊 TEST SUITE SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['success'])
    failed_tests = total_tests - passed_tests
    
    print(f"📈 TOTAL TESTS: {total_tests}")
    print(f"✅ PASSED: {passed_tests}")
    print(f"❌ FAILED: {failed_tests}")
    print(f"📊 SUCCESS RATE: {(passed_tests/total_tests*100):.1f}%")
    
    # Show failed tests
    if failed_tests > 0:
        print(f"\n❌ FAILED TESTS ({failed_tests}):")
        for result in results:
            if not result['success']:
                print(f"   • {result['name']} (Exit Code: {result['exit_code']})")
                if result['error']:
                    print(f"     Error: {result['error']}")
    
    # Overall status
    print(f"\n🏆 OVERALL STATUS:")
    if failed_tests == 0:
        print("   ✅ ALL TESTS PASSED - Website is secure and functional")
        exit_code = 0
    elif passed_tests >= total_tests * 0.67:  # At least 2/3 passing
        print("   ⚠️ MOSTLY PASSING - Minor issues detected")
        exit_code = 1
    else:
        print("   ❌ SIGNIFICANT ISSUES - Multiple test failures")
        exit_code = 2
    
    print(f"📅 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)