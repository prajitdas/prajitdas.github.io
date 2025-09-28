#!/usr/bin/env python3
"""
Comprehensive Website Resource Accessibility Test
Tests all local HTML, PDF, image, text, and other files referenced in the website
"""

import os
import sys
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import time

# Import local logging system (only for local runs, not GitHub Actions)
try:
    if not os.environ.get('GITHUB_ACTIONS'):
        from local_test_logger import log_url_failure, log_file_failure, log_validation_failure
        LOCAL_LOGGING_ENABLED = True
    else:
        LOCAL_LOGGING_ENABLED = False
except ImportError:
    LOCAL_LOGGING_ENABLED = False

class WebsiteResourceTester:
    def __init__(self, base_path=None, base_url="https://prajitdas.github.io"):
        # Auto-detect if running from tests directory
        if base_path is None:
            current_dir = os.getcwd()
            if '.github/tests' in current_dir:
                base_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
            else:
                base_path = current_dir
        
        self.base_path = base_path
        self.base_url = base_url.rstrip('/')
        self.local_path = Path(base_path).resolve()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def find_html_files(self):
        """Find all HTML files in the base directory"""
        html_files = []
        for file_path in self.local_path.rglob("*.html"):
            relative_path = file_path.relative_to(self.local_path)
            if any(part.startswith('.') for part in relative_path.parts):
                continue
            html_files.append(file_path)
        return html_files

    def extract_resources_from_html(self, html_file):
        """Extract all resource references from an HTML file"""
        resources = set()
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract different types of resources
            resource_selectors = [
                ('link[href]', 'href'),
                ('script[src]', 'src'),
                ('img[src]', 'src'),
                ('a[href]', 'href'),
            ]
            
            for selector, attr in resource_selectors:
                elements = soup.select(selector)
                for element in elements:
                    resource_url = element.get(attr)
                    if resource_url:
                        resource_url = resource_url.strip()
                        if resource_url and not resource_url.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                            resources.add(resource_url)
            
            return resources
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
            return set()

    def classify_resource(self, resource_url):
        """Classify the resource type based on URL and extension"""
        path = urlparse(resource_url).path.lower()
        
        if path.endswith('.pdf'):
            return 'PDF'
        elif path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico')):
            return 'IMAGES'
        elif path.endswith('.css'):
            return 'CSS'
        elif path.endswith('.js'):
            return 'JS'
        elif path.endswith(('.html', '.htm')):
            return 'HTML'
        elif path.endswith(('.txt', '.xml', '.json')):
            return 'TEXT'
        else:
            return 'OTHER'

    def test_local_file_exists(self, file_path):
        """Test if a local file exists"""
        if file_path.startswith(('http://', 'https://')):
            return False  # External URLs don't have local files
        
        # Remove query parameters and anchors
        clean_path = file_path.lstrip('/')
        clean_path = clean_path.split('?')[0].split('#')[0]
        full_path = self.local_path / clean_path
        file_exists = full_path.exists() and full_path.is_file()
        
        # Log local file failure
        if not file_exists and LOCAL_LOGGING_ENABLED:
            log_file_failure(
                file_path=str(full_path),
                error_type="FILE_NOT_FOUND",
                error_message=f"Local file does not exist: {file_path}",
                test_category="Resource Accessibility"
            )
        
        return file_exists

    def test_web_accessibility(self, url):
        """Test if a resource is accessible via web"""
        try:
            if not url.startswith(('http://', 'https://')):
                if url.startswith('/'):
                    test_url = f"{self.base_url}{url}"
                else:
                    test_url = f"{self.base_url}/{url}"
            else:
                test_url = url
            
            response = self.session.head(test_url, timeout=10, allow_redirects=True)
            
            # Log URL failure if status code is not 200
            if response.status_code != 200 and LOCAL_LOGGING_ENABLED:
                error_type = f"HTTP_{response.status_code}"
                log_url_failure(
                    url=test_url,
                    error_type=error_type,
                    status_code=response.status_code,
                    test_category="Resource Accessibility"
                )
            
            return {
                'status_code': response.status_code,
                'accessible': response.status_code == 200,
                'url': test_url
            }
        except Exception as e:
            # Log URL failure for exceptions
            if LOCAL_LOGGING_ENABLED:
                log_url_failure(
                    url=test_url if 'test_url' in locals() else url,
                    error_type="CONNECTION_ERROR",
                    error_message=str(e),
                    test_category="Resource Accessibility"
                )
            
            return {
                'status_code': None,
                'accessible': False,
                'error': str(e),
                'url': test_url if 'test_url' in locals() else url
            }

    def test_resource(self, resource_url):
        """Test both local and web accessibility of a resource"""
        local_exists = self.test_local_file_exists(resource_url)
        web_result = self.test_web_accessibility(resource_url)
        
        return {
            'resource': resource_url,
            'local_exists': local_exists,
            'web_accessible': web_result['accessible'],
            'web_status': web_result['status_code'],
            'status': 'PASS' if (local_exists or web_result['accessible']) else 'FAIL',
            'type': self.classify_resource(resource_url)
        }

    def test_key_files(self):
        """Test accessibility of key website files"""
        key_files = [
            'keybase.txt',
            'robots.txt', 
            'sitemap.xml',
            'assets/docs/resume/resume-prajit-das-032225.pdf',
            'assets/img/Profile.jpg',
            'index.html'
        ]
        
        print(f"\n🔑 KEY FILE ACCESSIBILITY:")
        for file_path in key_files:
            local_result = "✅" if self.test_local_file_exists(file_path) else "❌"
            web_result = self.test_web_accessibility(file_path)
            web_status = "✅" if web_result['accessible'] else "❌"
            print(f"   {file_path}: Local {local_result} | Web {web_status}")

    def run_comprehensive_test(self):
        """Run comprehensive resource accessibility test"""
        print(f"🔍 Starting comprehensive resource accessibility test...")
        print(f"📁 Base path: {self.base_path}")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 80)
        
        html_files = self.find_html_files()
        print(f"📄 Found {len(html_files)} HTML files to analyze")
        
        all_resources = set()
        file_resource_map = {}
        
        for html_file in html_files:
            relative_path = html_file.relative_to(self.local_path)
            resources = self.extract_resources_from_html(html_file)
            file_resource_map[str(relative_path)] = resources
            all_resources.update(resources)
            print(f"   📄 {relative_path}: {len(resources)} resources")
        
        print(f"\n🔗 Total unique local resources found: {len(all_resources)}")
        
        results = {}
        for i, resource in enumerate(sorted(all_resources), 1):
            if i <= 20:  # Limit output for quick testing
                print(f"\n[{i}/{len(all_resources)}] Testing: {resource}")
            result = self.test_resource(resource)
            
            resource_type = result['type']
            if resource_type not in results:
                results[resource_type] = []
            results[resource_type].append(result)
            
            if i <= 20:  # Limit output for quick testing
                local_status = "✅" if result['local_exists'] else "❌"
                web_status = "✅" if result['web_accessible'] else "❌"
                status_code = f"({result['web_status']})" if result['web_status'] else ""
                print(f"   Local: {local_status} | Web: {web_status} {status_code}")
            
            time.sleep(0.05)  # Shorter delay
        
        self.generate_report(results, file_resource_map)
        return results

    def generate_report(self, results, file_resource_map):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE RESOURCE ACCESSIBILITY REPORT")
        print("=" * 80)
        
        total_resources = sum(len(resources) for resources in results.values())
        total_passed = sum(len([r for r in resources if r['status'] == 'PASS']) 
                          for resources in results.values())
        total_failed = total_resources - total_passed
        
        print(f"\n📈 SUMMARY STATISTICS:")
        print(f"   Total Resources: {total_resources}")
        print(f"   ✅ Passed: {total_passed}")
        print(f"   ❌ Failed: {total_failed}")
        if total_resources > 0:
            print(f"   📊 Success Rate: {(total_passed/total_resources*100):.1f}%")
        else:
            print(f"   📊 Success Rate: N/A (no resources found)")
        
        print(f"\n📋 BREAKDOWN BY FILE TYPE:")
        for resource_type, resources in sorted(results.items()):
            passed = len([r for r in resources if r['status'] == 'PASS'])
            total = len(resources)
            percentage = (passed/total*100) if total > 0 else 0
            print(f"   {resource_type}: {passed}/{total} passed ({percentage:.1f}%)")
        
        # Only show first few failed resources to avoid spam
        print(f"\n❌ FAILED RESOURCES (first 10):")
        failed_count = 0
        for resource_type, resources in sorted(results.items()):
            failed_resources = [r for r in resources if r['status'] == 'FAIL']
            if failed_resources and failed_count < 10:
                print(f"\n   {resource_type} files:")
                for resource in failed_resources[:5]:  # Limit to 5 per type
                    if failed_count >= 10:
                        break
                    failed_count += 1
                    reasons = []
                    if not resource['local_exists']:
                        reasons.append("not found locally")
                    if not resource['web_accessible']:
                        status = f"({resource['web_status']})" if resource['web_status'] else ""
                        reasons.append(f"web error {status}")
                    reason_text = ", ".join(reasons)
                    print(f"     • {resource['resource']} - {reason_text}")
        
        self.test_key_files()
        print("\n" + "=" * 80)

def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = None
    
    tester = WebsiteResourceTester(base_path=base_path)
    results = tester.run_comprehensive_test()
    
    total_failed = sum(len([r for r in resources if r['status'] == 'FAIL']) 
                      for resources in results.values())
    
    # Only fail if critical resources fail
    critical_failures = 0
    for resource_type, resources in results.items():
        if resource_type in ['PDF', 'HTML', 'CSS', 'JS']:
            critical_failures += len([r for r in resources if r['status'] == 'FAIL'])
    
    sys.exit(1 if critical_failures > 0 else 0)

if __name__ == "__main__":
    main()
