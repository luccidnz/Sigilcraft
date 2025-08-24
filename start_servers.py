#!/usr/bin/env python3
"""
Coordinated startup script for Sigilcraft
Starts both Node.js and Flask servers with proper coordination
"""

import subprocess
import sys
import time
import requests
import threading
import signal
import os
import socket
from pathlib import Path

# Server configuration
NODE_PORT = 5000
FLASK_PORTS = [5001, 5002, 5003, 5004, 5005]  # Try multiple ports for Flask
MAX_STARTUP_TIME = 60  # seconds

class ServerManager:
    def __init__(self):
        self.node_process = None
        self.flask_process = None
        self.flask_port = None
        self.running = True

    def signal_handler(self, signum, frame):
        print("\n🛑 Shutdown signal received. Stopping servers...")
        self.running = False
        self.stop_servers()
        sys.exit(0)

    def find_available_port(self, start_port, port_list=None):
        """Find an available port from the list or starting from start_port"""
        if port_list:
            for port in port_list:
                if self.is_port_available(port):
                    return port
        else:
            for port in range(start_port, start_port + 10):
                if self.is_port_available(port):
                    return port
        return None

    def is_port_available(self, port):
        """Check if a port is available"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('0.0.0.0', port))
                return True
        except OSError:
            return False

    def stop_servers(self):
        """Stop all server processes"""
        if self.flask_process:
            try:
                self.flask_process.terminate()
                self.flask_process.wait(timeout=5)
                print("✅ Flask server stopped")
            except:
                try:
                    self.flask_process.kill()
                except:
                    pass

        if self.node_process:
            try:
                self.node_process.terminate()
                self.node_process.wait(timeout=5)
                print("✅ Node.js server stopped")
            except:
                try:
                    self.node_process.kill()
                except:
                    pass

    def wait_for_server(self, url, timeout=30, server_name="Server"):
        """Wait for a server to become available"""
        print(f"⏳ Waiting for {server_name} at {url}...")
        start_time = time.time()

        while time.time() - start_time < timeout and self.running:
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    print(f"✅ {server_name} is ready!")
                    return True
                elif response.status_code in [404, 500]:
                    # Server is responding but may need more time
                    print(f"🔄 {server_name} responding with {response.status_code}, waiting...")
            except requests.exceptions.RequestException as e:
                if "Connection refused" not in str(e):
                    print(f"🔄 {server_name} connection attempt: {e}")
            time.sleep(2)

        print(f"❌ {server_name} failed to start within {timeout} seconds")
        return False

    def health_check_loop(self):
        """Continuously monitor server health"""
        while self.running:
            time.sleep(30)  # Check every 30 seconds

            if not self.running:
                break

            # Check Flask health
            if self.flask_port:
                try:
                    response = requests.get(f"http://127.0.0.1:{self.flask_port}/health", timeout=5)
                    if response.status_code != 200:
                        print(f"⚠️ Flask health check failed: {response.status_code}")
                except Exception as e:
                    print(f"⚠️ Flask health check error: {e}")

            # Check Node health
            try:
                response = requests.get(f"http://127.0.0.1:{NODE_PORT}/api/health", timeout=5)
                if response.status_code != 200:
                    print(f"⚠️ Node.js health check failed: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Node.js health check error: {e}")

    def start_flask_server(self):
        """Start the Flask server with better error handling"""
        print("🔥 Starting Flask server...")

        # Find available port
        self.flask_port = self.find_available_port(FLASK_PORTS[0], FLASK_PORTS)

        if not self.flask_port:
            print(f"❌ No available ports for Flask server in range {FLASK_PORTS}")
            return False

        print(f"🔥 Starting Flask server on port {self.flask_port}...")

        try:
            env = os.environ.copy()
            env['PORT'] = str(self.flask_port)
            env['PYTHONUNBUFFERED'] = '1'
            env['FLASK_ENV'] = 'production'

            # Ensure Python dependencies are available
            print("📦 Checking Python dependencies...")
            try:
                import flask, PIL, numpy
                print("✅ Core dependencies available")
            except ImportError as e:
                print(f"⚠️ Missing dependency: {e}")
                print("🔧 Installing missing dependencies...")
                subprocess.run([sys.executable, "-m", "pip", "install", "flask", "pillow", "numpy"],
                             check=True, capture_output=True)

            self.flask_process = subprocess.Popen(
                [sys.executable, "main.py"],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # Start output monitoring
            threading.Thread(
                target=self.monitor_flask_output,
                daemon=True
            ).start()

            # Wait for Flask to be ready with longer timeout
            flask_url = f"http://127.0.0.1:{self.flask_port}/health"
            if self.wait_for_server(flask_url, timeout=60, server_name="Flask"):
                print(f"✅ Flask server running on port {self.flask_port}")
                return True
            else:
                print("❌ Flask server failed to start")
                if self.flask_process:
                    self.flask_process.terminate()
                return False

        except Exception as e:
            print(f"❌ Error starting Flask server: {e}")
            if self.flask_process:
                try:
                    self.flask_process.terminate()
                except:
                    pass
            return False

    def start_node_server(self):
        """Start the Node.js server with better error handling"""
        print("🔥 Starting Node.js server...")

        if not os.path.exists("server.js"):
            print("❌ server.js not found. Please ensure the Node.js server file exists.")
            return False

        # Check if node_modules exists and install if not
        if not os.path.exists('node_modules'):
            print("📦 Installing Node.js dependencies...")
            try:
                subprocess.run(['npm', 'install'], check=True, capture_output=True)
                print("✅ Node.js dependencies installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install Node.js dependencies: {e}")
                print(f"Stderr: {e.stderr.decode()}")
                return False
            except FileNotFoundError:
                print("❌ npm command not found. Please ensure Node.js is installed and in your PATH.")
                return False

        try:
            env = os.environ.copy()
            env['NODE_ENV'] = 'production'
            if not env.get('PRO_KEY'):
                env['PRO_KEY'] = 'changeme_super_secret'

            self.node_process = subprocess.Popen(
                ['node', 'server.js'],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # Start output monitoring
            threading.Thread(
                target=self.monitor_node_output,
                daemon=True
            ).start()

            # Wait for Node.js to be ready
            node_url = f"http://127.0.0.1:{NODE_PORT}/api/health"
            if self.wait_for_server(node_url, timeout=60, server_name="Node.js"):
                print(f"✅ Node.js server running on port {NODE_PORT}")
                return True
            else:
                print("❌ Node.js server failed to start")
                if self.node_process:
                    self.node_process.terminate()
                return False

        except Exception as e:
            print(f"❌ Error starting Node.js server: {e}")
            if self.node_process:
                try:
                    self.node_process.terminate()
                except:
                    pass
            return False

    def monitor_flask_output(self):
        """Monitor and print Flask server output"""
        if not self.flask_process:
            return
        while self.running:
            try:
                line = self.flask_process.stdout.readline()
                if not line and self.flask_process.poll() is not None:
                    break
                if line:
                    print(f"[Flask] {line.strip()}")
            except Exception as e:
                print(f"[Flask] Error reading output: {e}")
                break

    def monitor_node_output(self):
        """Monitor and print Node.js server output"""
        if not self.node_process:
            return
        while self.running:
            try:
                line = self.node_process.stdout.readline()
                if not line and self.node_process.poll() is not None:
                    break
                if line:
                    print(f"[Node] {line.strip()}")
            except Exception as e:
                print(f"[Node] Error reading output: {e}")
                break

def main():
    """Main startup coordinator with comprehensive error handling"""
    print("🔮 SIGILCRAFT SERVER COORDINATOR")
    print("=" * 50)

    manager = ServerManager()

    # Set up signal handlers
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)

    try:
        # Check system requirements
        print("🔍 Checking system requirements...")

        # Check if Node.js is available
        try:
            subprocess.run(["node", "--version"], check=True, capture_output=True)
            print("✅ Node.js is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Node.js not found. Please install Node.js")
            return 1

        # Check if Python is available
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is available")

        # Start Flask server first
        print("\n📊 Starting backend services...")
        if not manager.start_flask_server():
            print("❌ Failed to start Flask server")
            return 1

        # Start Node.js server
        print("\n🌐 Starting frontend services...")
        if not manager.start_node_server():
            print("❌ Failed to start Node.js server")
            manager.stop_servers()
            return 1

        # Start health monitoring
        health_thread = threading.Thread(target=manager.health_check_loop, daemon=True)
        health_thread.start()

        print("\n🎉 SIGILCRAFT IS READY!")
        print("=" * 50)
        print(f"🌐 Frontend: http://localhost:{NODE_PORT}")
        print(f"🔥 Backend: http://localhost:{manager.flask_port}")
        print("🔮 Ready to generate quantum sigils!")
        print("\n💡 Press Ctrl+C to stop servers")
        print("🔍 Health monitoring active...")

        # Keep the main thread alive
        try:
            while manager.running:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.signal_handler(signal.SIGINT, None)

    except Exception as e:
        print(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
        manager.stop_servers()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())