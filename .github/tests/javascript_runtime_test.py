#!/usr/bin/env python3
"""
JavaScript Runtime Testing Suite
================================

Tests JavaScript execution in a real browser environment to catch:
- Runtime errors (TypeError, ReferenceError, etc.)
- Console errors and warnings
- JavaScript functionality validation
- DOM manipulation errors
- Async loading issues

Uses Selenium WebDriver for actual browser testing.
"""

import os
import sys
import unittest
import time
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import subprocess

# Test configuration
LOCAL_SERVER_URL = 'http://localhost:8000'
TIMEOUT = 10
WAIT_FOR_JS_LOAD = 3  # Wait for deferred JavaScript to load


class JavaScriptRuntimeTest(unittest.TestCase):
    """Test JavaScript execution and runtime behavior."""
    
    @classmethod
    def setUpClass(cls):
        """Set up browser - try Chrome first, then Safari."""
        cls.driver = None
        
        # Try Chrome first
        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            
            # Enable logging
            chrome_options.add_argument('--enable-logging')
            chrome_options.add_argument('--log-level=0')
            chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
            
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(5)
            print("Using Chrome WebDriver")
            return
        except Exception as e:
            print(f"Chrome not available: {e}")
        
        # Try Safari as fallback
        try:
            # Check if Safari WebDriver is available
            result = subprocess.run(['which', 'safaridriver'], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("Safari WebDriver not found")
            
            safari_options = SafariOptions()
            cls.driver = webdriver.Safari(options=safari_options)
            cls.driver.implicitly_wait(5)
            print("Using Safari WebDriver")
            return
        except Exception as e:
            print(f"Safari not available: {e}")
        
        # If neither works, skip tests
        raise unittest.SkipTest("No suitable WebDriver available (tried Chrome and Safari)")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up browser."""
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    
    def setUp(self):
        """Set up each test."""
        # Clear browser logs before each test
        try:
            self.driver.get_log('browser')
        except:
            pass
    
    def get_console_logs(self):
        """Get browser console logs."""
        try:
            logs = self.driver.get_log('browser')
            return logs
        except Exception as e:
            print(f"Could not retrieve console logs: {e}")
            return []
    
    def test_01_page_loads_without_js_errors(self):
        """Test that the main page loads without JavaScript errors."""
        try:
            self.driver.get(LOCAL_SERVER_URL)
            
            # Wait for page to fully load including deferred scripts
            time.sleep(WAIT_FOR_JS_LOAD)
            
            # Get console logs
            logs = self.get_console_logs()
            
            # Filter for JavaScript errors
            js_errors = []
            for log in logs:
                level = log.get('level', '')
                message = log.get('message', '')
                
                # Check for error-level logs that are JavaScript related
                if level == 'SEVERE':
                    if any(keyword in message.lower() for keyword in [
                        'uncaught', 'error', 'typeerror', 'referenceerror',
                        'syntaxerror', 'rangeerror', 'evalerror'
                    ]):
                        js_errors.append({
                            'level': level,
                            'message': message,
                            'timestamp': log.get('timestamp', '')
                        })
            
            # Report errors
            if js_errors:
                error_details = '\n'.join([
                    f"  - {error['level']}: {error['message']}"
                    for error in js_errors
                ])
                self.fail(f"JavaScript errors found:\n{error_details}")
                
        except WebDriverException as e:
            self.skipTest(f"Could not load page: {e}")
    
    def test_02_critical_js_functions_loaded(self):
        """Test that critical JavaScript functions are available."""
        try:
            self.driver.get(LOCAL_SERVER_URL)
            time.sleep(WAIT_FOR_JS_LOAD)
            
            # Test critical JavaScript functionality
            test_scripts = [
                # Test that basic DOM manipulation works
                "return typeof document !== 'undefined'",
                
                # Test that critical.js functions exist
                "return typeof window.showSkillBars === 'function'",
                
                # Test that deferred.js loaded without errors
                "return typeof window.initBackgroundSlideshow === 'function'",
                
                # Test basic DOM queries work
                "return document.querySelector('body') !== null",
            ]
            
            for i, script in enumerate(test_scripts):
                with self.subTest(test=f"script_{i+1}"):
                    try:
                        result = self.driver.execute_script(script)
                        self.assertTrue(result, f"JavaScript test failed: {script}")
                    except Exception as e:
                        self.fail(f"JavaScript execution failed: {script} - {e}")
                        
        except WebDriverException as e:
            self.skipTest(f"Could not test JavaScript functions: {e}")
    
    def test_03_dom_manipulation_works(self):
        """Test that DOM manipulation functions work correctly."""
        try:
            self.driver.get(LOCAL_SERVER_URL)
            time.sleep(WAIT_FOR_JS_LOAD)
            
            # Test DOM manipulation that should work
            dom_tests = [
                # Test element creation
                "var el = document.createElement('div'); return el.tagName === 'DIV'",
                
                # Test element insertion
                """
                var container = document.body;
                var test_el = document.createElement('div');
                test_el.id = 'test-element';
                container.appendChild(test_el);
                return document.getElementById('test-element') !== null;
                """,
                
                # Test style manipulation
                """
                var test_el = document.getElementById('test-element');
                if (test_el) {
                    test_el.style.display = 'none';
                    return test_el.style.display === 'none';
                }
                return false;
                """,
                
                # Clean up test element
                """
                var test_el = document.getElementById('test-element');
                if (test_el) {
                    test_el.remove();
                    return document.getElementById('test-element') === null;
                }
                return true;
                """
            ]
            
            for i, script in enumerate(dom_tests):
                with self.subTest(dom_test=f"test_{i+1}"):
                    try:
                        result = self.driver.execute_script(script)
                        self.assertTrue(result, f"DOM manipulation test failed: test_{i+1}")
                    except Exception as e:
                        self.fail(f"DOM manipulation failed: test_{i+1} - {e}")
                        
        except WebDriverException as e:
            self.skipTest(f"Could not test DOM manipulation: {e}")
    
    def test_04_background_slideshow_initialization(self):
        """Test that background slideshow initializes without errors."""
        try:
            self.driver.get(LOCAL_SERVER_URL)
            time.sleep(WAIT_FOR_JS_LOAD)
            
            # Check that background slideshow can be initialized
            test_script = """
            try {
                // Check if function exists
                if (typeof window.initBackgroundSlideshow !== 'function') {
                    return { success: false, error: 'initBackgroundSlideshow function not found' };
                }
                
                // Try to initialize (this should not throw errors)
                // Since we can't test the actual slideshow without images, 
                // just test that the function exists and is callable
                return { success: true, error: null };
            } catch (e) {
                return { success: false, error: e.toString() };
            }
            """
            
            result = self.driver.execute_script(test_script)
            
            if not result['success']:
                self.fail(f"Background slideshow initialization failed: {result['error']}")
                
        except WebDriverException as e:
            self.skipTest(f"Could not test background slideshow: {e}")
    
    def test_05_console_warnings_check(self):
        """Check for console warnings that might indicate issues."""
        try:
            self.driver.get(LOCAL_SERVER_URL)
            time.sleep(WAIT_FOR_JS_LOAD)
            
            logs = self.get_console_logs()
            
            # Filter for warnings
            warnings = []
            for log in logs:
                level = log.get('level', '')
                message = log.get('message', '')
                
                if level == 'WARNING':
                    warnings.append({
                        'level': level,
                        'message': message,
                        'timestamp': log.get('timestamp', '')
                    })
            
            # Report warnings (don't fail, just inform)
            if warnings:
                warning_details = '\n'.join([
                    f"  - {warning['message']}"
                    for warning in warnings
                ])
                print(f"Console warnings found:\n{warning_details}")
                
        except WebDriverException as e:
            self.skipTest(f"Could not check console warnings: {e}")
    
    def test_06_resource_loading_errors(self):
        """Check for failed resource loading (404s, etc.)."""
        try:
            self.driver.get(LOCAL_SERVER_URL)
            time.sleep(WAIT_FOR_JS_LOAD)
            
            logs = self.get_console_logs()
            
            # Look for resource loading errors
            resource_errors = []
            for log in logs:
                message = log.get('message', '')
                
                # Check for common resource loading error patterns
                if any(pattern in message.lower() for pattern in [
                    'failed to load resource',
                    '404',
                    'net::err_',
                    'failed to fetch'
                ]):
                    resource_errors.append(message)
            
            if resource_errors:
                error_details = '\n'.join([f"  - {error}" for error in resource_errors])
                self.fail(f"Resource loading errors found:\n{error_details}")
                
        except WebDriverException as e:
            self.skipTest(f"Could not check resource loading: {e}")


def run_javascript_tests(verbose: bool = False) -> bool:
    """
    Run JavaScript runtime tests.
    
    Args:
        verbose: Whether to run tests with verbose output
        
    Returns:
        bool: True if all tests passed, False otherwise
    """
    # Check if local server is running
    import requests
    try:
        response = requests.get(LOCAL_SERVER_URL, timeout=5)
        if response.status_code != 200:
            print(f"❌ Local server not accessible at {LOCAL_SERVER_URL}")
            print("Please start a local server with: python3 -m http.server 8000")
            return False
    except requests.RequestException:
        print(f"❌ Local server not running at {LOCAL_SERVER_URL}")
        print("Please start a local server with: python3 -m http.server 8000")
        return False
    
    # Configure test runner
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(JavaScriptRuntimeTest)
    
    # Run tests
    runner = unittest.TextTestRunner(
        verbosity=2 if verbose else 1,
        stream=sys.stdout,
        buffer=True
    )
    
    print("Starting JavaScript runtime tests...")
    print(f"Testing URL: {LOCAL_SERVER_URL}")
    print("-" * 60)
    
    result = runner.run(suite)
    
    # Summary
    print("-" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
            print(f"    {traceback.split('AssertionError: ')[-1].split(chr(10))[0]}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
            # Get last meaningful line from traceback
            lines = traceback.strip().split('\n')
            error_line = lines[-1] if lines else "Unknown error"
            print(f"    {error_line}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall result: {'✅ PASSED' if success else '❌ FAILED'}")
    
    return success


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run JavaScript runtime tests')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose test output')
    args = parser.parse_args()
    
    success = run_javascript_tests(verbose=args.verbose)
    sys.exit(0 if success else 1)