#!/usr/bin/env python3
"""
Smoke test for nnvisualization server
Tests CSV loading, security (path traversal), and basic page serving
"""

import sys
import time
import json
import subprocess
import urllib.request
import urllib.error
from io import StringIO
import csv

PORT = 8080
BASE_URL = f"http://localhost:{PORT}"

def test_csv_to_json_conversion():
    """Unit test: CSV to JSON conversion"""
    print("Test 1: CSV to JSON conversion...")
    
    # Import the read_csv function
    sys.path.insert(0, '.')
    from server import read_csv
    
    # Test data
    csv_content = "x,y\n1,2\n3,4\n5,6"
    csv_file = StringIO(csv_content)
    
    result = read_csv(csv_file)
    data = json.loads(result)
    
    expected = [
        {"x": "1", "y": "2"},
        {"x": "3", "y": "4"},
        {"x": "5", "y": "6"}
    ]
    
    assert data == expected, f"Expected {expected}, got {data}"
    print("  ✓ CSV to JSON conversion works correctly")

def start_server():
    """Start the server in background"""
    print(f"\nStarting server on port {PORT}...")
    process = subprocess.Popen(
        [sys.executable, 'server.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    max_retries = 10
    for i in range(max_retries):
        try:
            urllib.request.urlopen(f"{BASE_URL}/", timeout=1)
            print(f"  ✓ Server started successfully")
            return process
        except (urllib.error.URLError, ConnectionRefusedError):
            if i < max_retries - 1:
                time.sleep(0.5)
            else:
                raise Exception("Server failed to start")

def test_main_page():
    """Test that main page loads"""
    print("\nTest 2: Main page loads...")
    
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/")
        content = response.read().decode('utf-8')
        
        assert response.status == 200
        assert 'TensorFlow.js' in content or 'tensorflow' in content.lower()
        assert '<html>' in content.lower()
        
        print("  ✓ Main page loads successfully")
        return True
    except Exception as e:
        print(f"  ✗ Main page test failed: {e}")
        return False

def test_csv_endpoint():
    """Test CSV data endpoint returns valid JSON"""
    print("\nTest 3: CSV endpoint returns valid JSON...")
    
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/data_ex2.csv")
        content = response.read().decode('utf-8')
        
        assert response.status == 200
        data = json.loads(content)
        
        # Verify it's a list of objects with x and y keys
        assert isinstance(data, list), "CSV data should be a list"
        assert len(data) > 0, "CSV data should not be empty"
        assert 'x' in data[0] and 'y' in data[0], "CSV data should have x and y keys"
        
        print(f"  ✓ CSV endpoint works ({len(data)} rows loaded)")
        return True
    except Exception as e:
        print(f"  ✗ CSV endpoint test failed: {e}")
        return False

def test_path_traversal_blocked():
    """Test that path traversal attempts are blocked"""
    print("\nTest 4: Path traversal security...")
    
    # Test various path traversal patterns
    test_paths = [
        "/../README.md",
        "/%2e%2e/README.md",  # URL encoded ..
        "/..%2fREADME.md",
        "/../server.py",
    ]
    
    all_blocked = True
    for path in test_paths:
        try:
            urllib.request.urlopen(f"{BASE_URL}{path}")
            print(f"  ✗ Path traversal NOT blocked: {path}")
            all_blocked = False
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"  ✓ Path traversal blocked (403): {path}")
            elif e.code == 404:
                print(f"  ✓ Path traversal blocked (404): {path}")
            else:
                print(f"  ? Unexpected status {e.code} for: {path}")
                all_blocked = False
        except Exception as e:
            print(f"  ✗ Unexpected error for {path}: {e}")
            all_blocked = False
    
    return all_blocked

def test_javascript_loads():
    """Test that JavaScript file loads"""
    print("\nTest 5: JavaScript file loads...")
    
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/main.js")
        content = response.read().decode('utf-8')
        
        assert response.status == 200
        assert 'function' in content or 'const' in content
        
        print("  ✓ JavaScript file loads successfully")
        return True
    except Exception as e:
        print(f"  ✗ JavaScript test failed: {e}")
        return False

def test_training_demo_seams():
    """Test that page and JavaScript contain the expected training demo hooks"""
    print("\nTest 6: Training demo seams...")

    try:
        script_response = urllib.request.urlopen(f"{BASE_URL}/main.js")
        script = script_response.read().decode('utf-8')
        page_response = urllib.request.urlopen(f"{BASE_URL}/")
        page = page_response.read().decode('utf-8')

        assert 'model.fit(xs, ys' in script, "main.js should train the linear model"
        assert 'displayData(data)' in script, "main.js should render loaded data"
        assert 'updateTrainingStatus' in script, "main.js should render training status/loss"
        assert 'displayPrediction' in script, "main.js should render predictions"
        assert 'data-display' in page, "index.html should contain a data output target"
        assert 'training-status' in page, "index.html should contain a training output target"
        assert 'prediction-display' in page, "index.html should contain a prediction output target"

        print("  ✓ Training demo hooks are present")
        return True
    except Exception as e:
        print(f"  ✗ Training demo seam test failed: {e}")
        return False

def main():
    """Run all smoke tests"""
    print("=" * 60)
    print("NN Visualization Smoke Tests")
    print("=" * 60)
    
    results = []
    server_process = None
    
    try:
        # Test 1: Unit test (no server needed)
        test_csv_to_json_conversion()
        results.append(True)
        
        # Start server for integration tests
        server_process = start_server()
        time.sleep(1)  # Give server a moment to fully initialize
        
        # Run integration tests
        results.append(test_main_page())
        results.append(test_csv_endpoint())
        results.append(test_path_traversal_blocked())
        results.append(test_javascript_loads())
        results.append(test_training_demo_seams())
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        results.append(False)
    
    finally:
        # Clean up: stop server
        if server_process:
            print("\nStopping server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✅ All smoke tests PASSED")
        return 0
    else:
        print("\n❌ Some tests FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
