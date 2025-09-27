#!/usr/bin/env python3
"""
Website Validation Test Suite
Comprehensive tests to validate HTML structure, links, assets, and accessibility
"""

import os
import re
import sys
import unittest
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import mimetypes

class WebsiteValidationTests(unittest.TestCase):
    """Test suite for validating website structure and content"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Tests are now in .github/tests, so go up two levels to get to repo root
        cls.base_dir = Path(__file__).parent.parent.parent
        cls.assets_dir = cls.base_dir / "assets"
        cls.base_url = "https://prajitdas.github.io/"
        cls.html_files = list(cls.base_dir.glob("**/*.html"))
        cls.css_files = list(cls.base_dir.glob("**/*.css"))
        cls.js_files = list(cls.base_dir.glob("**/*.js"))
        
    def test_html_files_exist(self):
        """Test that required HTML files exist"""
        required_files = [
            "index.html",
            "sitemap.html",
            "assets/error-pages/404/404.html"
        ]
        
        for file_path in required_files:
            full_path = self.base_dir / file_path
            self.assertTrue(
                full_path.exists(),
                f"Required HTML file missing: {file_path}"
            )
    
    def test_html_structure_validity(self):
        """Test HTML structure and DOCTYPE declarations"""
        for html_file in self.html_files:
            # Skip if it's in a hidden directory or vendor files
            if any(part.startswith('.') for part in html_file.parts):
                continue
                
            with self.subTest(file=str(html_file.relative_to(self.base_dir))):
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for DOCTYPE declaration (case-insensitive)
                self.assertTrue(
                    content.strip().lower().startswith('<!doctype'),
                    f"Missing DOCTYPE in {html_file.name}"
                )
                
                # Parse HTML and check basic structure
                soup = BeautifulSoup(content, 'html.parser')
                
                # Check for required HTML elements
                self.assertIsNotNone(soup.find('html'), f"Missing <html> tag in {html_file.name}")
                self.assertIsNotNone(soup.find('head'), f"Missing <head> tag in {html_file.name}")
                self.assertIsNotNone(soup.find('body'), f"Missing <body> tag in {html_file.name}")
                
                # Check for title tag
                title = soup.find('title')
                if title:
                    self.assertTrue(
                        len(title.get_text().strip()) > 0,
                        f"Empty title tag in {html_file.name}"
                    )
    
    def test_meta_tags_validation(self):
        """Test essential meta tags in main pages"""
        index_file = self.base_dir / "index.html"
        
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for essential meta tags
            charset_meta = soup.find('meta', {'charset': True}) or soup.find('meta', {'http-equiv': 'Content-Type'})
            self.assertIsNotNone(charset_meta, "Missing charset meta tag")
            
            viewport_meta = soup.find('meta', {'name': 'viewport'})
            self.assertIsNotNone(viewport_meta, "Missing viewport meta tag")
            
            # Check for Google site verification
            google_verification = soup.find('meta', {'name': 'google-site-verification'})
            self.assertIsNotNone(google_verification, "Missing Google site verification meta tag")
            
            # Validate Google verification content
            if google_verification:
                content_attr = google_verification.get('content', '')
                self.assertTrue(
                    len(content_attr) > 10,
                    "Google verification content seems invalid"
                )
    
    def test_internal_links_validity(self):
        """Test that internal links point to existing files"""
        for html_file in self.html_files:
            if any(part.startswith('.') for part in html_file.parts):
                continue
                
            with self.subTest(file=str(html_file.relative_to(self.base_dir))):
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # Check all href links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    
                    # Skip external links, mailto, tel, and anchors
                    if (href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')) or
                        href.startswith('//')):
                        continue
                    
                    # Convert relative path to absolute
                    if href.startswith('/'):
                        # Absolute path from root
                        target_path = self.base_dir / href.lstrip('/')
                    else:
                        # Relative path from current file
                        target_path = html_file.parent / href
                    
                    # Remove query parameters and fragments
                    target_path_str = str(target_path).split('?')[0].split('#')[0]
                    target_path = Path(target_path_str)
                    
                    # Normalize path
                    try:
                        target_path = target_path.resolve()
                    except (OSError, ValueError):
                        self.fail(f"Invalid link path: {href} in {html_file.name}")
                    
                    self.assertTrue(
                        target_path.exists(),
                        f"Broken internal link: {href} in {html_file.name} -> {target_path}"
                    )
    
    def test_asset_links_validity(self):
        """Test that asset links (CSS, JS, images) point to existing files"""
        for html_file in self.html_files:
            if any(part.startswith('.') for part in html_file.parts):
                continue
                
            with self.subTest(file=str(html_file.relative_to(self.base_dir))):
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # Check CSS links
                for link in soup.find_all('link', rel='stylesheet'):
                    href = link.get('href', '')
                    if href and not href.startswith(('http://', 'https://', '//')):
                        self._check_asset_exists(href, html_file, 'CSS')
                
                # Check script sources
                for script in soup.find_all('script', src=True):
                    src = script['src']
                    if not src.startswith(('http://', 'https://', '//')):
                        self._check_asset_exists(src, html_file, 'JavaScript')
                
                # Check image sources
                for img in soup.find_all('img', src=True):
                    src = img['src']
                    if not src.startswith(('http://', 'https://', '//', 'data:')):
                        self._check_asset_exists(src, html_file, 'Image')
                
                # Check favicon and icon links
                for link in soup.find_all('link', rel=lambda x: x and 'icon' in x.lower()):
                    href = link.get('href', '')
                    if href and not href.startswith(('http://', 'https://', '//')):
                        self._check_asset_exists(href, html_file, 'Icon')
    
    def _check_asset_exists(self, asset_path, html_file, asset_type):
        """Helper method to check if an asset exists"""
        if asset_path.startswith('/'):
            # Absolute path from root
            target_path = self.base_dir / asset_path.lstrip('/')
        else:
            # Relative path from current file
            target_path = html_file.parent / asset_path
        
        # Remove query parameters
        target_path_str = str(target_path).split('?')[0]
        target_path = Path(target_path_str)
        
        try:
            target_path = target_path.resolve()
        except (OSError, ValueError):
            self.fail(f"Invalid {asset_type} path: {asset_path} in {html_file.name}")
        
        self.assertTrue(
            target_path.exists(),
            f"Missing {asset_type} asset: {asset_path} in {html_file.name} -> {target_path}"
        )
    
    def test_css_files_validity(self):
        """Test that CSS files are valid and not empty"""
        for css_file in self.css_files:
            if any(part.startswith('.') for part in css_file.parts):
                continue
                
            with self.subTest(file=str(css_file.relative_to(self.base_dir))):
                self.assertTrue(css_file.exists(), f"CSS file missing: {css_file}")
                
                # Check file is not empty
                self.assertGreater(
                    css_file.stat().st_size, 0,
                    f"CSS file is empty: {css_file.name}"
                )
                
                # Basic CSS syntax check
                with open(css_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check for balanced braces (basic syntax check)
                open_braces = content.count('{')
                close_braces = content.count('}')
                self.assertEqual(
                    open_braces, close_braces,
                    f"Unbalanced braces in CSS file: {css_file.name}"
                )
    
    def test_javascript_files_validity(self):
        """Test that JavaScript files exist and are not empty"""
        for js_file in self.js_files:
            if any(part.startswith('.') for part in js_file.parts):
                continue
            
            # Skip minified files and vendor files for syntax checking
            if '.min.' in js_file.name or 'vendor' in str(js_file).lower():
                continue
                
            with self.subTest(file=str(js_file.relative_to(self.base_dir))):
                self.assertTrue(js_file.exists(), f"JavaScript file missing: {js_file}")
                
                # Check file is not empty
                if js_file.stat().st_size > 0:
                    with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Basic syntax checks
                    open_parens = content.count('(')
                    close_parens = content.count(')')
                    open_braces = content.count('{')
                    close_braces = content.count('}')
                    
                    # Allow some tolerance for string literals containing these characters
                    paren_diff = abs(open_parens - close_parens)
                    brace_diff = abs(open_braces - close_braces)
                    
                    self.assertLess(
                        paren_diff, 5,
                        f"Potentially unbalanced parentheses in JS file: {js_file.name}"
                    )
                    self.assertLess(
                        brace_diff, 5,
                        f"Potentially unbalanced braces in JS file: {js_file.name}"
                    )
    
    def test_image_assets_exist(self):
        """Test that referenced image assets exist"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp'}
        
        for html_file in self.html_files:
            if any(part.startswith('.') for part in html_file.parts):
                continue
                
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find image references in HTML
            img_pattern = r'(?:src|href)=["\']([^"\']+\.(?:jpg|jpeg|png|gif|svg|ico|webp))["\']'
            matches = re.findall(img_pattern, content, re.IGNORECASE)
            
            for img_path in matches:
                # Skip external URLs and data URIs
                if img_path.startswith(('http://', 'https://', '//', 'data:')):
                    continue
                
                with self.subTest(image=img_path, file=html_file.name):
                    if img_path.startswith('/'):
                        target_path = self.base_dir / img_path.lstrip('/')
                    else:
                        target_path = html_file.parent / img_path
                    
                    try:
                        target_path = target_path.resolve()
                        self.assertTrue(
                            target_path.exists(),
                            f"Missing image: {img_path} referenced in {html_file.name}"
                        )
                    except (OSError, ValueError):
                        self.fail(f"Invalid image path: {img_path} in {html_file.name}")
    
    def test_no_deprecated_html_elements(self):
        """Test for deprecated HTML elements (excluding auto-generated files)"""
        deprecated_elements = ['font', 'center', 'big', 'tt', 'strike']  # Removed 'small' and 'u' as they're valid in HTML5
        
        for html_file in self.html_files:
            if any(part.startswith('.') for part in html_file.parts):
                continue
            
            # Skip auto-generated files (bibtex2html output)
            if 'publication' in html_file.name.lower() or 'bibtex' in html_file.name.lower():
                continue
                
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            for element in deprecated_elements:
                deprecated_tags = soup.find_all(element)
                self.assertEqual(
                    len(deprecated_tags), 0,
                    f"Found deprecated <{element}> tag in {html_file.name}"
                )
    
    def test_responsive_design_meta_tags(self):
        """Test for responsive design meta tags"""
        index_file = self.base_dir / "index.html"
        
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for viewport meta tag with proper responsive settings
            viewport_meta = soup.find('meta', {'name': 'viewport'})
            if viewport_meta:
                viewport_content = viewport_meta.get('content', '')
                self.assertIn(
                    'width=device-width',
                    viewport_content,
                    "Viewport meta tag should include width=device-width for responsive design"
                )
    
    def test_security_headers(self):
        """Test for security-related meta tags"""
        for html_file in self.html_files:
            if any(part.startswith('.') for part in html_file.parts):
                continue
                
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for X-UA-Compatible for IE edge mode
            if 'X-UA-Compatible' in content:
                self.assertIn(
                    'IE=edge',
                    content,
                    f"X-UA-Compatible should use IE=edge in {html_file.name}"
                )
    
    def test_publication_files_generated(self):
        """Test that publication HTML files are properly generated"""
        pub_dir = self.base_dir / "assets" / "docs"
        if pub_dir.exists():
            # Look for publication HTML files
            pub_files = list(pub_dir.glob("**/*publications*.html"))
            
            for pub_file in pub_files:
                with self.subTest(file=str(pub_file.relative_to(self.base_dir))):
                    self.assertTrue(pub_file.exists())
                    
                    with open(pub_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check that it contains bibliography content
                    self.assertTrue(
                        len(content) > 100,
                        f"Publication file seems too short: {pub_file.name}"
                    )
                    
                    # Check for bibtex2html signature
                    soup = BeautifulSoup(content, 'html.parser')
                    self.assertIsNotNone(
                        soup.find('html'),
                        f"Invalid HTML structure in publication file: {pub_file.name}"
                    )


if __name__ == '__main__':
    # Set up test discovery and run tests
    unittest.main(verbosity=2)