#!/usr/bin/env python
"""Simple button click test."""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt

class SimpleTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Test")
        self.setGeometry(100, 100, 400, 300)
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Username:"))
        self.username = QLineEdit()
        layout.addWidget(self.username)
        
        layout.addWidget(QLabel("Password:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        
        # Create button with debug
        self.btn = QPushButton("Test Button")
        print(f"Button created: {self.btn}")
        print(f"Button handler: {self._on_click}")
        
        # Try different connection methods
        self.btn.clicked.connect(self._on_click)
        print("Button connected with clicked.connect()")
        
        layout.addWidget(self.btn)
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def _on_click(self):
        print("\n" + "="*50)
        print("BUTTON CLICK DETECTED!")
        print("="*50)
        print(f"Username: {self.username.text()}")
        print(f"Password: {self.password.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleTest()
    window.show()
    print("Window shown, ready for button clicks...")
    sys.exit(app.exec_())
