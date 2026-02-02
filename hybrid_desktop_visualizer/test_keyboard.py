#!/usr/bin/env python
"""
Test that demonstrates the keyboard event handling works correctly.
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent

# Import the custom button
sys.path.insert(0, r"C:\Users\Surjeet Kumar\chemical_visualizer\hybrid_desktop_visualizer")
from auth_window import ClickableButton

print("\n" + "="*70)
print("KEYBOARD EVENT TEST - DEMONSTRATING KEY PRESS HANDLING")
print("="*70 + "\n")

app = QApplication(sys.argv)

# Create a simple test window
window = QWidget()
window.setWindowTitle("Keyboard Test - Press Tab then Enter on the button")
window.setGeometry(100, 100, 400, 300)

layout = QVBoxLayout()

layout.addWidget(QLabel("Username:"))
username_field = QLineEdit()
username_field.setText("testuser")
layout.addWidget(username_field)

layout.addWidget(QLabel("Password:"))
password_field = QLineEdit()
password_field.setEchoMode(QLineEdit.Password)
password_field.setText("testpass123")
layout.addWidget(password_field)

# Create clickable button
button = ClickableButton("Login (Press Enter or Space)")
click_count = {"count": 0}

def on_button_click():
    click_count["count"] += 1
    print(f"\n>>> BUTTON CLICKED! (Click #{click_count['count']})")
    print(f"    Username: {username_field.text()}")
    print(f"    Password: {'*' * len(password_field.text())}")

# Connect both signals
button.clicked.connect(on_button_click)
button.button_clicked.connect(on_button_click)

layout.addWidget(button)

window.setLayout(layout)

print("INSTRUCTIONS:")
print("1. Window will open in a moment")
print("2. Username and password are already filled")
print("3. Click in the window")
print("4. Press TAB to focus the Login button (it will be highlighted in blue)")
print("5. Press ENTER or SPACEBAR")
print("6. You should see 'BUTTON CLICKED!' message in console")
print("\nWaiting for user input...\n")

window.show()
sys.exit(app.exec_())
