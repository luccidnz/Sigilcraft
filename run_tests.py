
#!/usr/bin/env python3
"""
Comprehensive test runner for Sigilcraft
"""
import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def run_command(cmd, timeout=30):
    """Run command with timeout"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"

def test_unified_server():
    """Test unified server"""
    print("🧪 Testing unified server...")
    
    # Determine port from environment
    port = os.environ.get('PORT', '5000')
    base_url = f"http://127.0.0.1:{port}"
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200 and response.text == "OK":
            print("✅ Root endpoint works")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server not responding: {e}")
        return False
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint works")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False
    
    # Test API endpoints
    try:
        response = requests.get(f"{base_url}/api/vibes", timeout=5)
        if response.status_code == 200:
            print("✅ Vibes API endpoint works")
        else:
            print(f"❌ Vibes API endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Vibes API endpoint error: {e}")
        return False
    
    return True

def main():
    """Main test runner"""
    print("🚀 Starting Sigilcraft Health Check...")
    
    # Run pytest first
    print("🧪 Running pytest smoke tests...")
    success, stdout, stderr = run_command("python -m pytest tests/test_smoke.py -v")
    
    if success:
        print("✅ Pytest tests passed")
    else:
        print(f"❌ Pytest tests failed:\n{stderr}")
        return False
    
    # Give servers time to start
    print("⏱️  Waiting for servers to start...")
    time.sleep(3)
    
    # Test unified server
    server_ok = test_unified_server()
    
    if server_ok:
        print("🎉 All tests passed! Sigilcraft is ready!")
        return True
    else:
        print("❌ Server tests failed. Check the logs above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
