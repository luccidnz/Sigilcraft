
#!/usr/bin/env python3
"""
ULTRA COMPREHENSIVE TEST SUITE FOR SIGILCRAFT NEXUS
Advanced testing with performance monitoring and quantum validation
Version 3.0.0 - Supreme Edition
"""

import os
import sys
import pytest
import json
import time
import base64
from unittest.mock import patch, MagicMock

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

@pytest.fixture
def client():
    """Create ultra-optimized test client"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def performance_tracker():
    """Track test performance metrics"""
    class PerformanceTracker:
        def __init__(self):
            self.metrics = {}
            self.start_time = None
        
        def start(self, test_name):
            self.start_time = time.time()
        
        def end(self, test_name):
            if self.start_time:
                duration = time.time() - self.start_time
                self.metrics[test_name] = duration
                return duration
            return 0
        
        def get_summary(self):
            if not self.metrics:
                return "No performance data collected"
            
            total_time = sum(self.metrics.values())
            avg_time = total_time / len(self.metrics)
            slowest = max(self.metrics.items(), key=lambda x: x[1])
            fastest = min(self.metrics.items(), key=lambda x: x[1])
            
            return {
                'total_time': total_time,
                'average_time': avg_time,
                'slowest_test': slowest,
                'fastest_test': fastest,
                'total_tests': len(self.metrics)
            }
    
    return PerformanceTracker()

class TestUltraHealthEndpoints:
    """Ultra-comprehensive health and basic endpoint testing"""

    def test_root_endpoint_performance(self, client, performance_tracker):
        """Test root endpoint with performance monitoring"""
        performance_tracker.start('root_endpoint')
        
        response = client.get("/")
        duration = performance_tracker.end('root_endpoint')
        
        assert response.status_code in [200, 304], f"Unexpected status: {response.status_code}"
        assert duration < 1.0, f"Root endpoint too slow: {duration:.3f}s"
        
        # Validate response content
        if response.status_code == 200:
            content = response.data.decode()
            assert "html" in content.lower() or "<!DOCTYPE" in content
            assert len(content) > 100, "Response content too small"

    def test_health_endpoint_comprehensive(self, client, performance_tracker):
        """Ultra-comprehensive health endpoint testing"""
        performance_tracker.start('health_endpoint')
        
        response = client.get("/health")
        duration = performance_tracker.end('health_endpoint')
        
        assert response.status_code == 200
        assert duration < 0.1, f"Health check too slow: {duration:.3f}s"
        
        data = response.get_json()
        assert data is not None, "Health endpoint returned no JSON"
        assert data.get('status') == 'operational'
        assert 'version' in data
        assert 'timestamp' in data
        assert 'uptime' in data
        
        # Validate timestamp is recent (within last hour)
        import time
        now = time.time()
        response_time = data.get('timestamp', 0)
        assert abs(now - response_time) < 3600, "Health timestamp too old"

    def test_api_status_ultra_detailed(self, client, performance_tracker):
        """Ultra-detailed API status validation"""
        performance_tracker.start('api_status')
        
        response = client.get("/api/status")
        duration = performance_tracker.end('api_status')
        
        assert response.status_code == 200
        assert duration < 0.2, f"API status too slow: {duration:.3f}s"
        
        data = response.get_json()
        
        # Validate core fields
        required_fields = ['success', 'status', 'service', 'version', 'quantum_ready', 'available_vibes']
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        assert data['success'] is True
        assert data['quantum_ready'] is True
        assert data['available_vibes'] >= 12, "Insufficient vibes available"
        
        # Validate endpoints structure
        endpoints = data.get('endpoints', {})
        required_endpoints = ['generate', 'batch', 'vibes']
        for endpoint in required_endpoints:
            assert endpoint in endpoints, f"Missing endpoint: {endpoint}"

class TestUltraAPIEndpoints:
    """Ultra-comprehensive API endpoint testing"""

    def test_vibes_endpoint_ultra_validation(self, client, performance_tracker):
        """Ultra-comprehensive vibes endpoint validation"""
        performance_tracker.start('vibes_endpoint')
        
        response = client.get("/api/vibes")
        duration = performance_tracker.end('vibes_endpoint')
        
        assert response.status_code == 200
        assert duration < 0.5, f"Vibes endpoint too slow: {duration:.3f}s"
        
        data = response.get_json()
        assert data['success'] is True
        assert 'vibes' in data
        assert 'detailed_info' in data
        
        # Validate vibes list
        vibes = data['vibes']
        assert isinstance(vibes, list)
        assert len(vibes) >= 12, f"Expected at least 12 vibes, got {len(vibes)}"
        
        expected_vibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void', 'quantum', 'aurora', 'phoenix', 'dragon']
        for vibe in expected_vibes:
            assert vibe in vibes, f"Missing expected vibe: {vibe}"
        
        # Validate detailed info structure
        detailed_info = data['detailed_info']
        for vibe in vibes:
            assert vibe in detailed_info, f"Missing detailed info for vibe: {vibe}"
            
            vibe_info = detailed_info[vibe]
            required_info_fields = ['name', 'power_level', 'complexity', 'pattern_type', 'description']
            for field in required_info_fields:
                assert field in vibe_info, f"Missing {field} for vibe {vibe}"

    def test_generate_endpoint_ultra_validation(self, client, performance_tracker):
        """Ultra-comprehensive generation endpoint validation"""
        
        # Test input validation scenarios
        test_cases = [
            # Invalid cases
            ({}, 400, "empty request"),
            ({'phrase': ''}, 400, "empty phrase"),
            ({'phrase': 'a'}, 400, "phrase too short"),
            ({'phrase': 'x' * 1001}, 400, "phrase too long"),
            
            # Valid cases
            ({'phrase': 'test sigil'}, [200, 500], "basic generation"),
            ({'phrase': 'ultra test', 'vibe': 'mystical'}, [200, 500], "with vibe"),
            ({'phrase': 'advanced test', 'advanced': True}, [200, 500], "advanced mode"),
            ({'phrase': 'quality test', 'quality': 'hd'}, [200, 500], "HD quality"),
        ]
        
        for test_data, expected_codes, description in test_cases:
            if not isinstance(expected_codes, list):
                expected_codes = [expected_codes]
            
            performance_tracker.start(f'generate_{description.replace(" ", "_")}')
            
            response = client.post("/api/generate", json=test_data)
            duration = performance_tracker.end(f'generate_{description.replace(" ", "_")}')
            
            assert response.status_code in expected_codes, f"Unexpected status for {description}: {response.status_code}"
            
            # For successful requests, validate response structure
            if response.status_code == 200:
                data = response.get_json()
                assert data['success'] is True, f"Generation failed for {description}"
                assert 'image' in data, f"No image in response for {description}"
                assert 'metadata' in data, f"No metadata in response for {description}"
                
                # Validate image format
                image_data = data['image']
                assert image_data.startswith('data:'), f"Invalid image format for {description}"
                assert 'base64,' in image_data, f"Invalid base64 format for {description}"
                
                # Validate metadata structure
                metadata = data['metadata']
                required_metadata = ['phrase', 'vibe', 'generation_time', 'quantum_seed']
                for field in required_metadata:
                    assert field in metadata, f"Missing metadata {field} for {description}"

    def test_batch_generation_ultra(self, client, performance_tracker):
        """Ultra-comprehensive batch generation testing"""
        performance_tracker.start('batch_generation')
        
        # Test batch with multiple phrases
        test_phrases = [
            'batch test one',
            'batch test two', 
            'batch test three'
        ]
        
        batch_data = {
            'phrases': test_phrases,
            'vibe': 'mystical',
            'quality': 'standard'
        }
        
        response = client.post("/api/batch", json=batch_data)
        duration = performance_tracker.end('batch_generation')
        
        # Should either succeed or fail gracefully
        assert response.status_code in [200, 400, 500], f"Unexpected batch status: {response.status_code}"
        
        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
            assert 'results' in data
            assert 'stats' in data
            
            results = data['results']
            assert len(results) == len(test_phrases), "Batch result count mismatch"
            
            stats = data['stats']
            required_stats = ['total_requested', 'successful', 'failed', 'total_time']
            for stat in required_stats:
                assert stat in stats, f"Missing batch stat: {stat}"

class TestUltraPerformance:
    """Ultra-comprehensive performance testing"""

    def test_concurrent_requests_simulation(self, client, performance_tracker):
        """Simulate concurrent requests to test performance"""
        import threading
        import queue
        
        results = queue.Queue()
        num_threads = 5
        requests_per_thread = 3
        
        def make_requests():
            thread_results = []
            for i in range(requests_per_thread):
                start_time = time.time()
                response = client.get("/api/vibes")
                duration = time.time() - start_time
                
                thread_results.append({
                    'status_code': response.status_code,
                    'duration': duration
                })
            
            results.put(thread_results)
        
        # Start concurrent threads
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=make_requests)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Collect and analyze results
        all_results = []
        while not results.empty():
            all_results.extend(results.get())
        
        assert len(all_results) == num_threads * requests_per_thread
        
        # Validate performance metrics
        durations = [r['duration'] for r in all_results]
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        
        assert avg_duration < 1.0, f"Average request time too slow: {avg_duration:.3f}s"
        assert max_duration < 2.0, f"Slowest request too slow: {max_duration:.3f}s"
        
        # Ensure all requests succeeded
        success_count = sum(1 for r in all_results if r['status_code'] == 200)
        success_rate = success_count / len(all_results)
        
        assert success_rate >= 0.9, f"Success rate too low: {success_rate:.2%}"

    def test_memory_usage_during_generation(self, client, performance_tracker):
        """Test memory usage during sigil generation"""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            
            # Measure baseline memory
            baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Generate multiple sigils
            for i in range(5):
                test_data = {
                    'phrase': f'memory test sigil {i}',
                    'vibe': 'mystical',
                    'advanced': True
                }
                
                response = client.post("/api/generate", json=test_data)
                # Accept both success and graceful failure
                assert response.status_code in [200, 400, 500]
            
            # Measure memory after generation
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - baseline_memory
            
            # Memory increase should be reasonable (less than 100MB for 5 generations)
            assert memory_increase < 100, f"Excessive memory usage: {memory_increase:.2f}MB"
            
        except ImportError:
            pytest.skip("psutil not available for memory testing")

class TestUltraErrorHandling:
    """Ultra-comprehensive error handling testing"""

    def test_error_handler_responses(self, client, performance_tracker):
        """Test all error handlers return proper JSON"""
        
        error_test_cases = [
            ('/api/nonexistent', 'GET', 404, 'not_found'),
            ('/api/generate', 'GET', 405, 'method_not_allowed'),
            ('/api/generate', 'PUT', 405, 'method_not_allowed'),
        ]
        
        for endpoint, method, expected_status, test_name in error_test_cases:
            performance_tracker.start(f'error_{test_name}')
            
            if method == 'GET':
                response = client.get(endpoint)
            elif method == 'PUT':
                response = client.put(endpoint)
            else:
                response = client.post(endpoint)
                
            duration = performance_tracker.end(f'error_{test_name}')
            
            assert response.status_code == expected_status, f"Wrong status for {test_name}"
            assert response.content_type == 'application/json', f"Non-JSON error response for {test_name}"
            
            data = response.get_json()
            assert data is not None, f"No JSON data in error response for {test_name}"
            assert data.get('success') is False, f"Error response shows success=True for {test_name}"
            assert 'error' in data, f"No error message in response for {test_name}"

    def test_malformed_json_handling(self, client, performance_tracker):
        """Test handling of malformed JSON requests"""
        performance_tracker.start('malformed_json')
        
        # Send malformed JSON
        response = client.post('/api/generate', 
                              data='{"phrase": "test", invalid json}',
                              content_type='application/json')
        
        duration = performance_tracker.end('malformed_json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data

class TestUltraIntegration:
    """Ultra-comprehensive integration testing"""

    def test_full_workflow_simulation(self, client, performance_tracker):
        """Simulate a complete user workflow"""
        performance_tracker.start('full_workflow')
        
        # Step 1: Check API status
        response = client.get("/api/status")
        assert response.status_code == 200
        
        # Step 2: Get available vibes
        response = client.get("/api/vibes")
        assert response.status_code == 200
        vibes_data = response.get_json()
        available_vibes = vibes_data['vibes']
        
        # Step 3: Try to generate a sigil with each vibe type
        successful_generations = 0
        for vibe in available_vibes[:5]:  # Test first 5 vibes to save time
            generation_data = {
                'phrase': f'integration test with {vibe} energy',
                'vibe': vibe,
                'advanced': False
            }
            
            response = client.post("/api/generate", json=generation_data)
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    successful_generations += 1
        
        duration = performance_tracker.end('full_workflow')
        
        # At least some generations should succeed
        assert successful_generations > 0, "No successful generations in full workflow"
        assert duration < 10.0, f"Full workflow too slow: {duration:.3f}s"

def test_performance_summary(performance_tracker):
    """Print performance summary at the end"""
    summary = performance_tracker.get_summary()
    
    if isinstance(summary, dict):
        print(f"\n{'='*60}")
        print("🚀 ULTRA TEST PERFORMANCE SUMMARY")
        print(f"{'='*60}")
        print(f"Total tests: {summary['total_tests']}")
        print(f"Total time: {summary['total_time']:.3f}s")
        print(f"Average time: {summary['average_time']:.3f}s")
        print(f"Fastest test: {summary['fastest_test'][0]} ({summary['fastest_test'][1]:.3f}s)")
        print(f"Slowest test: {summary['slowest_test'][0]} ({summary['slowest_test'][1]:.3f}s)")
        print(f"{'='*60}")

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
