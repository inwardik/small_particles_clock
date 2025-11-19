#!/usr/bin/env python3
"""
Simple HTTP server that serves data from data.json file.
The server returns objects from the list sequentially, cycling when it reaches the end.
"""

import json
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Global index to track current position in data array
current_index = 0
data_cache = []
reload_flag = False


def load_data():
    """Load data from data.json file"""
    global data_cache
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data_cache = json.load(f)
            print(f"Loaded {len(data_cache)} items from data.json")
            return True
    except FileNotFoundError:
        print("Error: data.json file not found")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in data.json - {e}")
        return False


def get_next_item():
    """Get next item from data array, cycling when reaching the end"""
    global current_index

    if not data_cache:
        return None

    item = data_cache[current_index]
    current_index = (current_index + 1) % len(data_cache)

    return item


class DataHandler(BaseHTTPRequestHandler):
    """HTTP request handler"""

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)

        # Enable CORS for frontend access
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        if parsed_path.path == '/data':
            # Return next item from data array
            item = get_next_item()
            if item:
                response = json.dumps(item, ensure_ascii=False)
                self.wfile.write(response.encode('utf-8'))
            else:
                error = json.dumps({"error": "No data available"})
                self.wfile.write(error.encode('utf-8'))
        else:
            # Unknown endpoint
            error = json.dumps({"error": "Unknown endpoint"})
            self.wfile.write(error.encode('utf-8'))

    def log_message(self, format, *args):
        """Override to provide custom logging"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def keyboard_monitor():
    """Monitor keyboard input for reload command"""
    global reload_flag
    while True:
        try:
            key = sys.stdin.read(1)
            if key.lower() == 'r':
                print("\n[RELOAD] Reloading server...")
                reload_flag = True
                break
        except:
            break


def run_server(port=8000):
    """Start HTTP server"""
    global reload_flag

    while True:
        reload_flag = False

        # Load data before starting server
        if not load_data():
            print("Failed to load data. Please ensure data.json exists.")
            return

        server_address = ('', port)
        httpd = HTTPServer(server_address, DataHandler)

        print(f"Server started on http://localhost:{port}")
        print(f"Endpoint: http://localhost:{port}/data")
        print("Press Ctrl+C to stop the server, or 'r' to reload")

        # Start keyboard monitor thread
        monitor_thread = threading.Thread(target=keyboard_monitor, daemon=True)
        monitor_thread.start()

        try:
            # Check reload flag periodically
            while not reload_flag:
                httpd.handle_request()
        except KeyboardInterrupt:
            print("\nServer stopped")
            break

        if reload_flag:
            print("Reloading data and restarting server...")
            httpd.server_close()
            continue
        else:
            httpd.server_close()
            break


if __name__ == '__main__':
    # You can change the port here if needed
    PORT = 8000
    run_server(PORT)
