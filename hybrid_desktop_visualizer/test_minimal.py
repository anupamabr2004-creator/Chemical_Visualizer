"""
QUICK TEST: Try this script to verify buttons work
Run: python test_minimal.py
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal
import requests

class MinimalTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimal Button Test")
        self.setGeometry(100, 100, 400, 200)
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Username (try 'testuser'):"))
        self.username = QLineEdit()
        layout.addWidget(self.username)
        
        layout.addWidget(QLabel("Password (try 'testpass123'):"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        
        btn = QPushButton("Click Me - Should Call API")
        btn.clicked.connect(self.on_click)
        layout.addWidget(btn)
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def on_click(self):
        print("\n" + "="*50)
        print("BUTTON CLICKED!")
        print("="*50)
        
        username = self.username.text()
        password = self.password.text()
        
        print(f"Username: '{username}'")
        print(f"Password: '{password}'")
        
        if not username or not password:
            print("ERROR: Fields empty")
            return
        
        print("Calling API...")
        try:
            response = requests.post(
                "http://localhost:8000/api/auth/login/",
                json={"username": username, "password": password},
                timeout=5
            )
            print(f"API Response: {response.status_code}")
            print(f"Response text: {response.text[:200]}")
            
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Login worked!")
            else:
                QMessageBox.warning(self, "Failed", f"Login failed: {response.status_code}")
        except Exception as e:
            print(f"API ERROR: {e}")
            QMessageBox.critical(self, "Error", f"Error: {e}")

if __name__ == "__main__":
    print("\nStarting minimal test...")
    print("1. Make sure backend is running: python manage.py runserver")
    print("2. Enter 'testuser' and 'testpass123'")
    print("3. Click the button")
    print("4. Check the console output\n")
    
    app = QApplication(sys.argv)
    window = MinimalTest()
    window.show()
    sys.exit(app.exec_())
