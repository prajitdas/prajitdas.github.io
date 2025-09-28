# JSLint Testing Setup for prajitdas.github.io

This document explains the JSLint testing setup for the personal website of Dr. Prajit Kumar Das.

## Overview

JSLint is a JavaScript code quality tool that helps identify potential problems in JavaScript code. This setup provides automated testing for all JavaScript files in the website.

## Files Added/Modified

### Configuration Files
- `package.json` - Node.js project configuration with JSLint dependencies
- `.jslintrc` - JSLint configuration settings
- `.github/workflows/jslint.yml` - GitHub Actions workflow for automated testing

### Scripts
- `scripts/jslint-check.sh` - Comprehensive JSLint testing script with reporting

### JavaScript Files (Updated for JSLint Compliance)
- `assets/js/main.js` - Main JavaScript file (reformatted for JSLint)
- `assets/js/custom.js` - Custom JavaScript file (reformatted for JSLint)

## JSLint Configuration

The `.jslintrc` file contains the following key settings:

```json
{
  "browser": true,      // Allow browser globals
  "node": true,         // Allow Node.js globals
  "es6": true,          // Allow ES6 features
  "maxlen": 120,        // Maximum line length
  "predef": [           // Predefined globals
    "jQuery", "$", "console", "window", "document", ...
  ]
}
```

## Available NPM Scripts

Run these commands in the project root:

```bash
# Lint all JavaScript files
npm run lint

# Lint with verbose output
npm run lint:verbose

# Lint specific files
npm run lint:main     # Only main.js
npm run lint:custom   # Only custom.js

# Run all tests (currently just JSLint)
npm test

# Start development server
npm run dev

# Build (includes linting)
npm run build
```

## Manual Testing

### Using NPM Scripts (Recommended)
```bash
# Install dependencies first
npm install

# Run JSLint on all files
npm run lint

# Run with detailed output
npm run lint:verbose
```

### Using the Shell Script
```bash
# Make script executable (if not already)
chmod +x scripts/jslint-check.sh

# Run the comprehensive test script
./scripts/jslint-check.sh
```

### Direct JSLint Usage
```bash
# Install JSLint globally
npm install -g jslint

# Test individual files
jslint assets/js/main.js --maxlen=120 --browser --node --es6
jslint assets/js/custom.js --maxlen=120 --browser --node --es6
```

## Automated Testing

### GitHub Actions
The workflow runs automatically on:
- Push to main/master/develop branches
- Pull requests to main/master
- Changes to JavaScript files or configuration

### CI/CD Pipeline
1. **Checkout** - Gets the latest code
2. **Setup Node.js** - Installs Node.js (versions 16, 18, 20)
3. **Install Dependencies** - Runs `npm ci`
4. **Run JSLint Tests** - Tests individual and all files
5. **Generate Reports** - Creates detailed test reports
6. **Upload Artifacts** - Saves results for download

## Code Quality Standards

### JSLint Rules Enforced
- **Strict Mode**: All files must use 'use strict'
- **Proper Indentation**: 4 spaces, consistent formatting
- **Variable Declarations**: All variables must be declared
- **Function Scope**: Proper function scoping and closures
- **Line Length**: Maximum 120 characters per line
- **Global Variables**: Explicitly defined in configuration

### Common Issues Fixed
1. **Implicit Globals**: Added proper global declarations
2. **Variable Naming**: Used descriptive variable names
3. **Function Structure**: Wrapped code in IIFEs (Immediately Invoked Function Expressions)
4. **String Quotes**: Consistent use of single quotes
5. **Semicolons**: Proper semicolon usage

## Pre-commit Hooks (Optional)

To run JSLint before every commit, add this to `.git/hooks/pre-commit`:

```bash
#!/bin/sh
echo "Running JSLint checks..."
npm run lint
if [ $? -ne 0 ]; then
    echo "JSLint checks failed. Commit aborted."
    exit 1
fi
```

## Troubleshooting

### Common JSLint Errors

1. **"Missing 'use strict' statement"**
   - Solution: Add `'use strict';` at the beginning of functions

2. **"Undeclared variable"**
   - Solution: Add variable to `predef` array in `.jslintrc` or declare properly

3. **"Line too long"**
   - Solution: Break long lines or increase `maxlen` in configuration

4. **"Expected '{' and instead saw '"'**
   - Solution: Fix bracket placement and string quote consistency

### Installation Issues

If you encounter permission issues:
```bash
# Use npm without sudo
npm config set prefix ~/.npm-global
export PATH=~/.npm-global/bin:$PATH
```

## Integration with IDEs

### VS Code
Install the JSLint extension:
```bash
code --install-extension ms-vscode.jslint
```

### WebStorm/IntelliJ
JSLint is built-in. Configure in: Settings → Languages & Frameworks → JavaScript → Code Quality Tools → JSLint

## Reporting

### Console Output
- ✅ Passed files shown in green
- ❌ Failed files shown in red
- Detailed error messages with line numbers

### HTML Reports
Generated in `reports/jslint-report.html` with:
- Timestamp of analysis
- File-by-file results
- Detailed error information
- Professional styling

### GitHub Actions Reports
- Summary in job output
- Downloadable artifacts
- Matrix testing across Node.js versions

## Maintenance

### Regular Tasks
1. **Update Dependencies**: Run `npm update` monthly
2. **Review Rules**: Periodically review and update `.jslintrc`
3. **Check New Files**: Ensure new JS files follow standards
4. **Monitor CI**: Check GitHub Actions for failures

### Adding New JavaScript Files
1. Create the file with proper JSLint headers:
   ```javascript
   /*jslint browser: true, node: true, es6: true */
   /*global jQuery, console */
   
   (function () {
       'use strict';
       // Your code here
   }());
   ```
2. Test locally: `npm run lint`
3. Commit and push (CI will test automatically)

## Benefits

1. **Code Quality**: Consistent code style and best practices
2. **Early Bug Detection**: Catches potential issues before deployment
3. **Team Collaboration**: Ensures all contributors follow same standards
4. **Automated Testing**: No manual checking required
5. **Professional Standards**: Industry-standard code quality tool

## Contact

For questions about this JSLint setup, please refer to:
- [JSLint Documentation](http://jslint.com/help.html)
- [Project Issues](https://github.com/prajitdas/prajitdas.github.io/issues)

---

*This JSLint setup ensures that the prajitdas.github.io website maintains high JavaScript code quality standards.*