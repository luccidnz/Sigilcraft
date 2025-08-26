
#!/usr/bin/env python3
"""
UNIFIED SIGILCRAFT SERVER FOR REPLIT
Runs Flask API backend with proper port binding
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

# Import the Flask app
from main import app as flask_app

def start_express_server():
    """Start Express server in background"""
    try:
        print("🚀 Starting Express frontend server...")
        process = subprocess.Popen(
            ['node', 'server.js'],
            env={**os.environ, 'FLASK_BACKEND': 'true'},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Log Express output
        for line in process.stdout:
            print(f"[EXPRESS] {line.strip()}")
            
    except Exception as e:
        print(f"❌ Failed to start Express server: {e}")

def signal_handler(signum, frame):
    """Handle graceful shutdown"""
    print(f"\n🛑 Received signal {signum}. Shutting down gracefully...")
    sys.exit(0)

if __name__ == '__main__':
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🔮 Starting Unified Sigilcraft Server for Replit...")
    
    # Get port from Replit environment
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🎯 Server will run on port {port}")
    print("🎨 Ultra-revolutionary sigil generation ready!")
    
    try:
        # Start Flask app directly (single process mode)
        flask_app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Server shutdown gracefully")
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)
