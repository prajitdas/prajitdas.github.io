#!/usr/bin/env python3
"""
Consolidated Website Validation Test Suite
==========================================

This module combines comprehensive static analysis and functional testing
for the personal website. Includes HTML validation, link checking, security
headers, asset validation, and accessibility testing.

Replaces both test_website_validation.py and website_functionality_test.py
to eliminate redundancy while maintaining comprehensive coverage.
"""

import os
import sys
import unittest
import requests
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict, Set, Optional, Tuple

# Import local logging system (only for local runs, not GitHub Actions)
try:
    if not os.environ.get('GITHUB_ACTIONS'):
        from local_test_logger import log_url_failure, log_validation_failure, log_security_issue
        LOCAL_LOGGING_ENABLED = True
    else:
        LOCAL_LOGGING_ENABLED = False
except ImportError:
    LOCAL_LOGGING_ENABLED = False

# Website configuration
BASE_URL = 'https://prajitdas.github.io'
LOCAL_PATH = Path(__file__).parent.parent.parent.parent  # Root of repository
TIMEOUT = 30  # Increased from 10 to 30 seconds for stability
MAX_RETRIES = 3  # Increased from 2 to 3 retries for stability
RETRY_DELAY = 2  # Increased from 1 to 2 seconds for stability
MAX_EXTERNAL_LINKS = 20  # Limit external link testing for performance

# Fast mode for development (skip external link validation)
FAST_MODE = os.environ.get('FAST_VALIDATION', '').lower() in ('1', 'true', 'yes')

