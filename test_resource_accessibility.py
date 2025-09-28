#!/usr/bin/env python3
"""
Comprehensive Website Resource Accessibility Test
Tests all local HTML, PDF, image, text, and other files referenced in the website
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import time

class WebsiteResourceTester:
    def __init__(self, base_url="https://prajitdas.github.io", local_path="."):
        self.base_url = base_url.rstrip('/')
        self.local_path = Path(local_path).resolve()
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Website Resource Tester)'
        })
        
    def extract_local_resources_from_file(self, file_path):
        """Extract all local resource references from an HTML file"""
        resources = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract different types of resources
            resource_patterns = [
                # Images
                ('img', 'src'),
                ('img', 'srcset'),
                # Links
                ('a', 'href'),
                ('link', 'href'),
                # Scripts
                ('script', 'src'),
                # Objects and embeds
                ('object', 'data'),
                ('embed', 'src'),
                # Sources in video/audio
                ('source', 'src'),
                # CSS background images (basic extraction)
            ]
            
            for tag_name, attr in resource_patterns:
                for tag in soup.find_all(tag_name):
                    if tag.get(attr):
                        url = tag[attr]
                        if self.is_local_resource(url):
                            if attr == 'srcset':
                                # Handle srcset which can have multiple URLs
                                urls = self.parse_srcset(url)
                                resources.update(urls)
                            else:
                                resources.add(url)
            
            # Extract CSS background images and other URL() references
            css_urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', content)
            for url in css_urls:
                if self.is_local_resource(url):
                    resources.add(url)
                    
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
        return resources
    
    def parse_srcset(self, srcset):
        """Parse srcset attribute to extract URLs"""
        urls = []
        # srcset format: "url1 1x, url2 2x" or "url1 100w, url2 200w"
        parts = srcset.split(',')
        for part in parts:
            part = part.strip()
            # Extract URL (everything before the first space)
            url = part.split()[0] if part.split() else part
            if url and self.is_local_resource(url):
                urls.append(url)
        return urls
    
    def is_local_resource(self, url):
        """Check if URL is a local resource (not external)"""
        if not url:
            return False
            
        # Remove fragments
        url = url.split('#')[0]
        
        # Skip empty URLs
        if not url:
            return False
            
        parsed = urlparse(url)
        
        # External URLs
        if parsed.scheme in ('http', 'https') and parsed.netloc:
            # Only check if it's our domain
            return parsed.netloc == 'prajitdas.github.io'
        
        # Skip mailto, tel, javascript, data URLs
        if parsed.scheme in ('mailto', 'tel', 'javascript', 'data'):
            return False
            
        # Local relative URLs
        return True
    
    def normalize_url(self, url):
        """Normalize URL for testing"""
        # Remove leading ./ 
        if url.startswith('./'):
            url = url[2:]
        
        # Handle prajitdas.github.io URLs
        if url.startswith('https://prajitdas.github.io/'):
            url = url.replace('https://prajitdas.github.io/', '')
        
        return url
    
    def test_local_file_exists(self, url):
        """Test if local file exists on filesystem"""
        normalized = self.normalize_url(url)
        local_file = self.local_path / normalized
        
        return {
            'url': url,
            'normalized': normalized,
            'local_path': str(local_file),
            'exists': local_file.exists(),
            'is_file': local_file.is_file() if local_file.exists() else False,
            'size': local_file.stat().st_size if local_file.exists() and local_file.is_file() else 0
        }
    
    def test_web_accessibility(self, url):
        """Test if resource is accessible via web"""
        normalized = self.normalize_url(url)
        web_url = f"{self.base_url}/{normalized}"
        
        try:
            response = self.session.head(web_url, timeout=10, allow_redirects=True)
            return {
                'url': web_url,
                'status_code': response.status_code,
                'accessible': response.status_code == 200,
                'content_type': response.headers.get('content-type', ''),
                'content_length': response.headers.get('content-length', '0')
            }
        except Exception as e:
            return {
                'url': web_url,
                'status_code': None,
                'accessible': False,
                'error': str(e),
                'content_type': '',
                'content_length': '0'
            }
    
    def find_html_files(self):
        """Find all HTML files in the project"""
        html_files = []
        
        # Main HTML files
        for pattern in ['*.html', '**/*.html']:
            html_files.extend(self.local_path.glob(pattern))
        
        return html_files
    
    def run_comprehensive_test(self):
        """Run comprehensive resource accessibility test"""
        print(f"🔍 Starting comprehensive resource accessibility test...")
        print(f"📁 Base path: {self.local_path}")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 80)
        
        # Find all HTML files
        html_files = self.find_html_files()
        print(f"📄 Found {len(html_files)} HTML files to analyze")
        
        # Extract all resources
        all_resources = set()
        file_resource_map = {}
        
        for html_file in html_files:
            resources = self.extract_local_resources_from_file(html_file)
            all_resources.update(resources)
            file_resource_map[html_file] = resources
            print(f"   📄 {html_file.name}: {len(resources)} resources")
        
        print(f"\\n🔗 Total unique local resources found: {len(all_resources)}")
        
        # Test each resource
        results = {
            'html': [],
            'pdf': [],
            'images': [],
            'text': [],
            'css': [],
            'js': [],
            'other': []
        }
        
        for i, resource in enumerate(sorted(all_resources), 1):
            print(f"\\n[{i}/{len(all_resources)}] Testing: {resource}")
            
            # Test local file existence
            local_test = self.test_local_file_exists(resource)
            
            # Test web accessibility
            web_test = self.test_web_accessibility(resource)
            
            # Determine file type
            file_type = self.get_file_type(resource)
            
            result = {
                'resource': resource,
                'type': file_type,
                'local': local_test,
                'web': web_test,
                'status': 'PASS' if local_test['exists'] and web_test['accessible'] else 'FAIL'
            }
            
            results[file_type].append(result)
            
            # Print result
            local_status = "✅" if local_test['exists'] else "❌"
            web_status = "✅" if web_test['accessible'] else "❌"
            print(f"   Local: {local_status} | Web: {web_status} ({web_test.get('status_code', 'ERROR')})")
            
            # Small delay to be respectful
            time.sleep(0.1)
        
        # Generate summary report
        self.generate_report(results, file_resource_map)
        
        return results
    
    def get_file_type(self, url):
        """Determine file type based on extension"""
        ext = Path(url).suffix.lower()
        
        if ext in ['.html', '.htm']:
            return 'html'
        elif ext in ['.pdf']:
            return 'pdf'
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp']:
            return 'images'
        elif ext in ['.txt', '.md']:
            return 'text'
        elif ext in ['.css']:
            return 'css'
        elif ext in ['.js']:
            return 'js'
        else:
            return 'other'
    
    def generate_report(self, results, file_resource_map):
        """Generate comprehensive test report"""
        print("\\n" + "=" * 80)
        print("📊 COMPREHENSIVE RESOURCE ACCESSIBILITY REPORT")
        print("=" * 80)
        
        total_resources = sum(len(resources) for resources in results.values())
        total_passed = sum(len([r for r in resources if r['status'] == 'PASS']) 
                          for resources in results.values())
        total_failed = total_resources - total_passed
        
        print(f"\\n📈 SUMMARY STATISTICS:")
        print(f"   Total Resources: {total_resources}")
        print(f"   ✅ Passed: {total_passed}")
        print(f"   ❌ Failed: {total_failed}")
        print(f"   📊 Success Rate: {(total_passed/total_resources*100):.1f}%")
        
        # Detailed breakdown by type
        print(f"\\n📋 BREAKDOWN BY FILE TYPE:")
        for file_type, resources in results.items():
            if resources:
                passed = len([r for r in resources if r['status'] == 'PASS'])
                total = len(resources)
                print(f"   {file_type.upper()}: {passed}/{total} passed ({passed/total*100:.1f}%)")
        
        # Failed resources details
        print(f"\\n❌ FAILED RESOURCES:")
        for file_type, resources in results.items():
            failed = [r for r in resources if r['status'] == 'FAIL']
            if failed:
                print(f"\\n   {file_type.upper()} files:")
                for resource in failed:
                    local_issue = "not found locally" if not resource['local']['exists'] else ""
                    web_issue = f"web error ({resource['web'].get('status_code', 'ERROR')})" if not resource['web']['accessible'] else ""
                    issues = [i for i in [local_issue, web_issue] if i]
                    print(f"     • {resource['resource']} - {', '.join(issues)}")
        
        # Key files check
        print(f"\\n🔑 KEY FILE ACCESSIBILITY:")
        key_files = [
            'keybase.txt',
            'robots.txt',
            'sitemap.xml',
            'assets/docs/resume/resume-prajit-das-032225.pdf',
            'assets/img/Profile.jpg',
            'index.html'
        ]
        
        for key_file in key_files:
            local_exists = (self.local_path / key_file).exists()
            web_test = self.test_web_accessibility(key_file)
            local_status = "✅" if local_exists else "❌"
            web_status = "✅" if web_test['accessible'] else "❌"
            print(f"   {key_file}: Local {local_status} | Web {web_status}")
        
        print("\\n" + "=" * 80)

def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "."
    
    tester = WebsiteResourceTester(local_path=base_path)
    results = tester.run_comprehensive_test()
    
    # Exit with error code if any tests failed
    total_failed = sum(len([r for r in resources if r['status'] == 'FAIL']) 
                      for resources in results.values())
    sys.exit(1 if total_failed > 0 else 0)

if __name__ == "__main__":
    main()