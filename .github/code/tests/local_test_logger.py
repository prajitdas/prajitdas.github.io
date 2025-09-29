#!/usr/bin/env python3
"""
Local Test Logging System
Creates detailed, timestamped logs of test failures for local debugging.
Logs are stored locally and excluded from GitHub uploads.
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class LocalTestLogger:
    """
    Comprehensive local logging system for test suite failures.
    Creates detailed logs with timestamps, URLs, error details, and categorization.
    """
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"test_failures_{timestamp}.log"
        
        # Setup logging
        self.logger = self._setup_logger()
        self.failures = []
        
        # Start logging session
        self.logger.info("=" * 80)
        self.logger.info(f"TEST LOGGING SESSION STARTED: {datetime.now().isoformat()}")
        self.logger.info("=" * 80)
    
    def _setup_logger(self) -> logging.Logger:
        """Setup detailed file logger"""
        logger = logging.getLogger('test_failures')
        logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # File handler with detailed formatting
        file_handler = logging.FileHandler(self.log_file, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Detailed formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def log_test_start(self, test_name: str, description: str = ""):
        """Log the start of a test category"""
        self.logger.info(f"🧪 STARTING TEST: {test_name}")
        if description:
            self.logger.info(f"   Description: {description}")
        self.logger.info("-" * 60)
    
    def log_test_end(self, test_name: str, passed: int, failed: int, execution_time: float = None):
        """Log the end of a test category with summary"""
        self.logger.info(f"✅ COMPLETED TEST: {test_name}")
        self.logger.info(f"   Passed: {passed}, Failed: {failed}")
        if execution_time:
            self.logger.info(f"   Execution Time: {execution_time:.2f}s")
        self.logger.info("-" * 60)
    
    def log_url_failure(self, url: str, error_type: str, status_code: Optional[int] = None, 
                       error_message: str = "", test_category: str = "Unknown"):
        """Log a URL/DOI failure with detailed information"""
        failure_data = {
            'timestamp': datetime.now().isoformat(),
            'type': 'URL_FAILURE',
            'test_category': test_category,
            'url': url,
            'error_type': error_type,
            'status_code': status_code,
            'error_message': error_message,
            'is_doi': url.startswith(('http://dx.doi.org/', 'https://doi.org/', 'https://dx.doi.org/')),
            'domain': self._extract_domain(url)
        }
        
        self.failures.append(failure_data)
        
        # Log to file
        self.logger.error(f"🔗 URL FAILURE: {url}")
        self.logger.error(f"   Test Category: {test_category}")
        self.logger.error(f"   Error Type: {error_type}")
        if status_code:
            self.logger.error(f"   Status Code: {status_code}")
        if error_message:
            self.logger.error(f"   Error Message: {error_message}")
        self.logger.error(f"   Is DOI: {failure_data['is_doi']}")
        self.logger.error(f"   Domain: {failure_data['domain']}")
    
    def log_file_failure(self, file_path: str, error_type: str, error_message: str = "", 
                        test_category: str = "Unknown"):
        """Log a local file failure"""
        failure_data = {
            'timestamp': datetime.now().isoformat(),
            'type': 'FILE_FAILURE',
            'test_category': test_category,
            'file_path': file_path,
            'error_type': error_type,
            'error_message': error_message,
            'file_extension': Path(file_path).suffix,
            'file_size_exists': os.path.exists(file_path)
        }
        
        self.failures.append(failure_data)
        
        # Log to file
        self.logger.error(f"📁 FILE FAILURE: {file_path}")
        self.logger.error(f"   Test Category: {test_category}")
        self.logger.error(f"   Error Type: {error_type}")
        self.logger.error(f"   File Extension: {failure_data['file_extension']}")
        self.logger.error(f"   File Exists: {failure_data['file_size_exists']}")
        if error_message:
            self.logger.error(f"   Error Message: {error_message}")
    
    def log_validation_failure(self, item: str, validation_type: str, expected: str, 
                             actual: str, test_category: str = "Unknown"):
        """Log a validation failure (HTML, CSS, JS, etc.)"""
        failure_data = {
            'timestamp': datetime.now().isoformat(),
            'type': 'VALIDATION_FAILURE',
            'test_category': test_category,
            'item': item,
            'validation_type': validation_type,
            'expected': expected,
            'actual': actual
        }
        
        self.failures.append(failure_data)
        
        # Log to file
        self.logger.error(f"⚠️ VALIDATION FAILURE: {item}")
        self.logger.error(f"   Test Category: {test_category}")
        self.logger.error(f"   Validation Type: {validation_type}")
        self.logger.error(f"   Expected: {expected}")
        self.logger.error(f"   Actual: {actual}")
    
    def log_security_issue(self, file_path: str, issue_type: str, severity: str, 
                          details: str = "", test_category: str = "Security"):
        """Log a security-related issue"""
        failure_data = {
            'timestamp': datetime.now().isoformat(),
            'type': 'SECURITY_ISSUE',
            'test_category': test_category,
            'file_path': file_path,
            'issue_type': issue_type,
            'severity': severity,
            'details': details
        }
        
        self.failures.append(failure_data)
        
        # Log to file
        self.logger.error(f"🛡️ SECURITY ISSUE: {file_path}")
        self.logger.error(f"   Issue Type: {issue_type}")
        self.logger.error(f"   Severity: {severity}")
        if details:
            self.logger.error(f"   Details: {details}")
    
    def log_performance_issue(self, metric: str, value: float, threshold: float, 
                            test_category: str = "Performance"):
        """Log a performance-related issue"""
        failure_data = {
            'timestamp': datetime.now().isoformat(),
            'type': 'PERFORMANCE_ISSUE',
            'test_category': test_category,
            'metric': metric,
            'value': value,
            'threshold': threshold,
            'deviation': value - threshold
        }
        
        self.failures.append(failure_data)
        
        # Log to file
        self.logger.error(f"⚡ PERFORMANCE ISSUE: {metric}")
        self.logger.error(f"   Value: {value}")
        self.logger.error(f"   Threshold: {threshold}")
        self.logger.error(f"   Deviation: {failure_data['deviation']:.2f}")
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL for categorization"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return "unknown"
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate comprehensive failure summary"""
        if not self.failures:
            return {'total_failures': 0, 'summary': 'No failures recorded'}
        
        summary = {
            'session_start': datetime.now().isoformat(),
            'total_failures': len(self.failures),
            'failure_types': {},
            'test_categories': {},
            'domains': {},
            'doi_failures': 0,
            'file_failures': 0,
            'url_failures': 0,
            'top_failing_domains': [],
            'recent_failures': []
        }
        
        # Categorize failures
        for failure in self.failures:
            # By type
            ftype = failure['type']
            summary['failure_types'][ftype] = summary['failure_types'].get(ftype, 0) + 1
            
            # By test category
            category = failure['test_category']
            summary['test_categories'][category] = summary['test_categories'].get(category, 0) + 1
            
            # URL-specific analysis
            if failure['type'] == 'URL_FAILURE':
                summary['url_failures'] += 1
                if failure.get('is_doi'):
                    summary['doi_failures'] += 1
                
                domain = failure.get('domain', 'unknown')
                summary['domains'][domain] = summary['domains'].get(domain, 0) + 1
            
            elif failure['type'] == 'FILE_FAILURE':
                summary['file_failures'] += 1
        
        # Top failing domains
        if summary['domains']:
            summary['top_failing_domains'] = sorted(
                summary['domains'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]
        
        # Recent failures (last 10)
        summary['recent_failures'] = self.failures[-10:] if len(self.failures) > 10 else self.failures
        
        return summary
    

    
    def finalize_session(self):
        """Finalize logging session with summary"""
        summary = self.generate_summary()
        
        self.logger.info("=" * 80)
        self.logger.info("SESSION SUMMARY")
        self.logger.info("=" * 80)
        self.logger.info(f"Total Failures: {summary['total_failures']}")
        
        if summary['total_failures'] > 0:
            self.logger.info(f"URL Failures: {summary['url_failures']}")
            self.logger.info(f"DOI Failures: {summary['doi_failures']}")
            self.logger.info(f"File Failures: {summary['file_failures']}")
            
            # Log failure types
            self.logger.info("\nFailure Types:")
            for ftype, count in summary['failure_types'].items():
                self.logger.info(f"   {ftype}: {count}")
            
            # Log test categories
            self.logger.info("\nTest Categories:")
            for category, count in summary['test_categories'].items():
                self.logger.info(f"   {category}: {count}")
            
            # Log top failing domains
            if summary['top_failing_domains']:
                self.logger.info("\nTop Failing Domains:")
                for domain, count in summary['top_failing_domains']:
                    self.logger.info(f"   {domain}: {count} failures")
        
        self.logger.info("=" * 80)
        self.logger.info(f"SESSION ENDED: {datetime.now().isoformat()}")
        self.logger.info(f"Log saved to: {self.log_file}")
        self.logger.info("=" * 80)
        
        # Console output for immediate feedback
        print(f"\n📋 Test logging completed:")
        print(f"   📄 Log file: {self.log_file}")
        print(f"    Total failures: {summary['total_failures']}")
        if summary.get('doi_failures', 0) > 0:
            print(f"   🔗 DOI failures: {summary['doi_failures']}")
        if summary.get('url_failures', 0) > 0:
            print(f"   🌐 URL failures: {summary['url_failures']}")
        if summary.get('file_failures', 0) > 0:
            print(f"   📁 File failures: {summary['file_failures']}")

# Global logger instance
_logger_instance = None

def get_test_logger() -> LocalTestLogger:
    """Get or create global test logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = LocalTestLogger()
    return _logger_instance

def finalize_test_logging():
    """Finalize and save all test logs"""
    global _logger_instance
    if _logger_instance:
        _logger_instance.finalize_session()
        _logger_instance = None

# Convenience functions for easy integration
def log_url_failure(url: str, error_type: str, status_code: int = None, 
                   error_message: str = "", test_category: str = "Unknown"):
    """Convenience function to log URL failure"""
    logger = get_test_logger()
    logger.log_url_failure(url, error_type, status_code, error_message, test_category)

def log_file_failure(file_path: str, error_type: str, error_message: str = "", 
                    test_category: str = "Unknown"):
    """Convenience function to log file failure"""
    logger = get_test_logger()
    logger.log_file_failure(file_path, error_type, error_message, test_category)

def log_test_start(test_name: str, description: str = ""):
    """Convenience function to log test start"""
    logger = get_test_logger()
    logger.log_test_start(test_name, description)

def log_test_end(test_name: str, passed: int, failed: int, execution_time: float = None):
    """Convenience function to log test end"""
    logger = get_test_logger()
    logger.log_test_end(test_name, passed, failed, execution_time)

def log_validation_failure(item: str, validation_type: str, expected: str, 
                          actual: str, test_category: str = "Unknown"):
    """Convenience function to log validation failure"""
    logger = get_test_logger()
    logger.log_validation_failure(item, validation_type, expected, actual, test_category)

def log_security_issue(file_path: str, issue_type: str, severity: str, 
                      details: str = "", test_category: str = "Security"):
    """Convenience function to log security issue"""
    logger = get_test_logger()
    logger.log_security_issue(file_path, issue_type, severity, details, test_category)

def log_performance_issue(metric: str, value: float, threshold: float, 
                         test_category: str = "Performance"):
    """Convenience function to log performance issue"""
    logger = get_test_logger()
    logger.log_performance_issue(metric, value, threshold, test_category)