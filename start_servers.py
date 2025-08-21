
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
import json

def monitor_process(process, name):
    """Monitor a process and log its output"""
    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[{name}] {line.strip()}")
            else:
                break
    except Exception as e:
        print(f"[{name}] Monitor error: {e}")
    finally:
        if process.stdout:
            process.stdout.close()

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
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', port))
            return result == 0
    except:
        return False

def kill_process_on_port(port):
    """Kill any process using the specified port"""
    try:
        if os.name == 'posix':  # Linux/Unix
            subprocess.run(['fuser', '-k', f'{port}/tcp'], capture_output=True, timeout=5)
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
    
    # Set environment variables for Flask
    env = os.environ.copy()
    env['FLASK_ENV'] = 'production'
    env['PYTHONUNBUFFERED'] = '1'
    
    flask_process = subprocess.Popen([
        sys.executable, 'main.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, env=env)
    
    return flask_process

def start_node_server():
    """Start the Node.js server"""
    print("🟢 Starting Node.js server...")
    
    # Kill any existing Node processes on port 5000
    if is_port_in_use(5000):
        print("🔄 Clearing port 5000...")
        kill_process_on_port(5000)
        time.sleep(2)
    
    # Check if node_modules exists
    if not os.path.exists('node_modules'):
        print("📦 Installing Node.js dependencies...")
        subprocess.run(['npm', 'install'], check=True)
    
    # Set environment variables for Node.js
    env = os.environ.copy()
    if not env.get('PRO_KEY'):
        env['PRO_KEY'] = 'changeme_super_secret'
    
    node_process = subprocess.Popen([
        'node', 'server.js'
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, env=env)
    
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
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        with open('.env', 'w') as f:
            f.write('PRO_KEY=changeme_super_secret\n')
            f.write('NODE_ENV=production\n')
    
    # Start Flask server first
    flask_process = start_flask_server()
    
    # Wait for Flask to start
    print("⏳ Waiting for Flask server to initialize...")
    flask_ready = False
    for attempt in range(30):  # Wait up to 30 seconds
        time.sleep(1)
        for port in range(5001, 5010):
            if is_port_in_use(port):
                print(f"✅ Flask server detected on port {port}")
                flask_ready = True
                break
        if flask_ready:
            break
    
    if not flask_ready:
        print("❌ Flask server failed to start")
        # Print Flask output for debugging
        if flask_process.poll() is not None:
            output, _ = flask_process.communicate(timeout=5)
            print(f"Flask output: {output}")
        return 1
    
    # Start Node.js server
    node_process = start_node_server()
    
    # Wait for Node.js to start
    print("⏳ Waiting for Node.js server to initialize...")
    node_ready = False
    for attempt in range(20):  # Wait up to 20 seconds
        time.sleep(1)
        if is_port_in_use(5000):
            print("✅ Node.js server detected on port 5000")
            node_ready = True
            break
    
    if not node_ready:
        print("❌ Node.js server failed to start")
        # Print Node output for debugging
        if node_process.poll() is not None:
            try:
                output, _ = node_process.communicate(timeout=5)
                print(f"Node.js output: {output}")
            except:
                pass
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
    
    # Monitor both processes in the background
    flask_thread = Thread(target=monitor_process, args=(flask_process, "FLASK"))
    node_thread = Thread(target=monitor_process, args=(node_process, "NODE"))
    
    flask_thread.daemon = True
    node_thread.daemon = True
    
    flask_thread.start()
    node_thread.start()
    
    # Keep main thread alive and monitor process health
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
