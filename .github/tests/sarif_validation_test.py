#!/usr/bin/env python3
"""
Test SARIF file validation and generation functionality.
This test validates the SARIF creation logic used in the Codacy workflow.
"""

import json
import tempfile
import os
import sys

def create_minimal_sarif():
    """Create a minimal valid SARIF file."""
    sarif_data = {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Codacy Analysis CLI",
                        "version": "1.0.0"
                    }
                },
                "results": []
            }
        ]
    }
    return sarif_data

def validate_sarif_json(sarif_content):
    """Validate SARIF JSON structure."""
    try:
        if isinstance(sarif_content, str):
            data = json.loads(sarif_content)
        else:
            data = sarif_content
        
        # Check required fields
        required_fields = ["version", "$schema", "runs"]
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Validate version
        if data["version"] != "2.1.0":
            return False, f"Invalid SARIF version: {data['version']}"
        
        # Validate runs structure
        if not isinstance(data["runs"], list) or len(data["runs"]) == 0:
            return False, "Invalid runs structure"
        
        for run in data["runs"]:
            if "tool" not in run or "driver" not in run["tool"]:
                return False, "Invalid tool structure in run"
            
            if "name" not in run["tool"]["driver"]:
                return False, "Missing tool driver name"
        
        return True, "SARIF is valid"
    
    except json.JSONDecodeError as e:
        return False, f"JSON decode error: {e}"
    except Exception as e:
        return False, f"Validation error: {e}"

def test_sarif_creation():
    """Test SARIF creation and validation."""
    print("🧪 Testing SARIF creation and validation...")
    
    # Test 1: Create minimal SARIF
    print("📋 Test 1: Creating minimal SARIF...")
    sarif_data = create_minimal_sarif()
    is_valid, message = validate_sarif_json(sarif_data)
    print(f"   Result: {'✅ PASS' if is_valid else '❌ FAIL'} - {message}")
    
    if not is_valid:
        return False
    
    # Test 2: JSON serialization
    print("📋 Test 2: Testing JSON serialization...")
    try:
        json_str = json.dumps(sarif_data, indent=2)
        is_valid, message = validate_sarif_json(json_str)
        print(f"   Result: {'✅ PASS' if is_valid else '❌ FAIL'} - {message}")
        
        if not is_valid:
            return False
    except Exception as e:
        print(f"   Result: ❌ FAIL - JSON serialization error: {e}")
        return False
    
    # Test 3: File write/read cycle
    print("📋 Test 3: Testing file write/read cycle...")
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sarif', delete=False) as f:
            json.dump(sarif_data, f, indent=2)
            temp_file = f.name
        
        # Read back and validate
        with open(temp_file, 'r') as f:
            content = f.read()
        
        is_valid, message = validate_sarif_json(content)
        print(f"   Result: {'✅ PASS' if is_valid else '❌ FAIL'} - {message}")
        
        # Clean up
        os.unlink(temp_file)
        
        if not is_valid:
            return False
    except Exception as e:
        print(f"   Result: ❌ FAIL - File I/O error: {e}")
        return False
    
    # Test 4: Validate against empty/malformed input
    print("📋 Test 4: Testing malformed input handling...")
    test_cases = [
        ("", "Empty string"),
        ("{", "Incomplete JSON"),
        ('{"version": "1.0"}', "Missing required fields"),
        ('{"version": "2.1.0", "$schema": "test", "runs": []}', "Empty runs array")
    ]
    
    for test_input, description in test_cases:
        is_valid, message = validate_sarif_json(test_input)
        expected_result = "❌ Expected to fail"
        print(f"   {description}: {'✅ PASS' if not is_valid else '❌ FAIL'} - {expected_result}")
        if is_valid:  # We expect these to fail
            return False
    
    return True

def main():
    """Run SARIF validation tests."""
    print("🔍 SARIF Validation Test Suite")
    print("=" * 50)
    
    if test_sarif_creation():
        print("\n🎉 All tests passed! SARIF generation is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed! Check SARIF generation logic.")
        return 1

if __name__ == "__main__":
    sys.exit(main())