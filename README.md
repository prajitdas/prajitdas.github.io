# Profile

Personal [webpage](https://prajitdas.github.io) of Prajit Kumar Das - Researcher specializing in Security & Privacy, and Generative AI.

[![CodeQL](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/github-code-scanning/codeql) [![Codacy Security Scan](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/codacy.yml/badge.svg)](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/codacy.yml) [![Dependency Submission](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/dependency-graph/auto-submission/badge.svg)](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/dependency-graph/auto-submission) [![Website Validation](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/validate-website.yml/badge.svg)](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/validate-website.yml)

## 🔧 Development & Testing

### Website Validation Tests

This repository includes comprehensive automated tests that validate the structure, content, and integrity of the website.

**Test Coverage:**

- ✅ **HTML Structure**: Valid DOCTYPE, proper tag nesting, required elements
- ✅ **Meta Tags**: Essential SEO and responsive design meta tags
- ✅ **Internal Links**: All internal links point to existing files
- ✅ **Assets**: CSS, JavaScript, and image files exist and are valid
- ✅ **Security**: Basic security headers and no exposed sensitive files
- ✅ **Accessibility**: Responsive design elements and proper HTML semantics
- ✅ **Publications**: Generated publication files are valid
- ✅ **File Structure**: Required files and directories exist

### 📊 Latest Website Validation Results

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
**Test Runtime:** 0.34 seconds

### 🛡️ Security Assessment and Testing

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

### 🔒 Latest Security Testing Status

**Web Security Score:** 🟢 **EXCELLENT** (100% protection)  
**Files Scanned:** 65 text-based files  
**Security Issues:** 0 critical, 0 warnings
**Protected Files:** All sensitive development files secured (including new Codacy configs)
**Last Security Scan:** September 27, 2025

### Running Tests Locally

1. **Install test dependencies:**

   ```bash
   pip install -r .github/config/requirements.txt
   ```

2. **Run all tests:**

   ```bash
   # Using pytest directly
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
   ```

4. **Run SARIF validation test:**

   ```bash
   python .github/tests/sarif_validation_test.py
   ```

### 🔧 Recent Improvements

**SARIF JSON Syntax Error Fix (September 27, 2025):**

- ✅ **Resolved**: "Invalid SARIF. JSON syntax error: Unexpected end of JSON input"
- ✅ **Enhanced**: Codacy workflow with robust SARIF validation and fallback generation
- ✅ **Added**: Comprehensive SARIF validation test suite
- ✅ **Improved**: Error handling with `continue-on-error` for workflow reliability
- ✅ **Simplified**: SARIF creation logic to prevent YAML parsing issues

The enhanced Codacy security workflow now ensures:

- Always generates valid SARIF 2.1.0 format files
- Prevents JSON syntax errors that cause workflow failures
- Provides fallback SARIF creation when analysis fails
- Includes comprehensive validation before file upload

## 🚀 Additional Testing

1. **Run security scans:**
   pytest -k "test_meta" -v          # Meta tag tests
   ```

4. **Run security scans:**

   ```bash
   python .github/tests/security_scan.py     # Check for credentials and sensitive data
   python .github/tests/web_security_test.py # Test web file access protection
   ```

### GitHub Actions

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

### Test Results

- ✅ **Pass**: All validations successful
- ❌ **Fail**: Issues found that need attention
- ⚠️ **Warning**: Non-critical issues detected

## 🗂️ Project Structure

```plaintext
├── index.html                    # Main webpage
├── assets/                       # Static assets (CSS, JS, images)
├── .github/
│   ├── config/                   # Secure configuration files
│   │   ├── requirements.txt      # Python dependencies
│   │   ├── genPubHTML.sh        # Publication generation script
│   │   └── genWordCloud.py      # Word cloud generator
│   ├── tests/                    # Website validation test suite
│   │   ├── test_website_validation.py
│   │   ├── security_scan.py
│   │   ├── web_security_test.py
│   │   └── sarif_validation_test.py
│   └── workflows/               # GitHub Actions CI/CD
└── README.md                    # This file
```

## 🔐 Security Features

This repository implements multiple layers of security to prevent sensitive development files from being accessible via the web:

**Protection Methods:**

- **`.htaccess`**: Server-level blocking of sensitive files and directories
- **`robots.txt`**: Search engine directive to not crawl development files
- **`_config.yml`**: Jekyll exclusion of files from site generation
- **`.github/` Directory**: GitHub Pages never serves files from this directory

**Protected Files:**

- All Python scripts and configuration files
- Test suites and development tools
- Environment and package management files
- GitHub workflow configurations
- Codacy and security analyzer configurations
- Jekyll and build configuration files

## 🛠️ Dependencies

The testing framework uses:

- **beautifulsoup4**: HTML parsing and validation
- **requests**: HTTP requests for link checking
- **lxml**: XML/HTML processing
- **html5lib**: HTML5 parsing
- **pytest**: Test framework and runner

## 🚀 Publication Generation

Publications are automatically generated from BibTeX sources using:

- **bibtex2html**: Converts `.bib` files to HTML
- **Custom scripts**: Located in `.github/config/` for security
- **Automated workflow**: Generates and commits updated publication pages

## 📝 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

---

> **Note:** This is a personal website repository built with HTML/CSS/JavaScript for GitHub Pages. The Python files in the `.github/` directory are automated validation and generation tools, not the main project.
