
#!/usr/bin/env python3
"""
Comprehensive test suite for Sigilcraft application
Tests all functionality, error handling, and performance
"""

import requests
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Test configuration
NODE_URL = 'http://localhost:5000'
FLASK_URL = 'http://localhost:5001'

def test_server_health():
    """Test if both servers are running"""
    print("🔍 Testing server health...")
    
    # Test Node.js server
    try:
        response = requests.get(f'{NODE_URL}/api/test', timeout=10)
        if response.status_code == 200:
            print("✅ Node.js server is healthy")
            node_healthy = True
        else:
            print(f"❌ Node.js server returned {response.status_code}")
            node_healthy = False
    except Exception as e:
        print(f"❌ Node.js server unreachable: {e}")
        node_healthy = False
    
    # Test Flask server
    try:
        response = requests.get(f'{FLASK_URL}/health', timeout=10)
        if response.status_code == 200:
            print("✅ Flask server is healthy")
            flask_healthy = True
        else:
            print(f"❌ Flask server returned {response.status_code}")
            flask_healthy = False
    except Exception as e:
        print(f"❌ Flask server unreachable: {e}")
        flask_healthy = False
    
    return node_healthy and flask_healthy

def test_generation_endpoints():
    """Test sigil generation through both direct and proxy endpoints"""
    print("\n🎨 Testing sigil generation...")
    
    test_cases = [
        {"phrase": "Love", "vibe": "mystical"},
        {"phrase": "Success", "vibe": "cosmic"},
        {"phrase": "Health", "vibe": "elemental"},
        {"phrase": "Prosperity and abundance", "vibe": "crystal+light"},
        {"phrase": "A", "vibe": "shadow"},  # Edge case: very short
        {"phrase": "Protection from all negativity", "vibe": "mystical+shadow+crystal"}  # Complex case
    ]
    
    results = {"direct": [], "proxy": []}
    
    for test_case in test_cases:
        # Test direct Flask endpoint
        try:
            start_time = time.time()
            response = requests.post(f'{FLASK_URL}/generate', 
                                   json=test_case, 
                                   timeout=30)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('image'):
                    print(f"✅ Direct: '{test_case['phrase']}' ({test_case['vibe']}) - {duration:.2f}s")
                    results["direct"].append(True)
                else:
                    print(f"❌ Direct: '{test_case['phrase']}' failed - {data.get('error')}")
                    results["direct"].append(False)
            else:
                print(f"❌ Direct: '{test_case['phrase']}' HTTP {response.status_code}")
                results["direct"].append(False)
        except Exception as e:
            print(f"❌ Direct: '{test_case['phrase']}' error - {e}")
            results["direct"].append(False)
        
        # Test proxy endpoint
        try:
            start_time = time.time()
            response = requests.post(f'{NODE_URL}/generate', 
                                   json=test_case, 
                                   timeout=30)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('image'):
                    print(f"✅ Proxy: '{test_case['phrase']}' ({test_case['vibe']}) - {duration:.2f}s")
                    results["proxy"].append(True)
                else:
                    print(f"❌ Proxy: '{test_case['phrase']}' failed - {data.get('error')}")
                    results["proxy"].append(False)
            else:
                print(f"❌ Proxy: '{test_case['phrase']}' HTTP {response.status_code}")
                results["proxy"].append(False)
        except Exception as e:
            print(f"❌ Proxy: '{test_case['phrase']}' error - {e}")
            results["proxy"].append(False)
        
        time.sleep(0.5)  # Small delay between requests
    
    return results

