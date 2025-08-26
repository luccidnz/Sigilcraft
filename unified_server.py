
#!/usr/bin/env python3
"""
UNIFIED SIGILCRAFT SERVER FOR REPLIT
Production-ready Flask backend with WSGI server
"""

import os
import sys
import signal
from main import app as flask_app

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

    print(f"🎯 Server running on 0.0.0.0:{port}")
    print("🎨 Ultra-revolutionary sigil generation ready!")
    print(f"🌍 Access your app at: https://your-repl-name.replit.app")

    # Check if we're in a production environment (deployed)
    is_production = os.environ.get('REPLIT_DEPLOYMENT') == 'true'

    if is_production:
        print("🚀 Running in production mode with Gunicorn...")
        try:
            import gunicorn.app.wsgiapp as wsgi
            # Configure Gunicorn for production
            sys.argv = [
                'gunicorn',
                '--bind', f'0.0.0.0:{port}',
                '--workers', '2',
                '--worker-class', 'sync',
                '--timeout', '30',
                '--max-requests', '1000',
                '--max-requests-jitter', '100',
                '--preload',
                '--log-level', 'info',
                'main:app'
            ]
            wsgi.run()
        except ImportError:
            print("⚠️  Gunicorn not available, falling back to Flask dev server")
            flask_app.run(
                host='0.0.0.0',
                port=port,
                debug=False,
                threaded=True,
                use_reloader=False
            )
    else:
        print("🔧 Running in development mode...")
        try:
            # Start Flask app with proper Replit configuration
            flask_app.run(
                host='0.0.0.0',  # Required for Replit external access
                port=port,       # Use Replit's PORT environment variable
                debug=False,     # Keep debug disabled for cleaner logs
                threaded=True,   # Enable threading for better performance
                use_reloader=False  # Disable reloader to prevent conflicts
            )
        except KeyboardInterrupt:
            print("\n🛑 Server shutdown gracefully")
        except Exception as e:
            print(f"❌ Server startup failed: {e}")
            sys.exit(1)
