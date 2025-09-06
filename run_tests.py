
#!/usr/bin/env python3
"""
Comprehensive test runner for Sigilcraft
"""
import os
import sys
import subprocess

def run_tests():
    """Run all test suites"""
    print("🧪 Running Sigilcraft test suite...")
    
    # Run pytest with verbose output
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '-v', 
            '--tb=short'
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print(f"❌ Tests failed with return code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