def test_error_handling():
    """Test error handling with invalid inputs"""
    print("\n🛡️ Testing error handling...")
    
    error_test_cases = [
        {"phrase": "", "vibe": "mystical", "expected": "empty phrase"},
        {"phrase": "A" * 300, "vibe": "mystical", "expected": "too long"},
        {"phrase": "Test", "vibe": "invalid_vibe", "expected": "should default to mystical"},
        {"phrase": "Test", "vibe": "", "expected": "should default to mystical"},
        {"invalid_key": "value", "expected": "missing phrase"}
    ]
    
    passed = 0
    total = len(error_test_cases)
    
    for i, test_case in enumerate(error_test_cases):
        try:
            response = requests.post(f'{FLASK_URL}/generate', 
                                   json=test_case, 
                                   timeout=15)
            
            if response.status_code in [200, 400]:
                data = response.json()
                expected = test_case["expected"]
                
                if "empty phrase" in expected and not data.get('success'):
                    print(f"✅ Error test {i+1}: Correctly rejected empty phrase")
                    passed += 1
                elif "too long" in expected and not data.get('success'):
                    print(f"✅ Error test {i+1}: Correctly rejected long phrase")
                    passed += 1
                elif "should default" in expected and data.get('success'):
                    print(f"✅ Error test {i+1}: Correctly defaulted invalid vibe")
                    passed += 1
                elif "missing phrase" in expected and not data.get('success'):
                    print(f"✅ Error test {i+1}: Correctly rejected missing phrase")
                    passed += 1
                else:
                    print(f"❌ Error test {i+1}: Unexpected result - {data.get('error', 'unknown')}")
            else:
                print(f"❌ Error test {i+1}: Unexpected HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error test {i+1}: Exception - {e}")
    
    print(f"📊 Error handling: {passed}/{total} tests passed")
    return passed == total

def test_concurrent_load():
    """Test concurrent request handling"""
    print("\n⚡ Testing concurrent load...")
    
    def make_request(i):
        try:
            start_time = time.time()
            response = requests.post(f'{NODE_URL}/generate',
                                   json={"phrase": f"Test {i}", "vibe": "mystical"},
                                   timeout=30)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                return {"success": data.get('success', False), "duration": duration, "id": i}
            else:
                return {"success": False, "duration": duration, "id": i, "status": response.status_code}
        except Exception as e:
            return {"success": False, "duration": time.time() - start_time, "id": i, "error": str(e)}
    
    # Test with 5 concurrent requests
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request, i) for i in range(5)]
        results = []
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result["success"]:
                print(f"✅ Concurrent request {result['id']}: {result['duration']:.2f}s")
            else:
                error_info = result.get("error", result.get("status", "unknown"))
                print(f"❌ Concurrent request {result['id']}: {error_info}")
    
    successful = sum(1 for r in results if r["success"])
    avg_duration = sum(r["duration"] for r in results) / len(results)
    
    print(f"📊 Concurrent load: {successful}/5 successful, avg {avg_duration:.2f}s")
    return successful >= 4  # Allow 1 failure

def test_pro_functionality():
    """Test Pro-related endpoints"""
    print("\n👑 Testing Pro functionality...")
    
    # Test Pro status check
    try:
        response = requests.get(f'{NODE_URL}/api/is-pro', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Pro status check: {data}")
            pro_check = True
        else:
            print(f"❌ Pro status check failed: {response.status_code}")
            pro_check = False
    except Exception as e:
        print(f"❌ Pro status check error: {e}")
        pro_check = False
    
    # Test Pro key verification
    try:
        test_key = "test_key_123"
        response = requests.post(f'{NODE_URL}/api/verify-pro',
                               json={"key": test_key},
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Pro key verification: {data}")
            key_verify = True
        else:
            print(f"❌ Pro key verification failed: {response.status_code}")
            key_verify = False
    except Exception as e:
        print(f"❌ Pro key verification error: {e}")
        key_verify = False
    
    return pro_check and key_verify

def main():
    """Run all tests"""
    print("🔮 SIGILCRAFT COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Server Health", test_server_health()))
    
    if test_results[0][1]:  # Only proceed if servers are healthy
        generation_results = test_generation_endpoints()
        direct_success = sum(generation_results["direct"])
        proxy_success = sum(generation_results["proxy"])
        total_tests = len(generation_results["direct"])
        
        test_results.append((f"Direct Generation ({direct_success}/{total_tests})", direct_success >= total_tests * 0.8))
        test_results.append((f"Proxy Generation ({proxy_success}/{total_tests})", proxy_success >= total_tests * 0.8))
        test_results.append(("Error Handling", test_error_handling()))
        test_results.append(("Concurrent Load", test_concurrent_load()))
        test_results.append(("Pro Functionality", test_pro_functionality()))
    else:
        print("❌ Servers not healthy, skipping other tests")
    
    # Print final results
    print("\n" + "=" * 60)
    print("🏁 FINAL TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"Overall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Sigilcraft is fully operational!")
        return 0
    elif passed >= total * 0.8:
        print("⚠️  Most tests passed. Minor issues detected.")
        return 0
    else:
        print("❌ Multiple tests failed. Major issues detected.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
