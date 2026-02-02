"""Main application entry point."""
import sys
from PyQt5.QtWidgets import QApplication
from api_client import APIClient
from auth_window import AuthWindow
from dashboard_window import DashboardWindow


class ChemicalVisualizerApp:
    """Main application class."""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.api_client = APIClient("http://localhost:8000/api")
        self.auth_window = None
        self.dashboard_window = None
    
    def run(self):
        """Start the application."""
        print("DEBUG: Starting ChemicalVisualizerApp")
        self._show_auth_window()
        print("DEBUG: App event loop starting...")
        sys.exit(self.app.exec_())
    
    def _show_auth_window(self):
        """Show authentication window."""
        print("DEBUG: Creating AuthWindow...")
        self.auth_window = AuthWindow(self.api_client)
        self.auth_window.login_success.connect(self._on_login_success)
        print("DEBUG: Showing AuthWindow...")
        self.auth_window.show()
        print("DEBUG: AuthWindow shown, window is visible =", self.auth_window.isVisible())
    
    def _on_login_success(self, token: str, username: str):
        """Handle successful login."""
        self.api_client.set_token(token)
        self.dashboard_window = DashboardWindow(self.api_client, username)
        self.dashboard_window.show()


if __name__ == "__main__":
    app = ChemicalVisualizerApp()
    app.run()
