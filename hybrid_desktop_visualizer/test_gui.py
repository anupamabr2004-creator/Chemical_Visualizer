"""Test script to verify GUI button responses."""
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Test")
        self.setGeometry(100, 100, 300, 200)
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        btn = QPushButton("Click Me")
        btn.clicked.connect(self.on_click)
        layout.addWidget(btn)
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def on_click(self):
        print("✓ BUTTON CLICK DETECTED!")


if __name__ == "__main__":
    print("Starting test...")
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    print("Window shown. Try clicking the button...")
    sys.exit(app.exec_())
