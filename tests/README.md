# Website Validation Tests

This directory contains automated tests that validate the structure, content, and integrity of the website.

## Test Coverage

The test suite validates:

- ✅ **HTML Structure**: Valid DOCTYPE, proper tag nesting, required elements
- ✅ **Meta Tags**: Essential SEO and responsive design meta tags
- ✅ **Internal Links**: All internal links point to existing files
- ✅ **Assets**: CSS, JavaScript, and image files exist and are valid
- ✅ **Security**: Basic security headers and no exposed sensitive files
- ✅ **Accessibility**: Responsive design elements and proper HTML semantics
- ✅ **Publications**: Generated publication files are valid
- ✅ **File Structure**: Required files and directories exist

## Running Tests

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r tests/requirements.txt
   ```

2. **Run all tests:**
   ```bash
   # Using the test runner
   python tests/run_tests.py
   
   # Or using pytest directly
   cd tests && pytest test_website_validation.py -v
   
   # Or using unittest
   python tests/test_website_validation.py
   ```

3. **Run specific test categories:**
   ```bash
   cd tests
   pytest -k "test_html" -v          # HTML structure tests
   pytest -k "test_links" -v         # Link validation tests
   pytest -k "test_asset" -v         # Asset validation tests
   pytest -k "test_meta" -v          # Meta tag tests
   ```

### GitHub Actions

Tests run automatically on:
- Every push to `main` branch
- Every pull request
- Weekly schedule (Sundays at 2 AM UTC)
- Manual trigger via GitHub Actions UI

## Test Results

- ✅ **Pass**: All validations successful
- ❌ **Fail**: Issues found that need attention
- ⚠️ **Warning**: Non-critical issues detected

## Adding New Tests

To add new validation tests:

1. Add test methods to `WebsiteValidationTests` class in `test_website_validation.py`
2. Follow the naming convention: `test_your_feature_name()`
3. Use `self.subTest()` for testing multiple files
4. Add appropriate assertions with descriptive error messages

## Files

- `test_website_validation.py` - Main test suite
- `requirements.txt` - Python dependencies
- `run_tests.py` - Local test runner script
- `pytest.ini` - Pytest configuration
- `.github/workflows/validate-website.yml` - GitHub Actions workflow

## Dependencies

- **beautifulsoup4**: HTML parsing and validation
- **requests**: HTTP requests for link checking
- **lxml**: XML/HTML processing
- **html5lib**: HTML5 parsing
- **pytest**: Test framework and runner

## Troubleshooting

### Common Issues

1. **Import Errors**: Install dependencies with `pip install -r tests/requirements.txt`
2. **Path Issues**: Run tests from project root or tests directory
3. **Permission Errors**: Ensure test runner has execute permissions

### Test Failures

When tests fail:
1. Check the detailed error message
2. Verify the file paths are correct
3. Ensure all assets exist and are properly linked
4. Check HTML syntax and structure

## Integration

These tests integrate with:
- **GitHub Actions**: Automated CI/CD validation
- **Local Development**: Pre-commit validation
- **Publication Pipeline**: Validates generated content