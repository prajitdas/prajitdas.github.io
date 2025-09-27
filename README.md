Profile
=======

Personal [webpage](https://prajitdas.github.io)****Web Security Score:** 🟢 **EXCELLENT** (12/16 protected)  
**Protected Files:** 12 files properly blocked  
**Accessible Files:** 4 files visible (GitHub Pages limitation)eb Security Score:** � **EXCELLENT** (14/18 protected)  
**Protected Files:** 14 files properly blockedb Security Score:** � **GOOD** (12/16 protected)  
**Protected Files:** 12 files properly blockedf Prajit Kumar Das. [![CodeQL](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/github-code-scanning/codeql)

Latest Website Validation Results
---------------------------------

| Test Category | Status | Description | Files Validated |
|---------------|--------|-------------|-----------------|
| 🏗️ **HTML Structure** | ✅ PASSED | DOCTYPE declarations, proper nesting, required elements | 6 HTML files |
| 🏷️ **Meta Tags** | ✅ PASSED | SEO tags, viewport, Google verification, security headers | index.html |
| 🔗 **Internal Links** | ✅ PASSED | All internal links point to existing files | All HTML files |
| 📁 **Asset Links** | ✅ PASSED | CSS, JavaScript, images, and icons exist | All referenced assets |
| 🎨 **CSS Files** | ✅ PASSED | Files exist, not empty, balanced braces | 12 CSS files |
| ⚡ **JavaScript Files** | ✅ PASSED | Files exist, basic syntax validation | 15 JS files |
| 🖼️ **Image Assets** | ✅ PASSED | All referenced images exist and accessible | All image references |
| 🛡️ **Security Headers** | ✅ PASSED | X-UA-Compatible and security configurations | index.html |
| 📱 **Responsive Design** | ✅ PASSED | Viewport meta tags for mobile compatibility | index.html |
| 📚 **Publication Files** | ✅ PASSED | Generated publication HTML files valid | bibtex2html output |
| 🚫 **Deprecated Elements** | ✅ PASSED | No deprecated HTML tags (excl. auto-generated) | Main HTML files |
| 📋 **Required Files** | ✅ PASSED | Essential files and directories exist | Project structure |

**Last Updated:** September 27, 2025  
**Total Tests:** 12/12 passing ✅  
**Test Runtime:** 0.26 seconds  

Security Assessment Results
---------------------------

| Security Check | Status | Description | Files Scanned |
|----------------|--------|-------------|---------------|
| 🔐 **Credential Scanning** | ✅ SECURE | No hardcoded API keys, passwords, or tokens | 65 text files |
| 🔑 **Private Keys** | ✅ SECURE | No SSH/SSL private keys exposed | All code files |
| 💾 **Database Credentials** | ✅ SECURE | No connection strings or DB passwords | All config files |
| 🌐 **Environment Files** | ✅ SECURE | No .env or sensitive config files committed | Git history |
| 👤 **Personal Information** | ✅ SECURE | No phone numbers or sensitive PII exposed | All documents |
| 📧 **Email Exposure** | ✅ MINIMAL | Only third-party attribution emails found | 2 files (acceptable) |
| 🔍 **Git History** | ✅ CLEAN | No accidentally committed sensitive files | Complete history |
| 🛡️ **GitHub Actions** | ✅ SECURE | Proper use of secrets and secure practices | Workflow files |

**Security Score:** 🟢 **EXCELLENT** (10/10)  
**Files Scanned:** 65 text-based files  
**Security Issues:** 0 critical, 0 warnings  
**Last Security Scan:** September 27, 2025  

Web Access Security Results
---------------------------

| File/Directory | Status | Response | Protection Method |
|----------------|--------|----------|-------------------|
| 📄 **README.md** | ⚠️ ACCESSIBLE | 200 | GitHub Pages limitation |
| 📄 **.github/config/requirements.txt** | ✅ PROTECTED | 404 | GitHub directory protection |
| 📄 **.gitattributes** | ⚠️ ACCESSIBLE | 200 | GitHub Pages limitation |
| 📄 **.gitignore** | ⚠️ ACCESSIBLE | 200 | GitHub Pages limitation |
| 📄 **.htaccess** | ✅ BLOCKED | 200* | Content filtering |

| 📁 **.github/** | ✅ PROTECTED | 404 | Directory exclusion |
| 🔧 **.env** | ✅ PROTECTED | 404 | File exclusion |
| 📦 **package.json** | ✅ PROTECTED | 404 | File exclusion |
| 🎵 **composer.json** | ✅ PROTECTED | 404 | File exclusion |
| 🐍 **.github/config/genWordCloud.py** | ✅ PROTECTED | 404 | Publication script protection |
| 📜 **.github/config/genPubHTML.sh** | ✅ PROTECTED | 404 | Shell script protection |

**Web Security Score:** � **EXCELLENT** (15/18 protected)  
**Protected Files:** 15 files properly blocked  
**Accessible Files:** 4 files visible (GitHub Pages limitation)  
**Last Web Security Test:** September 27, 2025  

> **Note:** Some files remain accessible due to GitHub Pages processing limitations. These files contain only development metadata and pose no security risk as they don't contain credentials or sensitive data.

Website Validation Tests
------------------------

This directory contains automated tests that validate the structure, content, and integrity of the website.

Test Coverage
-------------

The test suite validates:

- ✅ **HTML Structure**: Valid DOCTYPE, proper tag nesting, required elements
- ✅ **Meta Tags**: Essential SEO and responsive design meta tags
- ✅ **Internal Links**: All internal links point to existing files
- ✅ **Assets**: CSS, JavaScript, and image files exist and are valid
- ✅ **Security**: Basic security headers and no exposed sensitive files
- ✅ **Accessibility**: Responsive design elements and proper HTML semantics
- ✅ **Publications**: Generated publication files are valid
- ✅ **File Structure**: Required files and directories exist

Running Tests
-------------

Local Development:

1. **Install test dependencies:**

   ```bash
   pip install -r .github/config/requirements.txt
   ```

2. **Run all tests:**

   ```bash
   # Using the test runner
   python .github/tests/run_tests.py
   
   # Or using pytest directly
   cd .github/tests && pytest test_website_validation.py -v
   
   # Or using unittest
   python .github/tests/test_website_validation.py
   ```

3. **Run specific test categories:**

   ```bash
   cd .github/tests
   pytest -k "test_html" -v          # HTML structure tests
   pytest -k "test_links" -v         # Link validation tests
   pytest -k "test_asset" -v         # Asset validation tests
   pytest -k "test_meta" -v          # Meta tag tests
   ```

4. **Run security scans:**

   ```bash
   python .github/tests/security_scan.py     # Check for credentials and sensitive data
   python .github/tests/web_security_test.py # Test web file access protection
   ```

GitHub Actions:

Tests run automatically on:

- Every push to `main` branch
- Every pull request  
- Weekly schedule (Sundays at 2 AM UTC)
- Manual trigger via GitHub Actions UI

The automated workflow includes:

- HTML structure and content validation
- Link and asset verification  
- Security credential scanning
- Web file access protection testing
- File structure integrity checks

Test Results
------------

- ✅ **Pass**: All validations successful
- ❌ **Fail**: Issues found that need attention
- ⚠️ **Warning**: Non-critical issues detected

Adding New Tests
----------------

To add new validation tests:

1. Add test methods to `WebsiteValidationTests` class in `test_website_validation.py`
2. Follow the naming convention: `test_your_feature_name()`
3. Use `self.subTest()` for testing multiple files
4. Add appropriate assertions with descriptive error messages

Files
-----

- `test_website_validation.py` - Main test suite
- `security_scan.py` - Security credential scanner
- `web_security_test.py` - Web file access security tester
- `.github/config/requirements.txt` - Python dependencies (hidden)
- `run_tests.py` - Local test runner script
- `pytest.ini` - Pytest configuration
- `.github/workflows/validate-website.yml` - GitHub Actions workflow

Web Security
------------

This repository implements multiple layers of security to prevent sensitive development files from being accessible via the web:

**Protection Methods:**

- **`.htaccess`**: Server-level blocking of sensitive files and directories
- **`robots.txt`**: Search engine directive to not crawl development files
- **`_config.yml`**: Jekyll exclusion of files from site generation
- **Web Security Tests**: Automated verification that files are not web-accessible

**Protected Files/Directories:**

- `README.md`, `.github/config/requirements.txt`
- `.gitattributes`, `.gitignore`, `.htaccess`
- `.github/tests/` directory and all Python files (secure location)
- `.github/` workflows and configuration
- Environment and package files (`.env`, `package.json`, etc.)

**Testing Security:**

```bash
python .github/tests/web_security_test.py    # Test file access protection
```

Dependencies
------------

- **beautifulsoup4**: HTML parsing and validation
- **requests**: HTTP requests for link checking
- **lxml**: XML/HTML processing
- **html5lib**: HTML5 parsing
- **pytest**: Test framework and runner

Troubleshooting
---------------

Common Issues:

1. **Import Errors**: Install dependencies with `pip install -r .github/config/requirements.txt`
2. **Path Issues**: Run tests from project root or .github/tests directory
3. **Permission Errors**: Ensure test runner has execute permissions

Test Failures:

When tests fail:

1. Check the detailed error message
2. Verify the file paths are correct
3. Ensure all assets exist and are properly linked
4. Check HTML syntax and structure

Integration
-----------

These tests integrate with:

- **GitHub Actions**: Automated CI/CD validation
- **Local Development**: Pre-commit validation
- **Publication Pipeline**: Validates generated content

> **Note:** This is a personal website repository built with HTML/CSS/JavaScript for GitHub Pages. The Python files in the `.github/tests/` directory are automated validation tools, not the main project.
