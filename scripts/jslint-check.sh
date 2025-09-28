#!/bin/bash

# JSLint Testing Script for prajitdas.github.io
# This script runs JSLint on all JavaScript files and provides detailed reporting

set -e

echo "🔍 JSLint Code Quality Analysis for prajitdas.github.io"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create reports directory
mkdir -p reports

# Function to check if jslint is installed
check_jslint() {
    if ! command -v jslint &> /dev/null; then
        echo -e "${RED}JSLint is not installed. Installing...${NC}"
        npm install -g jslint
    else
        echo -e "${GREEN}JSLint is available${NC}"
    fi
}

# Function to lint a specific file
lint_file() {
    local file=$1
    local filename=$(basename "$file")
    
    echo -e "\n${BLUE}Linting: $file${NC}"
    echo "----------------------------------------"
    
    if jslint "$file" --maxlen=120 --browser --node --es6 2>&1; then
        echo -e "${GREEN}✅ $filename passed JSLint validation${NC}"
        return 0
    else
        echo -e "${RED}❌ $filename failed JSLint validation${NC}"
        return 1
    fi
}

# Function to generate HTML report
generate_html_report() {
    cat > reports/jslint-report.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSLint Code Quality Report - prajitdas.github.io</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { background: #42A8C0; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .success { color: #27ae60; background: #d5f4e6; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .error { color: #e74c3c; background: #fadbd8; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .file-section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 4px; }
        .timestamp { color: #666; font-size: 0.9em; }
        pre { background: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>JSLint Code Quality Report</h1>
            <p>Generated for prajitdas.github.io on $(date)</p>
        </div>
EOF

    echo "        <div class='file-section'>" >> reports/jslint-report.html
    echo "            <h2>JavaScript Files Analyzed</h2>" >> reports/jslint-report.html
    
    # Add results for each file
    for file in assets/js/*.js; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            echo "            <h3>$filename</h3>" >> reports/jslint-report.html
            
            if jslint "$file" --maxlen=120 --browser --node --es6 > /dev/null 2>&1; then
                echo "            <div class='success'>✅ Passed JSLint validation</div>" >> reports/jslint-report.html
            else
                echo "            <div class='error'>❌ Failed JSLint validation</div>" >> reports/jslint-report.html
                echo "            <pre>" >> reports/jslint-report.html
                jslint "$file" --maxlen=120 --browser --node --es6 2>&1 | head -20 >> reports/jslint-report.html
                echo "            </pre>" >> reports/jslint-report.html
            fi
        fi
    done
    
    cat >> reports/jslint-report.html << 'EOF'
        </div>
    </div>
</body>
</html>
EOF

    echo -e "\n${GREEN}📄 HTML report generated: reports/jslint-report.html${NC}"
}

# Main execution
main() {
    echo -e "${BLUE}Starting JSLint analysis...${NC}\n"
    
    check_jslint
    
    # Initialize counters
    passed=0
    failed=0
    total=0
    
    # Test each JavaScript file
    for file in assets/js/*.js; do
        if [ -f "$file" ]; then
            total=$((total + 1))
            if lint_file "$file"; then
                passed=$((passed + 1))
            else
                failed=$((failed + 1))
            fi
        fi
    done
    
    # Generate reports
    generate_html_report
    
    # Summary
    echo -e "\n${BLUE}Summary:${NC}"
    echo "========"
    echo -e "Total files tested: ${YELLOW}$total${NC}"
    echo -e "Passed: ${GREEN}$passed${NC}"
    echo -e "Failed: ${RED}$failed${NC}"
    
    if [ $failed -eq 0 ]; then
        echo -e "\n${GREEN}🎉 All JavaScript files pass JSLint validation!${NC}"
        exit 0
    else
        echo -e "\n${RED}⚠️  Some files failed JSLint validation. Please fix the issues above.${NC}"
        exit 1
    fi
}

# Run main function
main "$@"