
#!/usr/bin/env python3
"""
Startup validator for Sigilcraft
Ensures all components are working before full launch
"""

import sys
import os
import importlib.util

def validate_environment():
    """Validate the environment setup"""
    print("🔍 Validating environment...")
    
    # Check if public directory exists
    if not os.path.exists('public'):
        print("❌ Public directory missing!")
        return False
    
    # Check if required files exist
    required_files = ['public/index.html', 'public/style.css', 'public/main.js']
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Required file missing: {file_path}")
            return False
    
    print("✅ Environment validation passed")
    return True

def validate_dependencies():
    """Validate Python dependencies"""
    print("🔍 Validating dependencies...")
    
    required_modules = ['flask', 'flask_cors']
    optional_modules = ['PIL']
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} available")
        except ImportError:
            print(f"❌ Required module missing: {module}")
            return False
    
    for module in optional_modules:
        try:
            __import__(module)
            print(f"✅ {module} available")
        except ImportError:
            print(f"⚠️  Optional module missing: {module} (fallback will be used)")
    
    print("✅ Dependency validation passed")
    return True

def validate_flask_app():
    """Validate Flask app can be imported"""
    print("🔍 Validating Flask app...")
    
    try:
        from main import app
        print("✅ Flask app imported successfully")
        
        # Test basic route
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"⚠️  Health endpoint returned {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Flask app validation failed: {e}")
        return False

def main():
    """Run all validations"""
    print("🚀 Starting Sigilcraft validation...")
    
    validations = [
        validate_environment,
        validate_dependencies,
        validate_flask_app
    ]
    
    for validation in validations:
        if not validation():
            print("❌ Validation failed!")
            sys.exit(1)
    
    print("🎉 All validations passed! Sigilcraft is ready to launch!")
    return True

if __name__ == "__main__":
    main()
