#!/usr/bin/env python3
"""
Security scan script to check for credential leakage and sensitive information
"""

import re
import sys
from pathlib import Path

def scan_for_credentials(base_dir):
    """Scan repository for potential security issues"""
    
    # Security patterns to check for
    patterns = {
        'api_keys': r'(api[_-]?key\s*[:=]\s*["\'][^"\']+["\'])',
        'aws_keys': r'(AKIA[0-9A-Z]{16}|aws_access_key_id\s*[:=])',
        'github_tokens': r'(gh[pousr]_[A-Za-z0-9]{36}|github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59})',
        'passwords': r'(password\s*[:=]\s*["\'][^"\']+["\'])',
        'private_keys': r'-----BEGIN.*(PRIVATE|RSA).*KEY-----',
        'connection_strings': r'(mysql://[^\\s]+@|postgres://[^\\s]+@|mongodb://[^\\s]+@)',
        'hardcoded_secrets': r'(secret\s*[:=]\s*["\'][^"\']+["\'])',
    }
    
    # Files to skip (known safe files)
    skip_patterns = [
        'keybase.txt',
        'github-activity',
        'Developer-ReadMe.txt',
        'bower.json',
        'font',  # Font files often have false positives
        '.svg',  # SVG files have coordinate data that can trigger false positives
    ]
    
    issues = []
    scanned_files = 0
    
    # Check specific file types
    for file_path in base_dir.rglob('*'):
        if not file_path.is_file():
            continue
            
        # Skip hidden directories and git files
        if any(part.startswith('.git') for part in file_path.parts):
            continue
            
        # Skip known safe files and our own security scan
        if any(skip in str(file_path) for skip in skip_patterns) or 'security_scan.py' in str(file_path):
            continue
            
        # Only scan text-based files
        if file_path.suffix not in ['.txt', '.html', '.js', '.json', '.yml', '.yaml', '.md', '.py', '.sh', '.css']:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                scanned_files += 1
                
            for pattern_name, pattern in patterns.items():
                matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                if matches:
                    # Filter out false positives
                    real_matches = []
                    for match in matches:
                        match_text = match if isinstance(match, str) else match[0]
                        
                        # Skip template variables and examples
                        if any(template in match_text.lower() for template in [
                            'example', 'your_', 'placeholder', 'template', 'xxx', 'yyy', 'zzz',
                            'client_id', 'client_secret'  # These are just parameter names
                        ]):
                            continue
                            
                        real_matches.append(match_text[:50] + '...' if len(match_text) > 50 else match_text)
                    
                    if real_matches:
                        issues.append({
                            'file': file_path.relative_to(base_dir),
                            'type': pattern_name,
                            'matches': real_matches[:3]  # Limit to first 3 matches
                        })
        except Exception as e:
            continue  # Skip files that can't be read
    
    return issues, scanned_files

def main():
    """Main security scan function"""
    base_dir = Path(__file__).parent.parent
    
    print("🔍 Scanning repository for security issues...")
    print("=" * 50)
    
    issues, scanned_files = scan_for_credentials(base_dir)
    
    print(f"Files scanned: {scanned_files}")
    print(f"Security issues found: {len(issues)}")
    print()
    
    if issues:
        print("❌ SECURITY ISSUES DETECTED:")
        for issue in issues:
            print(f"  📁 File: {issue['file']}")
            print(f"     🚨 Type: {issue['type']}")
            print(f"     🔍 Matches: {issue['matches']}")
            print()
        return 1
    else:
        print("✅ No security issues detected!")
        print("   - No hardcoded API keys found")
        print("   - No exposed passwords found") 
        print("   - No private keys found")
        print("   - No connection strings found")
        return 0

if __name__ == "__main__":
    sys.exit(main())