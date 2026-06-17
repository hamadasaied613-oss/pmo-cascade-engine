#!/usr/bin/env python3
"""
PMO CASCADE Sovereign Engine — Standalone Desktop App
PyWebView wrapper with built-in FastAPI server
"""
import sys, os, threading, time, webview
from pathlib import Path

# Add current dir to path
sys.path.insert(0, str(Path(__file__).parent))

def start_server():
    """Start FastAPI server in background thread"""
    import uvicorn
    from SOVEREIGN_SERVER import app
    uvicorn.run(app, host="127.0.0.1", port=9000, log_level="error")

class AppAPI:
    """JavaScript API exposed to the webview"""
    def __init__(self, window):
        self.window = window

    def minimize(self):
        self.window.minimize()

    def maximize(self):
        if self.window.maximized:
            self.window.restore()
        else:
            self.window.maximize()

    def close(self):
        self.window.destroy()

    def get_version(self):
        return "2.0.0"

    def get_platform(self):
        return sys.platform

def main():
    # Start server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Wait for server to be ready
    time.sleep(2)

    # Create window
    api = AppAPI(None)
    window = webview.create_window(
        title="PMO CASCADE Sovereign Engine",
        url="http://127.0.0.1:9000",
        width=1400,
        height=900,
        min_size=(1024, 700),
        resizable=True,
        text_select=True,
        js_api=api,
    )
    api.window = window

    # Start webview (blocks until closed)
    webview.start(debug=False)

if __name__ == "__main__":
    main()
