#!/usr/bin/env python
"""Simple test of auth window."""
import sys
import os

# Add subdirectory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hybrid_desktop_visualizer'))

from PyQt5.QtWidgets import QApplication
from api_client import APIClient
from auth_window import AuthWindow

def test_auth():
    app = QApplication(sys.argv)
    
    print("=" * 70)
    print("Testing AuthWindow")
    print("=" * 70)
    
    # Test API client
    api_client = APIClient("http://localhost:8000/api")
    print(f"API Client created: {api_client}")
    print(f"API Base URL: {api_client.base_url}")
    
    # Create auth window
    print("\nCreating AuthWindow...")
    auth_window = AuthWindow(api_client)
    
    # Connect signal
    def on_login(token, username):
        print(f"\n[SUCCESS] Login received: token={token[:20]}..., username={username}")
        auth_window.close()
        app.quit()
    
    auth_window.login_success.connect(on_login)
    
    print("Showing window...")
    auth_window.show()
    
    # Auto-test: simulate login click after 2 seconds
    def auto_test():
        print("\n[AUTO-TEST] Simulating login with test credentials...")
        auth_window.login_username.setText("testuser")
        auth_window.login_password.setText("testpass123")
        auth_window._handle_login()
    
    from PyQt5.QtCore import QTimer
    QTimer.singleShot(2000, auto_test)
    
    # Exit after 10 seconds if not already done
    QTimer.singleShot(10000, lambda: app.quit())
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_auth()
