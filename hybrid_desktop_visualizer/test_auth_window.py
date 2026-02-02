#!/usr/bin/env python
"""Test auth window with actual API calls."""
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
    QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
import requests

class APIClient:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def login(self, username, password):
        try:
            print(f"[API] Calling login with username={username}")
            response = self.session.post(
                f"{self.base_url}/auth/login/",
                json={"username": username, "password": password}
            )
            print(f"[API] Response status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                token = data.get("access")
                if token:
                    return True, "Login successful", token
                return False, "No token in response", None
            else:
                return False, f"Login failed: {response.text}", None
        except Exception as e:
            return False, f"Error: {str(e)}", None

class TestAuthWindow(QMainWindow):
    login_success = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        
        self.setWindowTitle("Test Auth Window")
        self.setGeometry(100, 100, 500, 400)
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_field = QLineEdit()
        self.username_field.setText("testuser")  # Pre-filled for testing
        layout.addWidget(self.username_field)
        
        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setText("testpass123")  # Pre-filled for testing
        layout.addWidget(self.password_field)
        
        # Login button
        self.login_btn = QPushButton("Login")
        print(f"[INIT] Creating login button: {self.login_btn}")
        self.login_btn.clicked.connect(self._handle_login)
        print(f"[INIT] Connected button to handler")
        layout.addWidget(self.login_btn)
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def _handle_login(self):
        print("\n" + "="*60)
        print("[HANDLER] _handle_login() CALLED!")
        print("="*60)
        
        username = self.username_field.text().strip()
        password = self.password_field.text().strip()
        
        print(f"[HANDLER] Username: '{username}'")
        print(f"[HANDLER] Password: '{password}'")
        
        if not username or not password:
            print("[HANDLER] Fields are empty!")
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        print("[HANDLER] Fields OK, calling API...")
        success, message, token = self.api_client.login(username, password)
        
        print(f"[HANDLER] API Result: success={success}, message={message}")
        
        if success:
            print("[HANDLER] Login successful! Emitting signal...")
            self.login_success.emit(token, username)
            QMessageBox.information(self, "Success", "Login successful!")
            self.close()
        else:
            print("[HANDLER] Login failed!")
            QMessageBox.critical(self, "Login Failed", message)

if __name__ == "__main__":
    print("[MAIN] Starting application...")
    app = QApplication(sys.argv)
    window = TestAuthWindow()
    window.show()
    print("[MAIN] Window shown. Click the Login button to test...")
    sys.exit(app.exec_())
