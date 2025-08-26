#!/usr/bin/env python3
"""
UNIFIED SIGILCRAFT SERVER FOR REPLIT
Single-process Flask backend bound to Replit's PORT
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

    try:
        # Start Flask app with proper Replit configuration
        flask_app.run(
            host='0.0.0.0',  # Required for Replit external access
            port=port,       # Use Replit's PORT environment variable
            debug=False,     # Disable debug in production
            threaded=True,   # Enable threading for better performance
            use_reloader=False  # Disable reloader to prevent conflicts
        )
    except KeyboardInterrupt:
        print("\n🛑 Server shutdown gracefully")
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)