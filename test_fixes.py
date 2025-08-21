
#!/usr/bin/env python3
"""
Test script to verify specific fixes applied to the Sigilcraft application
"""

import requests
import json
import time
import sys

# Test configuration
NODE_URL = 'http://localhost:5000'
FLASK_PORTS = [5001, 5002, 5003, 5004, 5005]

def get_flask_url():
    """Find the active Flask port"""
    for port in FLASK_PORTS:
        try:
            import requests
            response = requests.get(f'http://localhost:{port}/health', timeout=2)
            if response.status_code == 200:
                return f'http://localhost:{port}'
        except:
            continue
    return None

def test_vibe_combinations():
    """Test that multiple vibe combinations work correctly"""
    print("🧪 Testing vibe combinations...")
    
    test_cases = [
        {"phrase": "Test Love", "vibe": "mystical"},
        {"phrase": "Test Love", "vibe": "crystal"},
        {"phrase": "Test Love", "vibe": "elemental+crystal"},
        {"phrase": "Test Love", "vibe": "elemental+crystal+cosmic"},
        {"phrase": "Test Love", "vibe": "elemental+crystal+cosmic+mystical+light+shadow"}
    ]
    
    success_count = 0
    for i, test_case in enumerate(test_cases):
        try:
            print(f"  Testing case {i+1}: '{test_case['phrase']}' with vibe '{test_case['vibe']}'")
            response = requests.post(f'{NODE_URL}/generate', 
                                   json=test_case, 
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('image'):
                    print(f"    ✅ Success")
                    success_count += 1
                else:
                    print(f"    ❌ Failed: {data.get('error', 'Unknown error')}")
            else:
                print(f"    ❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"    ❌ Exception: {e}")
        
        time.sleep(1)  # Delay between requests
    
    print(f"📊 Vibe combination test: {success_count}/{len(test_cases)} passed")
    return success_count == len(test_cases)

def test_error_conditions():
    """Test error handling"""
    print("\n🛡️ Testing error conditions...")
    
    error_cases = [
        {"phrase": "", "vibe": "mystical", "expected_error": True},
        {"phrase": "A", "vibe": "mystical", "expected_error": True},
        {"phrase": "Valid phrase", "vibe": "invalid_vibe", "expected_error": False},  # Should default
    ]
    
    passed = 0
    for i, case in enumerate(error_cases):
        try:
            response = requests.post(f'{NODE_URL}/generate', 
                                   json=case, 
                                   timeout=15)
            
            data = response.json()
            success = data.get('success', False)
            
            if case["expected_error"]:
                if not success:
                    print(f"  ✅ Error case {i+1}: Correctly rejected")
                    passed += 1
                else:
                    print(f"  ❌ Error case {i+1}: Should have been rejected")
            else:
                if success:
                    print(f"  ✅ Valid case {i+1}: Correctly accepted")
                    passed += 1
                else:
                    print(f"  ❌ Valid case {i+1}: Should have been accepted")
                    
        except Exception as e:
            print(f"  ❌ Error case {i+1}: Exception - {e}")
    
    print(f"📊 Error handling: {passed}/{len(error_cases)} passed")
    return passed == len(error_cases)

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

def main():
    print("🔧 SIGILCRAFT FIXES VERIFICATION")
    print("=" * 50)
    
    # Run specific fix tests
    results = []
    results.append(("Server Health", test_server_health()))
    results.append(("Vibe Combinations", test_vibe_combinations()))
    results.append(("Error Handling", test_error_conditions()))
    
    # Print results
    print("\n" + "=" * 50)
    print("🏁 FIX VERIFICATION RESULTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"Overall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL FIXES VERIFIED! Application is working correctly!")
        return 0
    else:
        print("⚠️ Some issues remain. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