class WebsiteValidationTest(unittest.TestCase):
    """Comprehensive website validation test suite."""
    
    # New pages to validate
    PAGES_TO_TEST = [
        'index.html',
        'experience.html',
        'projects.html',
        'service.html',
        'publications.html',
        '404.html'
    ]

    @classmethod
    def setUpClass(cls):
        """Set up test environment and validate base URL accessibility."""
        cls.session = requests.Session()
        cls.session.headers.update({
            'User-Agent': 'Website-Validator/1.0 (Test Suite)'
        })
        
        # Test base URL accessibility
        try:
            response = cls.session.get(BASE_URL, timeout=TIMEOUT)
            if response.status_code != 200:
                print(f"Warning: Base URL returned status {response.status_code}")
        except requests.RequestException as e:
            print(f"Warning: Could not reach base URL: {e}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up session."""
        cls.session.close()
    
    def test_01_html_file_existence(self):
        """Test that required HTML files exist locally."""
        for filename in self.PAGES_TO_TEST:
            file_path = LOCAL_PATH / filename
            self.assertTrue(
                file_path.exists(),
                f"Required HTML file '{filename}' not found at {file_path}"
            )
    
    def test_02_html_basic_structure(self):
        """Test basic HTML structure of main pages."""
        for filename in self.PAGES_TO_TEST:
            with self.subTest(file=filename):
                file_path = LOCAL_PATH / filename
                if not file_path.exists():
                    self.skipTest(f"File {filename} not found")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Check basic structure
                self.assertIsNotNone(soup.find('html'), f"No <html> tag in {filename}")
                self.assertIsNotNone(soup.find('head'), f"No <head> tag in {filename}")
                self.assertIsNotNone(soup.find('body'), f"No <body> tag in {filename}")
                self.assertIsNotNone(soup.find('title'), f"No <title> tag in {filename}")
    
    def test_03_meta_tags_validation(self):
        """Test presence of important meta tags."""
        index_path = LOCAL_PATH / 'index.html'
        if not index_path.exists():
            self.skipTest("index.html not found")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check for viewport meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        self.assertIsNotNone(viewport, "Viewport meta tag missing")
        
        # Check for charset declaration
        charset = soup.find('meta', attrs={'charset': True}) or soup.find('meta', attrs={'http-equiv': re.compile(r'content-type', re.I)})
        self.assertIsNotNone(charset, "Character encoding meta tag missing")
        
        # Check for description
        description = soup.find('meta', attrs={'name': 'description'})
        self.assertIsNotNone(description, "Description meta tag missing")
    
    def test_04_external_link_validation(self):
        """Test external links for accessibility (with retries)."""
        if FAST_MODE:
            self.skipTest("Skipping external link validation in fast mode")
            
        # Collect links from all pages
        external_links = set()
        
        for filename in self.PAGES_TO_TEST:
            file_path = LOCAL_PATH / filename
            if not file_path.exists():
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith(('http://', 'https://')) and not href.startswith(BASE_URL):
                    external_links.add(href)
        
        # Limit external link testing for performance - sample key links only
        external_links = sorted(list(external_links))[:MAX_EXTERNAL_LINKS]
        print(f"Testing {len(external_links)} external links (limited for performance)...")
        failed_links = []
        
        for url in external_links:
            with self.subTest(url=url):
                success = False
                last_error = None
                
                for attempt in range(MAX_RETRIES):
                    try:
                        response = self.session.head(url, timeout=TIMEOUT, allow_redirects=True)
                        if response.status_code < 400:
                            success = True
                            break
                        else:
                            last_error = f"HTTP {response.status_code}"
                        
                    except requests.RequestException as e:
                        last_error = str(e)
                        if attempt < MAX_RETRIES - 1:
                            time.sleep(RETRY_DELAY)
                
                if not success:
                    failed_links.append((url, last_error))
                    print(f"Failed link: {url} - {last_error}")
        
        if failed_links:
            failure_msg = f"Failed to access {len(failed_links)} external links:\n"
            for url, error in failed_links[:5]:  # Show first 5 failures
                failure_msg += f"  - {url}: {error}\n"
            if len(failed_links) > 5:
                failure_msg += f"  ... and {len(failed_links) - 5} more"
            
            # Don't fail the test for external link issues, just warn
            print(f"Warning: {failure_msg}")
    
    def test_05_internal_link_validation(self):
        """Test internal links and anchors."""
        index_path = LOCAL_PATH / 'index.html'
        if not index_path.exists():
            self.skipTest("index.html not found")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check internal links
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Skip external links and anchors
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
                continue
            
            with self.subTest(href=href):
                # Check if file exists locally
                link_path = LOCAL_PATH / href.lstrip('/')
                if not link_path.exists():
                    # Try as directory with index.html
                    index_path = link_path / 'index.html'
                    self.assertTrue(
                        index_path.exists(),
                        f"Internal link target not found: {href}"
                    )
    
    def test_06_image_assets_validation(self):
        """Test that referenced images exist and are accessible."""
        index_path = LOCAL_PATH / 'index.html'
        if not index_path.exists():
            self.skipTest("index.html not found")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        missing_images = []
        
        for img in soup.find_all('img', src=True):
            src = img['src']
            
            # Skip external images and data URLs
            if src.startswith(('http://', 'https://', 'data:')):
                continue
            
            # Remove query parameters for file checking
            clean_src = src.split('?')[0]
            
            # Check local image
            img_path = LOCAL_PATH / clean_src.lstrip('/')
            if not img_path.exists():
                missing_images.append(src)
        
        self.assertEqual(
            len(missing_images), 0,
            f"Missing image files: {missing_images}"
        )
    
    def test_07_css_assets_validation(self):
        """Test that CSS files exist and are accessible."""
        index_path = LOCAL_PATH / 'index.html'
        if not index_path.exists():
            self.skipTest("index.html not found")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        missing_css = []
        
        for link in soup.find_all('link', rel='stylesheet', href=True):
            href = link['href']
            
            # Skip external CSS
            if href.startswith(('http://', 'https://')):
                continue
            
            # Remove query parameters for file checking
            clean_href = href.split('?')[0]
            
            # Check local CSS file
            css_path = LOCAL_PATH / clean_href.lstrip('/')
            if not css_path.exists():
                missing_css.append(href)
        
        self.assertEqual(
            len(missing_css), 0,
            f"Missing CSS files: {missing_css}"
        )
    
    def test_08_javascript_assets_validation(self):
        """Test that JavaScript files exist."""
        index_path = LOCAL_PATH / 'index.html'
        if not index_path.exists():
            self.skipTest("index.html not found")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        missing_js = []
        
        for script in soup.find_all('script', src=True):
            src = script['src']
            
            # Skip external JavaScript
            if src.startswith(('http://', 'https://')):
                continue
            
            # Remove query parameters for file checking
            clean_src = src.split('?')[0]
            
            # Check local JavaScript file
            js_path = LOCAL_PATH / clean_src.lstrip('/')
            if not js_path.exists():
                missing_js.append(src)
        
        self.assertEqual(
            len(missing_js), 0,
            f"Missing JavaScript files: {missing_js}"
        )
    
    def test_09_live_website_accessibility(self):
        """Test live website accessibility and response for all pages."""
        print(f"Testing live accessibility for {len(self.PAGES_TO_TEST)} pages...")
        
        # Check base connectivity first
        try:
            self.session.get(BASE_URL, timeout=TIMEOUT)
        except requests.RequestException as e:
            self.skipTest(f"Could not access live website base URL: {e}")

        for page in self.PAGES_TO_TEST:
            url = urljoin(BASE_URL, page)
            
            with self.subTest(page=page):
                try:
                    response = self.session.get(url, timeout=TIMEOUT)
                    self.assertEqual(
                        response.status_code, 200,
                        f"Page '{page}' not accessible at {url}: HTTP {response.status_code}"
                    )
                    
                    # Check content type
                    content_type = response.headers.get('content-type', '')
                    self.assertIn(
                        'text/html', content_type.lower(),
                        f"Unexpected content type for {page}: {content_type}"
                    )
                    
                    # Check for basic content
                    self.assertGreater(
                        len(response.text), 500,
                        f"Response content for {page} seems too short ({len(response.text)} bytes)"
                    )
                    
                except requests.RequestException as e:
                    self.fail(f"Could not access live page {page}: {e}")
    
    def test_10_security_headers_check(self):
        """Test security headers on live website."""
        try:
            response = self.session.get(BASE_URL, timeout=TIMEOUT)
            headers = response.headers
            
            # Check for security headers (adjusted for GitHub Pages)
            security_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': ['DENY', 'SAMEORIGIN'],  # Accept either
            }
            
            warnings = []
            for header, expected in security_headers.items():
                actual = headers.get(header)
                if isinstance(expected, list):
                    if actual not in expected:
                        warnings.append(f"Security header '{header}' missing or unexpected value: {actual}")
                else:
                    if actual != expected:
                        warnings.append(f"Security header '{header}' missing or unexpected value: {actual}")
            
            # Don't fail test for GitHub Pages limitations, just warn
            if warnings:
                print(f"Security header warnings (GitHub Pages limitations): {warnings}")
                
        except requests.RequestException as e:
            self.skipTest(f"Could not access live website for security check: {e}")
    
    def test_11_responsive_design_elements(self):
        """Test responsive design elements in HTML."""
        index_path = LOCAL_PATH / 'index.html'
        if not index_path.exists():
            self.skipTest("index.html not found")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check for Bootstrap or responsive framework
        responsive_indicators = [
            soup.find('link', href=re.compile(r'bootstrap', re.I)),
            soup.find('meta', attrs={'name': 'viewport'}),
            soup.find(class_=re.compile(r'container|row|col', re.I))
        ]
        
        responsive_found = any(indicator for indicator in responsive_indicators)
        self.assertTrue(
            responsive_found,
            "No responsive design indicators found (Bootstrap, viewport meta, or responsive classes)"
        )
    
    def test_12_performance_indicators(self):
        """Test basic performance optimization indicators."""
        index_path = LOCAL_PATH / 'index.html'
        if not index_path.exists():
            self.skipTest("index.html not found")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check file size (basic performance indicator)
        file_size = len(content)
        self.assertLess(
            file_size, 500000,  # 500KB
            f"HTML file is quite large ({file_size} bytes), consider optimization"
        )
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check for minified resources or performance optimizations
        perf_indicators = [
            soup.find('link', href=re.compile(r'\.min\.css')),
            soup.find('script', src=re.compile(r'\.min\.js')),
            soup.find('style'),  # Inline CSS for critical path
        ]
        
        optimized_found = any(indicator for indicator in perf_indicators)
        if not optimized_found:
            print("Info: No obvious performance optimizations detected")


def run_validation_tests(verbose: bool = False) -> bool:
    """
    Run the complete validation test suite.
    
    Args:
        verbose: Whether to run tests with verbose output
        
    Returns:
        bool: True if all tests passed, False otherwise
    """
    # Configure test runner
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(WebsiteValidationTest)
    
    # Run tests
    runner = unittest.TextTestRunner(
        verbosity=2 if verbose else 1,
        stream=sys.stdout,
        buffer=True
    )
    
    print("Starting comprehensive website validation...")
    print(f"Base URL: {BASE_URL}")
    print(f"Local path: {LOCAL_PATH}")
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
            newline = '\n'
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split(newline)[0]}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            newline = '\n'
            print(f"  - {test}: {traceback.split(newline)[-2]}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall result: {'✅ PASSED' if success else '❌ FAILED'}")
    
    return success


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run website validation tests')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose test output')
    args = parser.parse_args()
    
    success = run_validation_tests(verbose=args.verbose)
    sys.exit(0 if success else 1)