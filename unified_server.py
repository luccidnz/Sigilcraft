
#!/usr/bin/env python3
"""
UNIFIED SIGILCRAFT SERVER FOR REPLIT
Production-ready Flask backend with WSGI server
"""

import os
import sys
import signal

# Import the Flask app
try:
    from main import app as flask_app
    print("✅ Flask app imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Flask app: {e}")
    sys.exit(1)

def signal_handler(signum, frame):
    """Handle graceful shutdown"""
    print(f"\n🛑 Received signal {signum}. Shutting down gracefully...")
    sys.exit(0)

if __name__ == '__main__':
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("🔮 Starting Unified Sigilcraft Server for Replit...")

    # Get port from Replit environment - this is critical for deployment
    port = int(os.environ.get('PORT', 5000))
    
    # Ensure public directory exists
    if not os.path.exists('public'):
        print("❌ Public directory not found!")
        sys.exit(1)

    print(f"🎯 Server running on 0.0.0.0:{port}")
    print("🎨 Ultra-revolutionary sigil generation ready!")
    print(f"🌍 Access your app at: https://your-repl-name.replit.app")

    # Always try to use Gunicorn for production-ready serving
    print("🚀 Attempting to run with production WSGI server...")
    
    try:
        import gunicorn.app.wsgiapp as wsgi
        print("✅ Gunicorn available - using production WSGI server")
        
        # Configure Gunicorn for optimal Replit performance
        sys.argv = [
            'gunicorn',
            '--bind', f'0.0.0.0:{port}',
            '--workers', '1',  # Single worker for Replit's resource limits
            '--worker-class', 'sync',
            '--timeout', '30',
            '--max-requests', '1000',
            '--max-requests-jitter', '100',
            '--preload',
            '--log-level', 'info',
            '--access-logfile', '-',
            '--error-logfile', '-',
            'main:app'
        ]
        wsgi.run()
        
    except ImportError:
        print("⚠️  Gunicorn not available - installing and retrying...")
        
        # Try to install Gunicorn
        try:
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'gunicorn'])
            print("✅ Gunicorn installed successfully")
            
            # Retry with Gunicorn
            import gunicorn.app.wsgiapp as wsgi
            sys.argv = [
                'gunicorn',
                '--bind', f'0.0.0.0:{port}',
                '--workers', '1',
                '--worker-class', 'sync',
                '--timeout', '30',
                '--max-requests', '1000',
                '--max-requests-jitter', '100',
                '--preload',
                '--log-level', 'info',
                '--access-logfile', '-',
                '--error-logfile', '-',
                'main:app'
            ]
            wsgi.run()
            
        except Exception as install_error:
            print(f"❌ Failed to install Gunicorn: {install_error}")
            print("🔧 Falling back to Flask development server...")
            
            try:
                # Fallback to Flask with production-like settings
                flask_app.run(
                    host='0.0.0.0',  # Required for Replit external access
                    port=port,       # Use Replit's PORT environment variable
                    debug=False,     # Keep debug disabled
                    threaded=True,   # Enable threading for better performance
                    use_reloader=False  # Disable reloader to prevent conflicts
                )
            except KeyboardInterrupt:
                print("\n🛑 Server shutdown gracefully")
            except Exception as e:
                print(f"❌ Server startup failed: {e}")
                sys.exit(1)
