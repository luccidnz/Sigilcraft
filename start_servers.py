
#!/usr/bin/env python3
"""
Server startup management script for Sigilcraft
Handles proper startup sequence and port management
"""

import subprocess
import time
import sys
import signal
import os
import socket
from threading import Thread

def find_available_port(start_port=5001):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + 10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    return None

def is_port_in_use(port):
    """Check if a port is already in use"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port))
            return False
    except OSError:
        return True

def kill_process_on_port(port):
    """Kill any process using the specified port"""
    try:
        if os.name == 'posix':  # Linux/Unix
            subprocess.run(['pkill', '-f', f':{port}'], capture_output=True)
            time.sleep(1)
    except:
        pass

def start_flask_server():
    """Start the Flask server"""
    print("🐍 Starting Flask server...")
    
    # Kill any existing Flask processes
    for port in range(5001, 5010):
        if is_port_in_use(port):
            print(f"🔄 Clearing port {port}...")
            kill_process_on_port(port)
    
    time.sleep(2)  # Wait for cleanup
    
    flask_process = subprocess.Popen([
        sys.executable, 'main.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    
    return flask_process

def start_node_server():
    """Start the Node.js server"""
    print("🟢 Starting Node.js server...")
    
    # Kill any existing Node processes on port 5000
    if is_port_in_use(5000):
        print("🔄 Clearing port 5000...")
        kill_process_on_port(5000)
        time.sleep(2)
    
    node_process = subprocess.Popen([
        'node', 'server.js'
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    
    return node_process

def monitor_process(process, name, log_lines=10):
    """Monitor a process and print its output"""
    lines = []
    while process.poll() is None:
        line = process.stdout.readline()
        if line:
            print(f"[{name}] {line.strip()}")
            lines.append(line)
            if len(lines) > log_lines:
                lines.pop(0)
        time.sleep(0.1)
    
    # Print remaining output
    remaining = process.stdout.read()
    if remaining:
        for line in remaining.split('\n'):
            if line.strip():
                print(f"[{name}] {line.strip()}")

def main():
    """Main startup function"""
    print("🚀 Starting Sigilcraft servers...")
    print("=" * 50)
    
    # Start Flask server first
    flask_process = start_flask_server()
    
    # Wait for Flask to start
    print("⏳ Waiting for Flask server to initialize...")
    time.sleep(5)
    
    # Check Flask status
    flask_running = False
    for port in range(5001, 5010):
        if is_port_in_use(port):
            print(f"✅ Flask server detected on port {port}")
            flask_running = True
            break
    
    if not flask_running:
        print("❌ Flask server failed to start")
        # Print Flask output for debugging
        if flask_process.poll() is not None:
            output = flask_process.stdout.read()
            print(f"Flask output: {output}")
        return 1
    
    # Start Node.js server
    node_process = start_node_server()
    
    # Wait for Node.js to start
    print("⏳ Waiting for Node.js server to initialize...")
    time.sleep(3)
    
    if is_port_in_use(5000):
        print("✅ Node.js server detected on port 5000")
    else:
        print("❌ Node.js server failed to start")
        return 1
    
    print("=" * 50)
    print("🎉 Both servers are running!")
    print("🌐 Access your app at: http://localhost:5000")
    print("🔧 Flask API available on port 5001+")
    print("=" * 50)
    print("Press Ctrl+C to stop all servers")
    
    # Set up signal handlers for clean shutdown
    def signal_handler(signum, frame):
        print("\n🛑 Shutting down servers...")
        flask_process.terminate()
        node_process.terminate()
        
        # Wait for graceful shutdown
        time.sleep(2)
        
        # Force kill if needed
        if flask_process.poll() is None:
            flask_process.kill()
        if node_process.poll() is None:
            node_process.kill()
        
        print("✅ All servers stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Monitor both processes
    flask_thread = Thread(target=monitor_process, args=(flask_process, "FLASK"))
    node_thread = Thread(target=monitor_process, args=(node_process, "NODE"))
    
    flask_thread.daemon = True
    node_thread.daemon = True
    
    flask_thread.start()
    node_thread.start()
    
    # Keep main thread alive
    try:
        while True:
            if flask_process.poll() is not None:
                print("❌ Flask server crashed!")
                return 1
            if node_process.poll() is not None:
                print("❌ Node.js server crashed!")
                return 1
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    sys.exit(main())
