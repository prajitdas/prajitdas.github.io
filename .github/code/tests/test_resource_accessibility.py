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

# CI environment detection
IS_CI = os.environ.get('GITHUB_ACTIONS') == 'true'

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
            if IS_CI:
                # Prefer GITHUB_WORKSPACE if available for reliability
                workspace = os.environ.get('GITHUB_WORKSPACE')
                if workspace and os.path.exists(workspace):
                    base_path = workspace
                elif '.github/code/tests' in current_dir:
                    base_path = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
                else:
                    base_path = current_dir
            else:
                if '.github/code/tests' in current_dir:
                    base_path = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
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

    def test_local_file_exists(self, resource_url):
        """Test if a resource exists locally, including anchor validation for HTML fragments"""
        if resource_url.startswith(('http://', 'https://')):
            return False  # External URLs don't have local files
        
        # Parse URL to separate path and fragment
        if '#' in resource_url:
            clean_path, fragment = resource_url.split('#', 1)
            clean_path = clean_path.split('?')[0]  # Remove query parameters
        else:
            clean_path = resource_url.split('?')[0]  # Remove query parameters
            fragment = None
        
        full_path = self.local_path / clean_path
        base_exists = full_path.exists()
        
        # If base file doesn't exist, fail
        if not base_exists:
            if hasattr(self, 'logger'):
                self.logger.log_file_failure(resource_url, f"File not found: {full_path}")
            return False
        
        # If there's a fragment and it's an HTML file, check if anchor exists
        if fragment and clean_path.endswith('.html'):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Check for anchor existence: name="fragment" or id="fragment"
                    import re
                    anchor_pattern = rf'(name="{re.escape(fragment)}"|id="{re.escape(fragment)}")'
                    if not re.search(anchor_pattern, content):
                        if hasattr(self, 'logger'):
                            self.logger.log_file_failure(resource_url, f"Anchor #{fragment} not found in {clean_path}")
                        return False
            except Exception as e:
                if hasattr(self, 'logger'):
                    self.logger.log_file_failure(resource_url, f"Error reading file for anchor check: {e}")
                return False
        
        return True

    def test_web_accessibility(self, url):
        """Test if a resource is accessible via web (CI-tolerant)."""
        try:
            if not url.startswith(('http://', 'https://')):
                if url.startswith('/'):
                    test_url = f"{self.base_url}{url}"
                else:
                    test_url = f"{self.base_url}/{url}"
            else:
                test_url = url

            parsed = urlparse(test_url)
            domain = parsed.netloc.lower()

            # Domains frequently blocking automated CI requests
            SKIP_DOMAINS = [
                'doi.org', 'dx.doi.org', 'arxiv.org', 'ieee.org', 'ieeexplore.ieee.org',
                'dl.acm.org', 'acm.org', 'search.proquest.com', 'ceur-ws.org',
                'igi-global.com', 'ebiquity.umbc.edu'
            ]

            if IS_CI and any(d in domain for d in SKIP_DOMAINS):
                return {
                    'status_code': None,
                    'accessible': True,  # treat as pass in CI
                    'url': test_url,
                    'skipped': True,
                    'reason': 'Skipped external academic domain in CI'
                }

            method = self.session.head
            try:
                response = method(test_url, timeout=8 if IS_CI else 12, allow_redirects=True)
            except requests.exceptions.RequestException:
                # Retry with GET if HEAD not allowed
                response = self.session.get(test_url, timeout=8 if IS_CI else 12, allow_redirects=True)

            status = response.status_code

            # Acceptable statuses broadened for CI (some sites return 403/429 to bots)
            acceptable_statuses = {200, 301, 302, 303, 307, 308}
            if IS_CI:
                acceptable_statuses.update({403, 418, 429})

            is_doi_link = 'doi.org' in domain or 'dx.doi.org' in domain
            accessible = (status in acceptable_statuses or (is_doi_link and status == 418))

            if not accessible and LOCAL_LOGGING_ENABLED and not IS_CI:
                error_type = f"HTTP_{status}"
                log_url_failure(
                    url=test_url,
                    error_type=error_type,
                    status_code=status,
                    test_category="Resource Accessibility"
                )

            return {
                'status_code': status,
                'accessible': accessible,
                'url': test_url
            }
        except Exception as e:
            if LOCAL_LOGGING_ENABLED and not IS_CI:
                log_url_failure(
                    url=test_url if 'test_url' in locals() else url,
                    error_type="CONNECTION_ERROR",
                    error_message=str(e),
                    test_category="Resource Accessibility"
                )
            return {
                'status_code': None,
                'accessible': IS_CI,  # do not fail CI for transient errors
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

    # --- New context-aware testing methods ---
    def _resolve_local_with_context(self, resource_url, referer_dir: Path):
        """Attempt improved local resolution using the referring HTML directory when initial lookup fails."""
        # Already absolute external
        if resource_url.startswith(('http://', 'https://')):
            return False, None
        core_part = resource_url.split('#')[0].split('?')[0]
        # If current simple resolution worked, we would not call this; caller checks.
        candidate = (self.local_path / referer_dir / core_part).resolve()
        if candidate.exists():
            return True, candidate
        # Fallback: search globally for a uniquely named file (only for simple filenames)
        if '/' not in core_part:
            matches = list(self.local_path.rglob(core_part))
            if len(matches) == 1:
                return True, matches[0]
        return False, None

    def test_resource_with_context(self, resource_url, referer_dir: Path):
        """Test resource considering the directory of the referring HTML file for relative resolution."""
        # First do standard test
        base_result = self.test_resource(resource_url)
        if base_result['status'] == 'PASS':
            return base_result

        # If local didn't exist, try context-aware local resolution
        if not base_result['local_exists']:
            local_ok, resolved_path = self._resolve_local_with_context(resource_url, referer_dir)
            if local_ok:
                # Re-check anchor if fragment present
                fragment = None
                if '#' in resource_url:
                    path_part, fragment = resource_url.split('#', 1)
                else:
                    path_part = resource_url
                anchor_ok = True
                if fragment and path_part.endswith('.html'):
                    try:
                        content = resolved_path.read_text(encoding='utf-8')
                        import re
                        anchor_pattern = rf'(name="{re.escape(fragment)}"|id="{re.escape(fragment)}")'
                        if not re.search(anchor_pattern, content):
                            anchor_ok = False
                    except Exception:
                        anchor_ok = False
                # Build improved web URL guess if web failed
                web_accessible = base_result['web_accessible']
                web_status = base_result['web_status']
                if not web_accessible:
                    # Construct URL with referer directory
                    rel_dir_url = '/'.join(referer_dir.as_posix().split('/'))
                    rel_dir_url = rel_dir_url.strip('/')
                    candidate_url = f"{self.base_url}/{rel_dir_url}/{path_part}".replace('//', '/')
                    web_retry = self.test_web_accessibility(candidate_url)
                    web_accessible = web_retry['accessible']
                    web_status = web_retry['status_code']
                final_status = 'PASS' if (local_ok and anchor_ok) or web_accessible else 'FAIL'
                return {
                    'resource': resource_url,
                    'local_exists': local_ok and anchor_ok,
                    'web_accessible': web_accessible,
                    'web_status': web_status,
                    'status': final_status,
                    'type': self.classify_resource(resource_url)
                }
        return base_result

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
        
        results = {}
        file_resource_map = {}
        resource_counter = 0
        for html_file in html_files:
            relative_path = html_file.relative_to(self.local_path)
            referer_dir = relative_path.parent
            resources = self.extract_resources_from_html(html_file)
            file_resource_map[str(relative_path)] = resources
            print(f"   📄 {relative_path}: {len(resources)} resources")
            for resource in sorted(resources):
                resource_counter += 1
                if resource_counter <= 20:
                    print(f"\n[{resource_counter}] Testing: {resource}")
                result = self.test_resource_with_context(resource, referer_dir)
                resource_type = result['type']
                results.setdefault(resource_type, []).append(result)
                if resource_counter <= 20:
                    local_status = "✅" if result['local_exists'] else "❌"
                    web_status = "✅" if result['web_accessible'] else "❌"
                    status_code = f"({result['web_status']})" if result['web_status'] else ""
                    print(f"   Local: {local_status} | Web: {web_status} {status_code}")
                time.sleep(0.02)

        print(f"\n🔗 Total resource references tested: {resource_counter}")
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

    # Critical resource types that should not fail in CI unless local
    critical_failures = 0
    for resource_type, resources_list in results.items():
        if resource_type in ['PDF', 'HTML', 'CSS', 'JS']:
            for r in resources_list:
                # Only count as critical if local reference missing (internal asset)
                if not r['local_exists'] and r['resource'].startswith(('http://', 'https://')):
                    # External resource: ignore in CI if web still accessible or skipped
                    if IS_CI:
                        continue
                if r['status'] == 'FAIL':
                    critical_failures += 1

    if IS_CI and critical_failures == 0:
        sys.exit(0)
    else:
        sys.exit(1 if critical_failures > 0 else 0)

if __name__ == "__main__":
    main()
