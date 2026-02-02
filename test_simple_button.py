#!/usr/bin/env python
"""Ultra-simple button test - no frills."""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

def on_button_click():
    print("\n" + "="*50)
    print("BUTTON CLICKED - THIS ACTUALLY WORKED!")
    print("="*50)

app = QApplication(sys.argv)

# Create simple window
window = QWidget()
window.setWindowTitle("Super Simple Button Test")
window.setGeometry(100, 100, 300, 150)

layout = QVBoxLayout()

# Add button
btn = QPushButton("Click Me")
print(f"[TEST] Button created: {btn}")

# Connect signal
btn.clicked.connect(on_button_click)
print(f"[TEST] Signal connected")

layout.addWidget(btn)
window.setLayout(layout)

# Show window
window.show()
print("[TEST] Window shown. Click the button now...")
print()

sys.exit(app.exec_())
