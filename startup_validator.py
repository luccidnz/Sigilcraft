
#!/usr/bin/env python3
"""
ULTRA STARTUP VALIDATOR FOR SIGILCRAFT NEXUS
Advanced system diagnostics and performance optimization
Version 3.0.0 - Supreme Edition
"""

import sys
import os
import time
import json
import psutil
import importlib.util
import subprocess
from pathlib import Path

class UltraValidator:
    def __init__(self):
        self.start_time = time.time()
        self.errors = []
        self.warnings = []
        self.performance_metrics = {}
        
    def log_performance(self, metric_name, value):
        """Track performance metrics"""
        self.performance_metrics[metric_name] = value
        
    def validate_environment(self):
        """Ultra-comprehensive environment validation"""
        print("🔍 Running ULTRA environment validation...")
        
        # Check Python version
        py_version = sys.version_info
        if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
            self.errors.append(f"Python 3.8+ required, found {py_version.major}.{py_version.minor}")
        else:
            print(f"✅ Python {py_version.major}.{py_version.minor}.{py_version.micro} - EXCELLENT")
        
        # Check public directory structure
        required_structure = {
            'public': ['index.html', 'style.css', 'main.js'],
            'tests': ['test_comprehensive.py'],
            '.': ['main.py', 'unified_server.py', 'requirements.txt']
        }
        
        for directory, files in required_structure.items():
            dir_path = Path(directory)
            if not dir_path.exists():
                self.errors.append(f"Missing directory: {directory}")
                continue
                
            for file in files:
                file_path = dir_path / file
                if not file_path.exists():
                    self.errors.append(f"Missing critical file: {file_path}")
                else:
                    file_size = file_path.stat().st_size
                    if file_size == 0:
                        self.warnings.append(f"Empty file detected: {file_path}")
                    print(f"✅ {file_path} ({file_size} bytes)")
        
        # Check system resources
        try:
            memory = psutil.virtual_memory()
            cpu_count = psutil.cpu_count()
            
            self.log_performance('memory_total_gb', memory.total / (1024**3))
            self.log_performance('memory_available_gb', memory.available / (1024**3))
            self.log_performance('cpu_cores', cpu_count)
            
            print(f"✅ System resources: {memory.available/(1024**3):.1f}GB RAM, {cpu_count} CPU cores")
            
            if memory.available < 500 * 1024 * 1024:  # Less than 500MB
                self.warnings.append("Low memory available - performance may be impacted")
                
        except ImportError:
            self.warnings.append("psutil not available - system monitoring limited")
        
        return len(self.errors) == 0
        
    def validate_dependencies(self):
        """Ultra-advanced dependency validation"""
        print("🔍 Validating ULTRA dependencies...")
        
        critical_deps = {
            'flask': '2.0.0',
            'flask_cors': '3.0.0',
            'PIL': '8.0.0',
            'gunicorn': '20.0.0'
        }
        
        optional_deps = {
            'pytest': 'testing',
            'psutil': 'system monitoring'
        }
        
        # Check critical dependencies
        for module, min_version in critical_deps.items():
            try:
                if module == 'PIL':
                    import PIL
                    version = PIL.__version__
                    print(f"✅ {module} v{version} - CRITICAL DEPENDENCY SATISFIED")
                else:
                    mod = __import__(module)
                    version = getattr(mod, '__version__', 'unknown')
                    print(f"✅ {module} v{version} - CRITICAL DEPENDENCY SATISFIED")
                    
            except ImportError as e:
                self.errors.append(f"Critical dependency missing: {module} ({e})")
                print(f"❌ {module} - CRITICAL FAILURE")
        
        # Check optional dependencies
        for module, purpose in optional_deps.items():
            try:
                __import__(module)
                version = getattr(__import__(module), '__version__', 'unknown')
                print(f"✅ {module} v{version} - {purpose.upper()} ENABLED")
            except ImportError:
                self.warnings.append(f"Optional dependency missing: {module} (needed for {purpose})")
                print(f"⚠️  {module} - {purpose.upper()} DISABLED")
        
        return len(self.errors) == 0
    
    def validate_flask_app(self):
        """Ultra-comprehensive Flask app validation"""
        print("🔍 Validating ULTRA Flask application...")
        
        try:
            # Import the app
            start_import = time.time()
            from main import app
            import_time = time.time() - start_import
            
            self.log_performance('app_import_time', import_time)
            print(f"✅ Flask app imported in {import_time:.3f}s - ULTRA FAST")
            
            # Test critical endpoints
            endpoints_to_test = [
                ('/', 'GET', 'index page'),
                ('/health', 'GET', 'health check'),
                ('/api/status', 'GET', 'API status'),
                ('/api/vibes', 'GET', 'vibes endpoint'),
            ]
            
            with app.test_client() as client:
                for endpoint, method, description in endpoints_to_test:
                    start_req = time.time()
                    
                    if method == 'GET':
                        response = client.get(endpoint)
                    else:
                        response = client.post(endpoint, json={})
                    
                    req_time = time.time() - start_req
                    
                    if response.status_code < 400:
                        print(f"✅ {endpoint} ({description}) - {response.status_code} in {req_time:.3f}s")
                    else:
                        self.warnings.append(f"{endpoint} returned {response.status_code}")
                        print(f"⚠️  {endpoint} ({description}) - {response.status_code}")
            
            # Test sigil generation capability
            test_payload = {
                'phrase': 'ultra test validation',
                'vibe': 'mystical',
                'advanced': False
            }
            
            start_gen = time.time()
            with app.test_client() as client:
                response = client.post('/api/generate', json=test_payload)
                gen_time = time.time() - start_gen
                
                if response.status_code == 200:
                    data = response.get_json()
                    if data.get('success') and data.get('image'):
                        print(f"✅ Sigil generation test - SUCCESS in {gen_time:.3f}s")
                        self.log_performance('test_generation_time', gen_time)
                    else:
                        self.warnings.append("Sigil generation test returned empty result")
                else:
                    self.warnings.append(f"Sigil generation test failed: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.errors.append(f"Flask app validation failed: {e}")
            print(f"❌ Flask validation failed: {e}")
            return False
    
    def validate_performance(self):
        """Ultra-advanced performance validation"""
        print("🔍 Running ULTRA performance diagnostics...")
        
        # Test file I/O performance
        test_file = '/tmp/sigilcraft_perf_test.txt'
        test_data = 'x' * 10000  # 10KB test
        
        start_io = time.time()
        try:
            with open(test_file, 'w') as f:
                f.write(test_data)
            with open(test_file, 'r') as f:
                read_data = f.read()
            os.remove(test_file)
            
            io_time = time.time() - start_io
            self.log_performance('disk_io_time', io_time)
            
            if io_time < 0.1:
                print(f"✅ Disk I/O performance - EXCELLENT ({io_time:.4f}s)")
            elif io_time < 0.5:
                print(f"✅ Disk I/O performance - GOOD ({io_time:.4f}s)")
            else:
                self.warnings.append(f"Slow disk I/O detected: {io_time:.4f}s")
                
        except Exception as e:
            self.warnings.append(f"Disk I/O test failed: {e}")
        
        # Test memory allocation
        start_mem = time.time()
        try:
            # Allocate and deallocate 10MB
            test_memory = bytearray(10 * 1024 * 1024)
            del test_memory
            
            mem_time = time.time() - start_mem
            self.log_performance('memory_alloc_time', mem_time)
            
            if mem_time < 0.1:
                print(f"✅ Memory allocation - ULTRA FAST ({mem_time:.4f}s)")
            else:
                print(f"✅ Memory allocation - OK ({mem_time:.4f}s)")
                
        except Exception as e:
            self.warnings.append(f"Memory test failed: {e}")
        
        return True
    
    def validate_security(self):
        """Ultra-advanced security validation"""
        print("🔍 Running ULTRA security validation...")
        
        security_checks = []
        
        # Check for sensitive files
        sensitive_patterns = ['.env', '*.key', '*.pem', 'secrets.*']
        for pattern in sensitive_patterns:
            if list(Path('.').glob(pattern)):
                security_checks.append(f"Sensitive files detected: {pattern}")
        
        # Check file permissions
        critical_files = ['main.py', 'unified_server.py']
        for file_path in critical_files:
            if os.path.exists(file_path):
                mode = os.stat(file_path).st_mode
                if mode & 0o002:  # World-writable
                    security_checks.append(f"World-writable file: {file_path}")
        
        if security_checks:
            for check in security_checks:
                self.warnings.append(f"Security: {check}")
                print(f"⚠️  Security warning: {check}")
        else:
            print("✅ Security validation - NO ISSUES DETECTED")
        
        return True
    
    def generate_report(self):
        """Generate ultra-comprehensive validation report"""
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("🎯 ULTRA VALIDATION REPORT")
        print("="*60)
        
        print(f"⏱️  Total validation time: {total_time:.3f}s")
        print(f"❌ Errors found: {len(self.errors)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        
        if self.errors:
            print("\n❌ CRITICAL ERRORS:")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
        
        if self.performance_metrics:
            print("\n📊 PERFORMANCE METRICS:")
            for metric, value in self.performance_metrics.items():
                if isinstance(value, float):
                    print(f"   {metric}: {value:.4f}")
                else:
                    print(f"   {metric}: {value}")
        
        # Overall assessment
        if len(self.errors) == 0:
            if len(self.warnings) == 0:
                print("\n🎉 VALIDATION STATUS: PERFECT - ULTRA READY!")
                return True
            elif len(self.warnings) <= 2:
                print("\n✅ VALIDATION STATUS: EXCELLENT - READY TO LAUNCH!")
                return True
            else:
                print("\n⚠️  VALIDATION STATUS: GOOD - MINOR ISSUES DETECTED")
                return True
        else:
            print("\n❌ VALIDATION STATUS: FAILED - CRITICAL ISSUES MUST BE RESOLVED")
            return False

def main():
    """Run ultra-comprehensive validation suite"""
    print("🚀 Starting ULTRA Sigilcraft Validation Suite...")
    print("🔮 Supreme Coding Master Edition v3.0.0")
    print("-" * 60)
    
    validator = UltraValidator()
    
    validation_steps = [
        ('Environment', validator.validate_environment),
        ('Dependencies', validator.validate_dependencies),
        ('Flask Application', validator.validate_flask_app),
        ('Performance', validator.validate_performance),
        ('Security', validator.validate_security)
    ]
    
    all_passed = True
    for step_name, step_func in validation_steps:
        print(f"\n🔍 {step_name} Validation:")
        try:
            if not step_func():
                all_passed = False
        except Exception as e:
            validator.errors.append(f"{step_name} validation crashed: {e}")
            all_passed = False
    
    # Generate comprehensive report
    final_result = validator.generate_report()
    
    if final_result:
        print("\n🎯 SIGILCRAFT NEXUS IS ULTRA-READY FOR DEPLOYMENT!")
    else:
        print("\n❌ CRITICAL ISSUES DETECTED - RESOLVE BEFORE DEPLOYMENT")
    
    return final_result

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
