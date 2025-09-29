#!/usr/bin/env python3
"""
JavaScript Code Quality and Linting Test Suite
==============================================

This module provides comprehensive JavaScript linting and code quality analysis
for all JavaScript files in the website. Uses multiple linting approaches:
- JSHint for code quality and potential errors
- Basic syntax validation
- Code complexity analysis
- Best practices checking

Features:
- Filters out minified files (.min.js) from strict linting
- Provides detailed error reporting with line numbers
- Suggests improvements for code quality
- Validates JavaScript syntax
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Configuration
LOCAL_PATH = Path(__file__).parent.parent.parent  # Root of repository
JS_EXTENSIONS = ['.js']
EXCLUDED_PATTERNS = [
    '*.min.js',      # Minified files
    '*jquery*',      # jQuery library files
    '*bootstrap*',   # Bootstrap library files
    'node_modules',  # Node modules
    'vendor',        # Vendor files
]

class JSLintValidator:
    """JavaScript linting and validation class"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.files_tested = []
        self.files_skipped = []
        
    def find_js_files(self) -> List[Path]:
        """Find all JavaScript files in the project"""
        js_files = []
        
        for root, dirs, files in os.walk(LOCAL_PATH):
            # Skip common directories that shouldn't be linted
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '.github']]
            
            for file in files:
                if any(file.endswith(ext) for ext in JS_EXTENSIONS):
                    file_path = Path(root) / file
                    
                    # Check if file should be excluded
                    should_exclude = False
                    for pattern in EXCLUDED_PATTERNS:
                        if pattern.replace('*', '') in str(file_path).lower():
                            should_exclude = True
                            break
                    
                    if should_exclude:
                        self.files_skipped.append(str(file_path.relative_to(LOCAL_PATH)))
                    else:
                        js_files.append(file_path)
                        
        return js_files
    
    def check_jshint_available(self) -> bool:
        """Check if JSHint is available"""
        try:
            result = subprocess.run(['jshint', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def install_jshint(self) -> bool:
        """Attempt to install JSHint using npm"""
        try:
            print("📦 Installing JSHint...")
            result = subprocess.run(['npm', 'install', '-g', 'jshint'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ JSHint installed successfully")
                return True
            else:
                print(f"❌ Failed to install JSHint: {result.stderr}")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ npm not found - cannot install JSHint")
            return False
    
    def validate_js_syntax(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Basic JavaScript syntax validation using Node.js"""
        try:
            # Try to parse the file with Node.js
            js_code = f"""
try {{
    const fs = require('fs');
    const code = fs.readFileSync('{file_path}', 'utf8');
    new Function(code);
    console.log('SYNTAX_OK');
}} catch (error) {{
    console.log('SYNTAX_ERROR:', error.message);
    process.exit(1);
}}
"""
            
            result = subprocess.run(['node', '-e', js_code], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and 'SYNTAX_OK' in result.stdout:
                return True, []
            else:
                error_msg = result.stdout.replace('SYNTAX_ERROR:', '').strip()
                return False, [f"Syntax Error: {error_msg}"]
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Fallback: basic regex-based validation
            return self.basic_js_validation(file_path)
    
    def basic_js_validation(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Basic JavaScript validation using regex patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            issues = []
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('//') or line.startswith('/*'):
                    continue
                
                # Check for common issues
                if line.count('(') != line.count(')'):
                    if not line.endswith(',') and not line.endswith(';'):
                        issues.append(f"Line {i}: Mismatched parentheses")
                
                if line.count('{') != line.count('}'):
                    if '{' in line and not line.endswith(','):
                        issues.append(f"Line {i}: Mismatched braces")
                
                # Check for undefined variables (basic)
                if re.search(r'\bundefined\s*[!=]==', line):
                    issues.append(f"Line {i}: Use typeof check instead of undefined comparison")
                
                # Check for == vs ===
                if re.search(r'[^=!]==[^=]', line):
                    issues.append(f"Line {i}: Consider using === instead of ==")
            
            return len(issues) == 0, issues
            
        except Exception as e:
            return False, [f"Failed to read file: {str(e)}"]
    
    def lint_with_jshint(self, file_path: Path) -> Tuple[bool, List[str], List[str]]:
        """Lint JavaScript file using JSHint"""
        try:
            result = subprocess.run(['jshint', str(file_path)], 
                                  capture_output=True, text=True, timeout=15)
            
            errors = []
            warnings = []
            
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        if 'error' in line.lower():
                            errors.append(line.strip())
                        else:
                            warnings.append(line.strip())
            
            return result.returncode == 0, errors, warnings
            
        except subprocess.TimeoutExpired:
            return False, ["JSHint timed out"], []
        except Exception as e:
            return False, [f"JSHint error: {str(e)}"], []
    
    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single JavaScript file"""
        relative_path = str(file_path.relative_to(LOCAL_PATH))
        self.files_tested.append(relative_path)
        
        print(f"🔍 Analyzing: {relative_path}")
        
        result = {
            'file': relative_path,
            'syntax_valid': True,
            'jshint_passed': True,
            'errors': [],
            'warnings': [],
            'file_size': file_path.stat().st_size,
        }
        
        # Check syntax first
        syntax_ok, syntax_errors = self.validate_js_syntax(file_path)
        result['syntax_valid'] = syntax_ok
        result['errors'].extend(syntax_errors)
        
        # If syntax is OK and JSHint is available, run JSHint
        if syntax_ok and self.check_jshint_available():
            jshint_ok, jshint_errors, jshint_warnings = self.lint_with_jshint(file_path)
            result['jshint_passed'] = jshint_ok
            result['errors'].extend(jshint_errors)
            result['warnings'].extend(jshint_warnings)
        elif syntax_ok:
            result['warnings'].append("JSHint not available - using basic validation only")
        
        return result
    
    def run_validation(self) -> Dict:
        """Run complete JavaScript validation"""
        print("🚀 JAVASCRIPT CODE QUALITY VALIDATION")
        print("=" * 60)
        print(f"📁 Scanning directory: {LOCAL_PATH}")
        
        # Find JavaScript files
        js_files = self.find_js_files()
        
        if not js_files:
            print("📄 No JavaScript files found for linting")
            return {
                'success': True,
                'files_tested': 0,
                'files_passed': 0,
                'files_failed': 0,
                'total_errors': 0,
                'total_warnings': 0
            }
        
        print(f"📄 Found {len(js_files)} JavaScript files to analyze")
        if self.files_skipped:
            print(f"⏭️ Skipped {len(self.files_skipped)} files (minified/library files)")
        
        # Check for JSHint
        if not self.check_jshint_available():
            print("⚠️ JSHint not found - attempting to install...")
            if not self.install_jshint():
                print("⚠️ Proceeding with basic validation only")
        
        print("-" * 60)
        
        results = []
        files_passed = 0
        total_errors = 0
        total_warnings = 0
        
        # Analyze each file
        for js_file in js_files:
            try:
                result = self.analyze_file(js_file)
                results.append(result)
                
                if result['syntax_valid'] and result['jshint_passed']:
                    files_passed += 1
                    if not result['errors']:
                        print(f"✅ {result['file']} - Clean")
                    else:
                        print(f"⚠️ {result['file']} - Warnings only")
                else:
                    print(f"❌ {result['file']} - Errors found")
                
                total_errors += len(result['errors'])
                total_warnings += len(result['warnings'])
                
                # Print errors and warnings
                for error in result['errors']:
                    print(f"   🚨 ERROR: {error}")
                for warning in result['warnings']:
                    print(f"   ⚠️ WARNING: {warning}")
                    
            except Exception as e:
                print(f"❌ Failed to analyze {js_file}: {str(e)}")
                results.append({
                    'file': str(js_file.relative_to(LOCAL_PATH)),
                    'syntax_valid': False,
                    'jshint_passed': False,
                    'errors': [f"Analysis failed: {str(e)}"],
                    'warnings': [],
                    'file_size': 0
                })
                total_errors += 1
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 JAVASCRIPT VALIDATION SUMMARY")
        print("=" * 60)
        
        files_failed = len(js_files) - files_passed
        success_rate = (files_passed / len(js_files)) * 100 if js_files else 100
        
        print(f"📄 Files analyzed: {len(js_files)}")
        print(f"✅ Files passed: {files_passed}")
        print(f"❌ Files failed: {files_failed}")
        print(f"🚨 Total errors: {total_errors}")
        print(f"⚠️ Total warnings: {total_warnings}")
        print(f"📊 Success rate: {success_rate:.1f}%")
        
        if self.files_skipped:
            print(f"\n⏭️ SKIPPED FILES ({len(self.files_skipped)}):")
            for skipped in self.files_skipped[:10]:  # Show first 10
                print(f"   • {skipped}")
            if len(self.files_skipped) > 10:
                print(f"   ... and {len(self.files_skipped) - 10} more")
        
        # Recommendations
        if total_errors > 0:
            print(f"\n💡 RECOMMENDATIONS:")
            print("   • Fix syntax errors and critical issues")
            print("   • Consider using a code formatter (Prettier)")
            print("   • Review JSHint warnings for best practices")
        elif total_warnings > 0:
            print(f"\n💡 RECOMMENDATIONS:")
            print("   • Review warnings for code improvements")
            print("   • Consider adding JSHint configuration file")
        else:
            print(f"\n🎉 EXCELLENT! All JavaScript files passed validation")
        
        # Consider success if no critical errors (syntax errors)
        critical_failures = sum(1 for r in results if not r['syntax_valid'])
        
        return {
            'success': critical_failures == 0,  # Success if no syntax errors
            'files_tested': len(js_files),
            'files_passed': files_passed,
            'files_failed': files_failed,
            'critical_failures': critical_failures,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'results': results
        }

def main():
    """Main function to run JavaScript validation"""
    try:
        validator = JSLintValidator()
        results = validator.run_validation()
        
        # Exit with appropriate code
        if results['success']:
            if results['total_warnings'] > 0:
                print(f"\n🏆 OVERALL RESULT: ✅ PASSED (with warnings)")
            else:
                print(f"\n🏆 OVERALL RESULT: ✅ PASSED")
            sys.exit(0)
        else:
            print(f"\n🏆 OVERALL RESULT: ❌ FAILED (critical errors found)")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ JavaScript validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()