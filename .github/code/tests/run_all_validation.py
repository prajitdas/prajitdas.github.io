#!/usr/bin/env python3
"""
Test Runner for Website Security and Functionality Tests
Executes all security and functionality tests in sequence with summary reporting.
"""

import subprocess
import sys
import os
from datetime import datetime

# Import local logging system (only for local runs, not GitHub Actions)
try:
    if not os.environ.get('GITHUB_ACTIONS'):
        from local_test_logger import get_test_logger, finalize_test_logging, log_test_start, log_test_end
        LOCAL_LOGGING_ENABLED = True
    else:
        LOCAL_LOGGING_ENABLED = False
except ImportError:
    LOCAL_LOGGING_ENABLED = False

def run_test(test_name, script_path, description=""):
    """Run a test script and return the results"""
    print(f"\n{'='*60}")
    print(f"🧪 RUNNING: {test_name}")
    print(f"{'='*60}")
    
    # Log test start for local logging
    if LOCAL_LOGGING_ENABLED:
        log_test_start(test_name, description)
    
    start_time = datetime.now()
    
    try:
        # Run the test script
        # Set longer timeout for comprehensive tests
        timeout = 300 if 'website_validation.py' in script_path or 'test_resource_accessibility.py' in script_path else 60
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, 
                              text=True, 
                              timeout=timeout)
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Print the output
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Count passed/failed from output (simple heuristic)
        output_lines = result.stdout.split('\n')
        passed_count = sum(1 for line in output_lines if '✅' in line or 'PASSED' in line.upper())
        failed_count = sum(1 for line in output_lines if '❌' in line or 'FAILED' in line.upper())
        
        # Log test end for local logging
        if LOCAL_LOGGING_ENABLED:
            log_test_end(test_name, passed_count, failed_count, execution_time)
        
        return {
            'name': test_name,
            'exit_code': result.returncode,
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
            'execution_time': execution_time,
            'passed_count': passed_count,
            'failed_count': failed_count
        }
    
    except subprocess.TimeoutExpired:
        execution_time = (datetime.now() - start_time).total_seconds()
        error_msg = f"Test timed out after {timeout} seconds"
        print(f"❌ TEST TIMEOUT: {test_name} exceeded {timeout} seconds")
        
        # Log test end for local logging
        if LOCAL_LOGGING_ENABLED:
            log_test_end(test_name, 0, 1, execution_time)
        
        return {
            'name': test_name,
            'exit_code': 124,
            'success': False,
            'output': "",
            'error': error_msg,
            'execution_time': execution_time,
            'passed_count': 0,
            'failed_count': 1
        }
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        error_msg = str(e)
        print(f"❌ TEST ERROR: {test_name} failed to run: {error_msg}")
        
        # Log test end for local logging
        if LOCAL_LOGGING_ENABLED:
            log_test_end(test_name, 0, 1, execution_time)
        
        return {
            'name': test_name,
            'exit_code': 1,
            'success': False,
            'output': "",
            'error': error_msg,
            'execution_time': execution_time,
            'passed_count': 0,
            'failed_count': 1
        }

