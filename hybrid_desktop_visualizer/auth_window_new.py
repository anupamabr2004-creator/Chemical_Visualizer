"""Authentication window for login and registration."""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from api_client import APIClient


class AuthWindow(QMainWindow):
    """Authentication window with login and registration."""
    
    login_success = pyqtSignal(str, str)  # token, username
    
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Chemical Visualizer - Authentication")
        self.setGeometry(100, 100, 500, 600)
        
        # Create stacked widget for login/register views
        self.stacked = QStackedWidget()
        self.login_widget = self._create_login_widget()
        self.register_widget = self._create_register_widget()
        
        self.stacked.addWidget(self.login_widget)
        self.stacked.addWidget(self.register_widget)
        
        self.setCentralWidget(self.stacked)
        self.stacked.setCurrentWidget(self.login_widget)
        
        self._apply_styles()
    
    def _create_login_widget(self) -> QWidget:
        """Create login form."""
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Spacer at top
        main_layout.addSpacing(40)
        
        # Centered card layout
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(48, 48, 48, 48)
        card_layout.setSpacing(24)
        
        # Card background widget
        card = QWidget()
        card.setMaximumWidth(420)
        card.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e6eef6;
            }
        """)
        
        # Title
        title = QLabel("Login")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e3a8a;")
        card_layout.addWidget(title)
        
        card_layout.addSpacing(8)
        
        # Subtitle
        subtitle = QLabel("Sign in to Chemical Visualizer")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #64748b; font-size: 13px;")
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(24)
        
        # Username
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #0b1220; font-weight: 600;")
        card_layout.addWidget(username_label)
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        self.login_username.setMinimumHeight(40)
        card_layout.addWidget(self.login_username)
        
        # Password
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #0b1220; font-weight: 600;")
        card_layout.addWidget(password_label)
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setMinimumHeight(40)
        card_layout.addWidget(self.login_password)
        
        card_layout.addSpacing(12)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self._handle_login)
        login_btn.setMinimumHeight(44)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setEnabled(True)
        login_btn.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #1D4ED8 0%, #1E3A8A 100%);
            }
        """)
        card_layout.addWidget(login_btn)
        
        # Divider
        divider = QLabel("─" * 40)
        divider.setAlignment(Qt.AlignCenter)
        divider.setStyleSheet("color: #cbd5e1;")
        card_layout.addWidget(divider)
        
        # Toggle to register
        toggle_layout = QHBoxLayout()
        toggle_layout.addWidget(QLabel("Don't have an account?"))
        register_toggle = QPushButton("Sign Up")
        register_toggle.setMaximumWidth(70)
        register_toggle.setStyleSheet("""
            QPushButton {
                background: none;
                color: #2563eb;
                padding: 0px;
                border: none;
                font-weight: 700;
                text-decoration: underline;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #1e40af;
            }
        """)
        register_toggle.clicked.connect(lambda: self.stacked.setCurrentWidget(self.register_widget))
        toggle_layout.addWidget(register_toggle)
        toggle_layout.addStretch()
        card_layout.addLayout(toggle_layout)
        
        card.setLayout(card_layout)
        
        # Center the card
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(card)
        center_layout.addStretch()
        main_layout.addLayout(center_layout)
        
        main_layout.addStretch()
        
        widget.setLayout(main_layout)
        return widget
    
    def _create_register_widget(self) -> QWidget:
        """Create registration form."""
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Spacer at top
        main_layout.addSpacing(40)
        
        # Centered card layout
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(48, 48, 48, 48)
        card_layout.setSpacing(24)
        
        # Card background widget
        card = QWidget()
        card.setMaximumWidth(420)
        card.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e6eef6;
            }
        """)
        
        # Title
        title = QLabel("Create Account")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e3a8a;")
        card_layout.addWidget(title)
        
        card_layout.addSpacing(8)
        
        # Subtitle
        subtitle = QLabel("Join Chemical Visualizer")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #64748b; font-size: 13px;")
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(24)
        
        # Username
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #0b1220; font-weight: 600;")
        card_layout.addWidget(username_label)
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose a username")
        self.register_username.setMinimumHeight(40)
        card_layout.addWidget(self.register_username)
        
        # Email
        email_label = QLabel("Email")
        email_label.setStyleSheet("color: #0b1220; font-weight: 600;")
        card_layout.addWidget(email_label)
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Enter your email")
        self.register_email.setMinimumHeight(40)
        card_layout.addWidget(self.register_email)
        
        # Password
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #0b1220; font-weight: 600;")
        card_layout.addWidget(password_label)
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Create a password")
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setMinimumHeight(40)
        card_layout.addWidget(self.register_password)
        
        card_layout.addSpacing(12)
        
        # Register button
        register_btn = QPushButton("Create Account")
        register_btn.clicked.connect(self._handle_register)
        register_btn.setMinimumHeight(44)
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.setEnabled(True)
        register_btn.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #1D4ED8 0%, #1E3A8A 100%);
            }
        """)
        card_layout.addWidget(register_btn)
        
        # Divider
        divider = QLabel("─" * 40)
        divider.setAlignment(Qt.AlignCenter)
        divider.setStyleSheet("color: #cbd5e1;")
        card_layout.addWidget(divider)
        
        # Toggle to login
        toggle_layout = QHBoxLayout()
        toggle_layout.addWidget(QLabel("Already have an account?"))
        login_toggle = QPushButton("Login")
        login_toggle.setMaximumWidth(60)
        login_toggle.setStyleSheet("""
            QPushButton {
                background: none;
                color: #2563eb;
                padding: 0px;
                border: none;
                font-weight: 700;
                text-decoration: underline;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #1e40af;
            }
        """)
        login_toggle.clicked.connect(lambda: self.stacked.setCurrentWidget(self.login_widget))
        toggle_layout.addWidget(login_toggle)
        toggle_layout.addStretch()
        card_layout.addLayout(toggle_layout)
        
        card.setLayout(card_layout)
        
        # Center the card
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(card)
        center_layout.addStretch()
        main_layout.addLayout(center_layout)
        
        main_layout.addStretch()
        
        widget.setLayout(main_layout)
        return widget
    
    def _handle_login(self):
        """Handle login button click."""
        print("[LOGIN BUTTON CLICKED]")
        
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()
        
        print(f"Username: {username}, Password length: {len(password)}")
        
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields")
            return
        
        print("[API] Calling login...")
        success, message, token = self.api_client.login(username, password)
        print(f"[API] Result: success={success}, message={message}")
        
        if success:
            print("[LOGIN] Success! Emitting signal and closing...")
            self.login_success.emit(token, username)
            self.close()
        else:
            print(f"[LOGIN] Failed: {message}")
            QMessageBox.critical(self, "Login Failed", message)
    
    def _handle_register(self):
        """Handle registration button click."""
        print("[REGISTER BUTTON CLICKED]")
        
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text().strip()
        
        print(f"Username: {username}, Email: {email}, Password length: {len(password)}")
        
        if not username or not email or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields")
            return
        
        print("[API] Calling register...")
        success, message = self.api_client.register(username, email, password)
        print(f"[API] Result: success={success}, message={message}")
        
        if success:
            print("[REGISTER] Success!")
            QMessageBox.information(self, "Success", "Registration successful! Please login.")
            self.stacked.setCurrentWidget(self.login_widget)
            self.register_username.clear()
            self.register_email.clear()
            self.register_password.clear()
        else:
            print(f"[REGISTER] Failed: {message}")
            QMessageBox.critical(self, "Registration Failed", message)
    
    def _apply_styles(self):
        """Apply light theme styles matching web frontend."""
        self.setStyleSheet("""
            QMainWindow {
                background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 50%, #ffffff 100%);
            }
            QWidget {
                background-color: transparent;
            }
            QLabel {
                color: #0b1220;
                font-weight: 500;
                font-size: 13px;
            }
            QLineEdit {
                border: 1px solid #e6eef6;
                border-radius: 8px;
                padding: 12px 16px;
                background-color: #ffffff;
                color: #0b1220;
                font-weight: 500;
                font-size: 14px;
                selection-background-color: #dbeafe;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
                padding: 11px 15px;
                background-color: #ffffff;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
            QPushButton {
                background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                letter-spacing: 0.3px;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #1D4ED8 0%, #1E3A8A 100%);
            }
            QPushButton:pressed {
                background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
            }
        """)
