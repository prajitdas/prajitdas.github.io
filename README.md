# 🌐 Prajit Kumar Das - Personal Website

Personal [webpage](https://prajitdas.github.io) of Prajit Kumar Das - Researcher specializing in Security & Privacy, and Generative AI.

[![CodeQL](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/github-code-scanning/codeql)
[![Codacy Security Scan](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/codacy.yml/badge.svg)](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/codacy.yml)
[![Automatic Dependency Submission](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/dependency-graph/auto-submission/badge.svg)](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/dependency-graph/auto-submission)
[![Website Validation Tests](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/validate-website.yml/badge.svg)](https://github.com/prajitdas/prajitdas.github.io/actions/workflows/validate-website.yml)

## 🎯 About This Repository

This repository hosts a professional personal website built with HTML/CSS/JavaScript for GitHub Pages. It features:

- **Professional portfolio** with research focus on Security & Privacy and Generative AI
- **Comprehensive validation suite** ensuring quality, security, and performance
- **Automated testing** with GitHub Actions integration
- **Security-first approach** with multiple layers of protection
- **Performance optimization** including Core Web Vitals and mobile experience

## 🧪 Comprehensive Website Validation Suite

This repository features a complete, non-redundant test suite validating website functionality, security, performance, and accessibility across **8 comprehensive categories**:

### 🎯 Test Categories Overview

1. **🌐 Website Validation** - HTML structure, meta tags, internal links, security headers (~30s)
2. **📜 JavaScript Quality** - Syntax validation, JSHint analysis, code quality (~20s)
3. **⚡ Performance Optimization** - Critical request chain, LCP optimization (~15s)
4. **🛡️ Security Scanning** - Credential scanning, file protection, sensitive data (~45s)
5. **🔍 SEO Validation** - Sitemap sync, meta tags, structured data, Open Graph (~25s)
6. **🔒 Vulnerability Assessment** - Security headers, SSL/TLS, information disclosure (~30s)
7. **📹 YouTube Performance** - Lazy loading optimization, mobile performance (~10s)
8. **📁 Resource Accessibility** - All 186+ resources tested (HTML, PDF, images, CSS, JS) (~60s)

### 📊 Current Performance Metrics

- **🎯 Overall Success Rate:** 87.5%
- **🔥 Critical Resources Success:** 100% (PDFs, CSS, JS, Images)
- **⚡ Quick Mode Execution:** ~3 minutes
- **🔍 Full Mode Execution:** ~10 minutes
- **📁 Total Resources Tested:** 186+ per run

### � Quick Start

#### **Local Testing**
```bash
# Navigate to tests directory
cd .github/tests

# Run quick validation (3 minutes)
python run_all_validation.py --quick

# Run full validation (10 minutes)
python run_all_validation.py

# Test specific category
python website_validation.py           # HTML validation
python test_resource_accessibility.py  # Resource testing
```

#### **GitHub Actions**
The test suite runs automatically on:
- **Push to main branch** (quick mode)
- **Pull requests** (quick mode)  
- **Weekly schedule** (full mode)
- **Manual trigger** (configurable mode)

### 🎯 Success Criteria

#### **Critical Resources (Must Pass 100%)**
- ✅ All PDF files accessible
- ✅ All CSS files loadable  
- ✅ All JavaScript files valid
- ✅ All images accessible
- ✅ Key files (keybase.txt, robots.txt, sitemap.xml)

#### **Overall Targets**
- **Minimum:** 75% success rate
- **Target:** 85%+ success rate
- **Current Achievement:** 87.5% success rate

#### **Expected Failures (Non-Critical)**
- External DOI links (anti-bot protection)
- Fragment identifiers (#anchor links)
- Temporary external image issues

## � Configuration & Dependencies

### **Test Modes**
- **Quick Mode:** Skips external link validation (3 minutes)
- **Full Mode:** Tests all external links (10 minutes)
- **Environment Variable:** `FAST_VALIDATION=1` forces quick mode

### **Python Dependencies**
```txt
beautifulsoup4==4.14.0  # HTML parsing and validation
requests==2.32.5        # HTTP requests for web testing
lxml==6.0.2            # XML/HTML processing
html5lib==1.1          # HTML5 parsing
pytest>=7.0.0          # Test framework
```

### **External Tools**
- **JSHint** (via npm) - JavaScript linting
- **GitHub Actions** - CI/CD execution

### **Coverage Matrix**

| Test Category | Local Files | Web Files | External Links | Security | Performance |
|---------------|-------------|-----------|----------------|----------|-------------|
| Website Validation | ✅ | ✅ | ⚡ (quick skip) | ✅ Basic | ❌ |
| JavaScript Quality | ✅ | ❌ | ❌ | ❌ | ❌ |
| Performance Optimization | ❌ | ✅ | ❌ | ❌ | ✅ |
| Security Scanning | ✅ | ✅ | ❌ | ✅ Advanced | ❌ |
| SEO Validation | ✅ | ✅ | ❌ | ❌ | ❌ |
| Vulnerability Assessment | ❌ | ✅ | ❌ | ✅ Advanced | ❌ |
| YouTube Performance | ✅ | ✅ | ❌ | ❌ | ✅ |
| Resource Accessibility | ✅ | ✅ | ✅ | ❌ | ❌ |

**Legend:** ✅ Full Coverage, ⚡ Conditional, ❌ Not Covered

## 🛡️ Security Features

This repository implements multiple layers of security with **EXCELLENT** (100% protection) security score:

### **Security Layers**
- **`.htaccess`**: Server-level blocking of sensitive files and directories
- **`robots.txt`**: Search engine directive to not crawl development files  
- **`_config.yml`**: Jekyll exclusion of files from site generation
- **`.github/` Directory**: GitHub Pages never serves files from this directory

### **Security Assessment Results**
- 🔐 **Credential Scanning:** ✅ SECURE (65 files scanned)
- 🔑 **Private Keys:** ✅ SECURE (No SSH/SSL keys exposed)
- 💾 **Database Credentials:** ✅ SECURE (No connection strings)
- 🌐 **Environment Files:** ✅ SECURE (No .env files committed)
- 🛡️ **GitHub Actions:** ✅ SECURE (Proper secrets usage)

### **Protected Files**
All Python scripts, configuration files, test suites, development tools, environment files, GitHub workflows, and security analyzer configurations are protected from web access.

## � Troubleshooting

### **Common Issues**
1. **High failure rate (>25%):** Check external links and network connectivity
2. **JavaScript errors:** Ensure JSHint is installed (`npm install -g jshint`)
3. **Import errors:** Verify all dependencies in requirements.txt are installed
4. **Timeout issues:** Use quick mode for faster execution

### **Debug Mode**
```bash
# Run individual tests for debugging
python -c "from test_resource_accessibility import WebsiteResourceTester; t = WebsiteResourceTester(); t.run_comprehensive_test()"

# Test specific categories
cd .github/tests
python website_validation.py           # HTML validation only
python comprehensive_security_scan.py  # Security scanning only
python seo_optimization.py            # SEO validation only
```

### **Test Results Interpretation**
- ✅ **Pass**: All validations successful
- ❌ **Fail**: Issues found that need attention  
- ⚠️ **Warning**: Non-critical issues detected

## 🏆 Benefits & Features

### **Comprehensive Coverage**
- **186+ resources** tested per run
- **8 different validation categories**
- **Zero redundancy** between tests
- **Efficient execution** (3-10 minutes)

### **Production Ready**
- **Automated CI/CD integration** with GitHub Actions
- **Detailed reporting and artifacts** 
- **Configurable execution modes** (quick/full)
- **Non-blocking for development workflow**

### **Maintainable Architecture**
- **Clear separation of concerns** across test categories
- **Well-documented test categories** with execution times
- **Easy to extend or modify** individual test components
- **Comprehensive error reporting** with actionable insights

## 🗂️ Project Structure

```plaintext
├── index.html                    # Main webpage
├── keybase.txt                   # Identity verification  
├── robots.txt                    # Search engine directives
├── sitemap.xml                   # SEO sitemap
├── assets/                       # Static assets (CSS, JS, images)
│   ├── css/                      # Stylesheets (optimized for performance)
│   ├── js/                       # JavaScript (validated and minified)
│   ├── img/                      # Images and icons
│   └── docs/                     # Documents (PDFs, publications)
├── .github/
│   ├── config/                   # Secure configuration files
│   │   ├── requirements.txt      # Python dependencies
│   │   ├── genPubHTML.sh        # Publication generation script
│   │   └── genWordCloud.py      # Word cloud generator
│   ├── tests/                    # Comprehensive validation test suite
│   │   ├── run_all_validation.py              # Main test runner
│   │   ├── website_validation.py              # HTML validation
│   │   ├── test_resource_accessibility.py     # Resource testing
│   │   ├── comprehensive_security_scan.py     # Security scanning
│   │   ├── vulnerability_assessment.py        # Vulnerability testing
│   │   ├── seo_optimization.py               # SEO validation
│   │   ├── youtube_performance.py            # YouTube optimization
│   │   ├── jslint_validation.py              # JavaScript quality
│   │   ├── critical_request_chain_optimization.py # Performance
│   │   ├── README.md                          # Test documentation
│   │   └── TEST_COVERAGE_MATRIX.md           # Coverage details
│   └── workflows/               # GitHub Actions CI/CD
│       ├── validate-website.yml              # Comprehensive validation
│       ├── codacy.yml                        # Security analysis
│       └── static.yml                        # GitHub Pages deployment
└── README.md                    # This comprehensive guide
```

## 🚀 Publication Generation

Publications are automatically generated from BibTeX sources using:

- **bibtex2html**: Converts `.bib` files to HTML
- **Custom scripts**: Located in `.github/config/` for security  
- **Automated workflow**: Generates and commits updated publication pages
- **Word cloud generation**: Visual representation of research topics

## 📋 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/prajitdas/prajitdas.github.io.git
cd prajitdas.github.io

# Install test dependencies
pip install -r .github/config/requirements.txt

# Install JavaScript linting (optional, for local development)
npm install -g jshint

# Run comprehensive validation
cd .github/tests
python run_all_validation.py --quick
```

## 📝 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

---

> **About:** This is a professional personal website repository built with HTML/CSS/JavaScript for GitHub Pages, featuring comprehensive automated validation, security scanning, and performance optimization. The Python files in `.github/` provide automated testing and generation tools ensuring website quality and security.

**🎯 Key Achievement:** 87.5% overall success rate with 100% critical resource accessibility and EXCELLENT security rating.