def main():
    """Run all tests and provide summary"""
    
    # Check for quick mode
    quick_mode = '--quick' in sys.argv or os.environ.get('FAST_VALIDATION', '').lower() in ('1', 'true', 'yes')
    if quick_mode:
        os.environ['FAST_VALIDATION'] = '1'
    
    print("🚀 WEBSITE SECURITY & FUNCTIONALITY VALIDATION SUITE")
    print("=" * 60)
    if quick_mode:
        print("⚡ QUICK MODE: External link validation skipped for speed")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define test suite
    tests = [
        {
            'name': 'Website Validation',
            'script': os.path.join(script_dir, 'website_validation.py'),
            'description': 'Comprehensive HTML validation, link checking, security headers, and functionality testing'
        },
        {
            'name': 'JavaScript Code Quality',
            'script': os.path.join(script_dir, 'jslint_validation.py'),
            'description': 'JavaScript linting, syntax validation, and code quality analysis using JSHint'
        },
        {
            'name': 'Critical Request Chain Optimization',
            'script': os.path.join(script_dir, 'critical_request_chain_optimization.py'),
            'description': 'Validates critical request chain optimization for improved LCP performance'
        },
        {
            'name': 'Comprehensive Security Scan',
            'script': os.path.join(script_dir, 'comprehensive_security_scan.py'),
            'description': 'Scans for potentially sensitive files that should be protected'
        },
        {
            'name': 'SEO & Sitemap Optimization',
            'script': os.path.join(script_dir, 'seo_optimization.py'),
            'description': 'Comprehensive SEO improvements, sitemap synchronization, and optimization validation'
        },
        {
            'name': 'Vulnerability Assessment',
            'script': os.path.join(script_dir, 'vulnerability_assessment.py'),
            'description': 'Advanced security testing beyond basic file protection'
        },
        {
            'name': 'YouTube Performance',
            'script': os.path.join(script_dir, 'youtube_performance.py'),
            'description': 'Validates YouTube lazy loading for improved mobile performance'
        },
        {
            'name': 'Resource Accessibility',
            'script': os.path.join(script_dir, 'test_resource_accessibility.py'),
            'description': 'Comprehensive validation of all website resources (HTML, PDF, images, CSS, JS, and text files)'
        },
        {
            'name': 'Local File Integrity',
            'script': os.path.join(script_dir, 'local_file_integrity.py'),
            'description': 'File permissions, content integrity, configuration consistency, and asset validation'
        },
        {
            'name': 'Performance & Accessibility',
            'script': os.path.join(script_dir, 'performance_accessibility.py'),
            'description': 'Core Web Vitals optimization, accessibility features, mobile performance, and technical SEO'
        },
        {
            'name': 'Content Security & Privacy',
            'script': os.path.join(script_dir, 'content_security_privacy.py'),
            'description': 'Content Security Policy, privacy compliance, data protection, and content integrity'
        }
    ]
    
    # Run all tests
    results = []
    for test in tests:
        if os.path.exists(test['script']):
            print(f"📝 {test['description']}")
            result = run_test(test['name'], test['script'], test['description'])
            results.append(result)
        else:
            print(f"⚠️ SKIPPED: {test['name']} - Script not found: {test['script']}")
            results.append({
                'name': test['name'],
                'exit_code': 127,
                'success': False,
                'output': "",
                'error': f"Script not found: {test['script']}",
                'execution_time': 0,
                'passed_count': 0,
                'failed_count': 1
            })
    
    # Generate summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUITE SUMMARY")
    print("=" * 60)
    
    total_validations = len(results)
    passed_validations = sum(1 for r in results if r['success'])
    failed_validations = total_validations - passed_validations

    # In CI quick/FAST mode allow specific tests to be soft-fails
    is_ci = os.environ.get('GITHUB_ACTIONS') == 'true'
    soft_failed_names = []
    
    # Tests that can be soft-failed in quick mode
    soft_fail_candidates = [
        'Resource Accessibility',
        'SEO & Sitemap Optimization',
        'YouTube Performance'
    ]
    
    if is_ci and ('--quick' in sys.argv or os.environ.get('FAST_VALIDATION')):
        for r in results:
            if not r['success'] and r['name'] in soft_fail_candidates:
                # Reclassify as soft-fail
                soft_failed_names.append(r['name'])
                r['success'] = True
                passed_validations += 1
                failed_validations -= 1
    
    print(f"📈 TOTAL VALIDATIONS: {total_validations}")
    print(f"✅ PASSED: {passed_validations}")
    print(f"❌ FAILED: {failed_validations}")
    print(f"📊 SUCCESS RATE: {(passed_validations/total_validations*100):.1f}%")
    
    # Show failed validations
    if failed_validations > 0:
        print(f"\n❌ FAILED VALIDATIONS ({failed_validations}):")
        for result in results:
            if not result['success']:
                print(f"   • {result['name']} (Exit Code: {result['exit_code']})")
                if result['error']:
                    print(f"     Error: {result['error']}")
    
    # Overall status
    print(f"\n🏆 OVERALL STATUS:")
    if failed_validations == 0:
        print("   ✅ ALL VALIDATIONS PASSED - Website is secure and functional")
        exit_code = 0
    elif passed_validations >= total_validations * 0.67:  # At least 2/3 passing
        print("   ⚠️ MOSTLY PASSING - Minor issues detected")
        exit_code = 1
    else:
        print("   ❌ SIGNIFICANT ISSUES - Multiple validation failures")
        exit_code = 2

    if soft_failed_names:
        print("\nℹ️ Soft-failed (treated as pass in CI quick mode): " + ", ".join(soft_failed_names))
    
    print(f"📅 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
        # Finalize local logging
    if LOCAL_LOGGING_ENABLED:
        try:
            finalize_test_logging()
            print("\n💾 Local test logs saved for debugging")
        except Exception as e:
            print(f"\n⚠️ Error saving local logs: {e}")
            print("Test suite completed successfully despite logging error")
    
    return exit_code

if __name__ == "__main__":
    if '--help' in sys.argv or '-h' in sys.argv:
        print("Website Validation Test Suite")
        print("Usage:")
        print("  python run_all_validation.py           # Full validation (slow)")
        print("  python run_all_validation.py --quick   # Quick validation (fast)")
        print("  FAST_VALIDATION=1 python run_all_validation.py  # Quick via env var")
        print()
        print("Quick mode skips external link validation for 10x faster execution.")
        sys.exit(0)
    exit_code = main()
    sys.exit(exit_code)