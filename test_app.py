
#!/usr/bin/env python3
"""
Comprehensive test script for the Sigil Generator
Tests uniqueness, vibe differences, and all functionality
"""

import requests
import json
import hashlib
import time
import sys

# Test configuration
BASE_URL = 'http://localhost:5000'
TEST_PHRASES = [
    "Abundance of money",
    "Tash in love with me", 
    "Health and happiness",
    "Success in business",
    "Peace and tranquility",
    "Creative inspiration flows",
    "Protection from negativity",
    "Wisdom and knowledge",
    "Love surrounds me",
    "Confidence and courage"
]

VIBES = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light']

def test_server_connectivity():
    """Test if server is running and responding"""
    print("🧪 Testing server connectivity...")
    try:
        response = requests.get(f'{BASE_URL}/test', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server online: {data.get('status')}")
            return True
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server connectivity failed: {e}")
        return False

def test_unique_generation():
    """Test that different phrases generate unique sigils"""
    print("\n🧪 Testing unique sigil generation...")
    
    generated_hashes = {}
    duplicate_count = 0
    total_tests = 0
    
    for phrase in TEST_PHRASES[:5]:  # Test first 5 phrases
        for vibe in VIBES:
            total_tests += 1
            print(f"  Testing: '{phrase}' with {vibe} vibe...")
            
            try:
                response = requests.post(f'{BASE_URL}/generate', 
                    json={'phrase': phrase, 'vibe': vibe},
                    timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        image_data = data.get('image')
                        if image_data:
                            # Create hash of image data
                            image_hash = hashlib.md5(image_data.encode()).hexdigest()
                            
                            # Check for duplicates
                            key = f"{phrase}_{vibe}"
                            if image_hash in generated_hashes.values():
                                duplicate_count += 1
                                print(f"    ⚠️  Duplicate detected!")
                                # Find which other combination generated this hash
                                for existing_key, existing_hash in generated_hashes.items():
                                    if existing_hash == image_hash:
                                        print(f"       Matches: {existing_key}")
                                        break
                            else:
                                generated_hashes[key] = image_hash
                                print(f"    ✅ Unique sigil generated")
                        else:
                            print(f"    ❌ No image data received")
                    else:
                        print(f"    ❌ Generation failed: {data.get('error')}")
                else:
                    print(f"    ❌ Request failed with status {response.status_code}")
                    
            except Exception as e:
                print(f"    ❌ Request error: {e}")
            
            time.sleep(0.5)  # Small delay between requests
    
    print(f"\n📊 Uniqueness Test Results:")
    print(f"   Total tests: {total_tests}")
    print(f"   Unique sigils: {len(generated_hashes)}")
    print(f"   Duplicates: {duplicate_count}")
    print(f"   Uniqueness rate: {(len(generated_hashes) / total_tests) * 100:.1f}%")
    
    return duplicate_count == 0

def test_vibe_differences():
    """Test that different vibes produce visually different results"""
    print("\n🧪 Testing vibe differences...")
    
    test_phrase = "Test phrase for vibe differences"
    vibe_hashes = {}
    
    for vibe in VIBES:
        print(f"  Testing {vibe} vibe...")
        
        try:
            response = requests.post(f'{BASE_URL}/generate', 
                json={'phrase': test_phrase, 'vibe': vibe},
                timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    image_data = data.get('image')
                    if image_data:
                        image_hash = hashlib.md5(image_data.encode()).hexdigest()
                        vibe_hashes[vibe] = image_hash
                        print(f"    ✅ {vibe} sigil generated")
                    else:
                        print(f"    ❌ No image data for {vibe}")
                else:
                    print(f"    ❌ {vibe} generation failed: {data.get('error')}")
            else:
                print(f"    ❌ {vibe} request failed")
                
        except Exception as e:
            print(f"    ❌ {vibe} error: {e}")
        
        time.sleep(0.5)
    
    # Check if all vibes produced different results
    unique_hashes = len(set(vibe_hashes.values()))
    total_vibes = len(vibe_hashes)
    
    print(f"\n📊 Vibe Difference Results:")
    print(f"   Vibes tested: {total_vibes}")
    print(f"   Unique results: {unique_hashes}")
    
    if unique_hashes == total_vibes:
        print(f"   ✅ All vibes produce different sigils!")
        return True
    else:
        print(f"   ❌ Some vibes produce identical results")
        # Show which vibes are duplicates
        hash_to_vibes = {}
        for vibe, hash_val in vibe_hashes.items():
            if hash_val in hash_to_vibes:
                hash_to_vibes[hash_val].append(vibe)
            else:
                hash_to_vibes[hash_val] = [vibe]
        
        for hash_val, vibes in hash_to_vibes.items():
            if len(vibes) > 1:
                print(f"     Identical: {', '.join(vibes)}")
        
        return False

def test_phrase_differences():
    """Test that different phrases produce different results with same vibe"""
    print("\n🧪 Testing phrase differences...")
    
    test_vibe = "mystical"
    phrase_hashes = {}
    
    for phrase in TEST_PHRASES[:6]:  # Test first 6 phrases
        print(f"  Testing phrase: '{phrase}'...")
        
        try:
            response = requests.post(f'{BASE_URL}/generate', 
                json={'phrase': phrase, 'vibe': test_vibe},
                timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    image_data = data.get('image')
                    if image_data:
                        image_hash = hashlib.md5(image_data.encode()).hexdigest()
                        phrase_hashes[phrase] = image_hash
                        print(f"    ✅ Phrase generated unique sigil")
                    else:
                        print(f"    ❌ No image data")
                else:
                    print(f"    ❌ Generation failed: {data.get('error')}")
            else:
                print(f"    ❌ Request failed")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        time.sleep(0.5)
    
    # Check uniqueness
    unique_hashes = len(set(phrase_hashes.values()))
    total_phrases = len(phrase_hashes)
    
    print(f"\n📊 Phrase Difference Results:")
    print(f"   Phrases tested: {total_phrases}")
    print(f"   Unique results: {unique_hashes}")
    
    if unique_hashes == total_phrases:
        print(f"   ✅ All phrases produce different sigils!")
        return True
    else:
        print(f"   ❌ Some phrases produce identical results")
        return False

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n🧪 Testing edge cases...")
    
    edge_cases = [
        ("", "Empty phrase should be rejected"),
        ("A", "Single character should work"),
        ("12345", "Numbers only should work"),
        ("!@#$%", "Special characters only should work"),
        ("A" * 201, "Over 200 characters should be rejected"),
        ("Mixed 123 !@# Content", "Mixed content should work"),
    ]
    
    passed = 0
    total = len(edge_cases)
    
    for test_phrase, description in edge_cases:
        print(f"  Testing: {description}")
        
        try:
            response = requests.post(f'{BASE_URL}/generate', 
                json={'phrase': test_phrase, 'vibe': 'mystical'},
                timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if test_phrase == "":
                    # Empty phrase should fail
                    if not data.get('success'):
                        print(f"    ✅ Correctly rejected empty phrase")
                        passed += 1
                    else:
                        print(f"    ❌ Should have rejected empty phrase")
                elif len(test_phrase) > 200:
                    # Long phrase should fail
                    if not data.get('success'):
                        print(f"    ✅ Correctly rejected long phrase")
                        passed += 1
                    else:
                        print(f"    ❌ Should have rejected long phrase")
                else:
                    # Other cases should succeed
                    if data.get('success'):
                        print(f"    ✅ Generated sigil successfully")
                        passed += 1
                    else:
                        print(f"    ❌ Should have generated sigil: {data.get('error')}")
            else:
                print(f"    ❌ Request failed with status {response.status_code}")
                
        except Exception as e:
            print(f"    ❌ Request error: {e}")
        
        time.sleep(0.3)
    
    print(f"\n📊 Edge Case Results: {passed}/{total} passed")
    return passed == total

def test_performance():
    """Test generation speed and stability"""
    print("\n🧪 Testing performance...")
    
    test_phrase = "Performance test phrase"
    times = []
    failures = 0
    
    print("  Running 10 consecutive generations...")
    
    for i in range(10):
        start_time = time.time()
        
        try:
            response = requests.post(f'{BASE_URL}/generate', 
                json={'phrase': f"{test_phrase} {i}", 'vibe': 'mystical'},
                timeout=30)
            
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    times.append(duration)
                    print(f"    Test {i+1}: {duration:.2f}s ✅")
                else:
                    failures += 1
                    print(f"    Test {i+1}: Failed - {data.get('error')} ❌")
            else:
                failures += 1
                print(f"    Test {i+1}: HTTP {response.status_code} ❌")
                
        except Exception as e:
            failures += 1
            print(f"    Test {i+1}: Error - {e} ❌")
        
        time.sleep(0.2)
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n📊 Performance Results:")
        print(f"   Successful generations: {len(times)}/10")
        print(f"   Average time: {avg_time:.2f}s")
        print(f"   Fastest: {min_time:.2f}s")
        print(f"   Slowest: {max_time:.2f}s")
        print(f"   Failures: {failures}")
        
        return failures == 0 and avg_time < 10.0
    else:
        print(f"   ❌ All tests failed!")
        return False

def main():
    """Run all tests"""
    print("🔮 SIGIL GENERATOR COMPREHENSIVE TEST SUITE")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Server Connectivity", test_server_connectivity()))
    
    if test_results[0][1]:  # Only proceed if server is online
        test_results.append(("Unique Generation", test_unique_generation()))
        test_results.append(("Vibe Differences", test_vibe_differences()))
        test_results.append(("Phrase Differences", test_phrase_differences()))
        test_results.append(("Edge Cases", test_edge_cases()))
        test_results.append(("Performance", test_performance()))
    
    # Print final results
    print("\n" + "=" * 50)
    print("🏁 FINAL TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"Overall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The sigil generator is working perfectly!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
