
#!/usr/bin/env python3
"""
UNIFIED SIGILCRAFT SERVER FOR REPLIT
Production-ready Flask backend with WSGI server
"""

import os
import sys
import signal
from main import app as flask_app
from flask import send_from_directory

def signal_handler(signum, frame):
    """Handle graceful shutdown"""
    print(f"\n🛑 Received signal {signum}. Shutting down gracefully...")
    sys.exit(0)

# Add static file serving routes
@flask_app.route('/')
def serve_index():
    """Serve the main index.html"""
    return send_from_directory('public', 'index.html')

@flask_app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from public directory"""
    try:
        return send_from_directory('public', filename)
    except:
        # If file not found, serve index.html for client-side routing
        return send_from_directory('public', 'index.html')

if __name__ == '__main__':
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("🔮 Starting Unified Sigilcraft Server for Replit...")

    # Get port from Replit environment - this is critical for deployment
    port = int(os.environ.get('PORT', 5000))

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
