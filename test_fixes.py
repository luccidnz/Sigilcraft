
#!/usr/bin/env python3
"""
Comprehensive test suite for Sigilcraft application
Tests all functionality, error handling, and performance
"""

import requests
import json
import time
import sys
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# Test configuration
NODE_URL = 'http://localhost:5000'

def find_flask_port():
    """Find which port Flask is running on"""
    for port in range(5001, 5010):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            if result == 0:
                # Port is open, test if it's Flask
                try:
                    response = requests.get(f'http://localhost:{port}/health', timeout=2)
                    if response.status_code == 200:
                        return port
                except:
                    continue
        except:
            continue
    return None

def get_flask_url():
    """Get Flask URL with dynamic port detection"""
    port = find_flask_port()
    return f'http://localhost:{port}' if port else None

def test_server_health():
    """Test server health endpoints"""
    print("\n❤️ Testing server health...")
    
    try:
        # Test Node.js health
        response = requests.get(f'{NODE_URL}/api/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Node.js health check: {data.get('status', 'unknown')}")
            node_healthy = True
        else:
            print(f"  ❌ Node.js health check failed: {response.status_code}")
            node_healthy = False
    except Exception as e:
        print(f"  ❌ Node.js health check error: {e}")
        node_healthy = False
    
    # Test Flask health with dynamic port detection
    flask_url = get_flask_url()
    if flask_url:
        try:
            response = requests.get(f'{flask_url}/health', timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Flask health check: {data.get('status', 'unknown')} on {flask_url}")
                flask_healthy = True
            else:
                print(f"  ❌ Flask health check failed: {response.status_code}")
                flask_healthy = False
        except Exception as e:
            print(f"  ❌ Flask health check error: {e}")
            flask_healthy = False
    else:
        print(f"  ❌ Flask server not found on any port")
        flask_healthy = False
    
    return node_healthy and flask_healthy

def test_vibe_combinations():
    """Test various vibe combinations for sigil generation"""
    print("\n🧪 Testing vibe combinations...")
    
    test_cases = [
        {"name": "Test Love", "vibe": "mystical"},
        {"name": "Test Love", "vibe": "crystal"},
        {"name": "Test Love", "vibe": "elemental+crystal"},
        {"name": "Test Love", "vibe": "elemental+crystal+cosmic"},
        {"name": "Test Love", "vibe": "elemental+crystal+cosmic+mystical+light+shadow"}
    ]
    
    passed = 0
    for i, case in enumerate(test_cases, 1):
        print(f"  Testing case {i}: '{case['name']}' with vibe '{case['vibe']}'")
        try:
            response = requests.post(f'{NODE_URL}/generate', 
                                   json=case, 
                                   timeout=60)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"    ✅ Generated successfully")
                    passed += 1
                else:
                    print(f"    ❌ Generation failed: {data.get('error', 'Unknown error')}")
            else:
                print(f"    ❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            print(f"    ❌ Exception: {e}")
    
    print(f"📊 Vibe combination test: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)

def test_error_handling():
    """Test error conditions and edge cases"""
    print("\n🛡️ Testing error conditions...")
    
    error_cases = [
        {"name": "", "vibe": "mystical"},  # Empty name
        {"name": "x" * 1000, "vibe": "mystical"},  # Very long name
        {"name": "Test", "vibe": "invalid_vibe"}  # Invalid vibe
    ]
    
    passed = 0
    for i, case in enumerate(error_cases, 1):
        print(f"  Error case {i}: {case}")
        try:
            response = requests.post(f'{NODE_URL}/generate', 
                                   json=case, 
                                   timeout=30)
            if response.status_code in [400, 422]:
                print(f"    ✅ Properly rejected with {response.status_code}")
                passed += 1
            elif response.status_code == 200:
                data = response.json()
                if not data.get('success'):
                    print(f"    ✅ Handled gracefully: {data.get('error', 'Unknown error')}")
                    passed += 1
                else:
                    print(f"    ❌ Should have failed but succeeded")
            else:
                print(f"    ❌ Unexpected status: {response.status_code}")
        except Exception as e:
            print(f"    ❌ Error case {i}: Exception - {e}")
    
    print(f"📊 Error handling: {passed}/{len(error_cases)} passed")
    return passed == len(error_cases)

def test_performance():
    """Test performance with concurrent requests"""
    print("\n⚡ Testing performance...")
    
    def make_request():
        try:
            start = time.time()
            response = requests.post(f'{NODE_URL}/generate', 
                                   json={"name": "Performance Test", "vibe": "mystical"}, 
                                   timeout=30)
            duration = time.time() - start
            return response.status_code == 200, duration
        except Exception as e:
            return False, 999
    
    # Test concurrent requests
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(make_request) for _ in range(5)]
        results = [future.result() for future in as_completed(futures)]
    
    successful = sum(1 for success, _ in results if success)
    avg_time = sum(duration for _, duration in results) / len(results)
    
    print(f"  📊 Concurrent requests: {successful}/5 successful")
    print(f"  📊 Average response time: {avg_time:.2f}s")
    
    return successful >= 3 and avg_time < 30

def main():
    """Run all tests"""
    print("🔧 SIGILCRAFT FIXES VERIFICATION")
    print("=" * 50)
    
    # Run all tests
    health_ok = test_server_health()
    vibe_ok = test_vibe_combinations()
    error_ok = test_error_handling()
    perf_ok = test_performance()
    
    # Summary
    print("\n" + "=" * 50)
    print("🏁 FIX VERIFICATION RESULTS")
    print("=" * 50)
    print(f"Server Health        {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Vibe Combinations    {'✅ PASS' if vibe_ok else '❌ FAIL'}")
    print(f"Error Handling       {'✅ PASS' if error_ok else '❌ FAIL'}")
    print(f"Performance          {'✅ PASS' if perf_ok else '❌ FAIL'}")
    print("-" * 50)
    
    total_tests = 4
    passed_tests = sum([health_ok, vibe_ok, error_ok, perf_ok])
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"Overall: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("🎉 All tests passed! Sigilcraft is working perfectly!")
        return 0
    elif success_rate >= 75:
        print("⚠️ Most tests passed. Minor issues remain.")
        return 1
    else:
        print("⚠️ Some issues remain. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
