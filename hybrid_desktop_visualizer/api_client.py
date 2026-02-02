"""API Client for communicating with Django backend."""
import requests
import json
from typing import Optional, List, Dict, Tuple
import os


class APIClient:
    """Handles all API communication with the Django backend."""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url.rstrip('/')
        self.token: Optional[str] = None
        self.session = requests.Session()
        self.username: Optional[str] = None
    
    def set_token(self, token: str):
        """Set the authentication token."""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def register(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """Register a new user."""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/register/",
                json={"username": username, "email": email, "password": password}
            )
            if response.status_code in [200, 201]:
                data = response.json()
                return True, data.get("message", "Registration successful")
            else:
                error_msg = response.json()
                if isinstance(error_msg, dict):
                    return False, error_msg.get("error", error_msg.get("detail", "Registration failed"))
                return False, "Registration failed"
        except requests.exceptions.ConnectionError:
            return False, "Connection error: Backend server not running"
        except Exception as e:
            return False, str(e)
    
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[str]]:
        """Login user and return token."""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login/",
                json={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                token = data.get("access")
                if token:
                    self.set_token(token)
                    self.username = username
                    return True, "Login successful", token
                return False, "No token in response", None
            else:
                error_msg = response.json()
                if isinstance(error_msg, dict):
                    msg = error_msg.get("error", error_msg.get("detail", "Login failed"))
                else:
                    msg = "Login failed"
                return False, msg, None
        except requests.exceptions.ConnectionError:
            return False, "Connection error: Backend server not running", None
        except Exception as e:
            return False, str(e), None
    
    def get_datasets(self) -> Tuple[bool, str, List[Dict]]:
        """Fetch all datasets (last 5) for authenticated user."""
        try:
            response = self.session.get(f"{self.base_url}/equipment/datasets/")
            if response.status_code == 200:
                return True, "Datasets loaded", response.json()
            else:
                return False, "Failed to load datasets", []
        except requests.exceptions.ConnectionError:
            return False, "Connection error: Backend server not running", []
        except Exception as e:
            return False, str(e), []
    
    def upload_file(self, file_path: str) -> Tuple[bool, str]:
        """Upload a CSV file."""
        try:
            if not os.path.exists(file_path):
                return False, f"File not found: {file_path}"
            
            filename = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f, 'text/csv')}
                response = self.session.post(
                    f"{self.base_url}/equipment/upload/",
                    files=files
                )
            
            if response.status_code in [200, 201]:
                return True, "File uploaded successfully"
            else:
                error_msg = response.json()
                if isinstance(error_msg, dict):
                    return False, error_msg.get("detail", error_msg.get("error", "Upload failed"))
                return False, "Upload failed"
        except requests.exceptions.ConnectionError:
            return False, "Connection error: Backend server not running"
        except Exception as e:
            return False, str(e)
    
    def get_dataset_detail(self, dataset_id: int) -> Tuple[bool, str, Optional[Dict]]:
        """Get detailed information about a dataset."""
        try:
            response = self.session.get(f"{self.base_url}/equipment/datasets/{dataset_id}/")
            if response.status_code == 200:
                return True, "Dataset loaded", response.json()
            else:
                return False, "Failed to load dataset", None
        except requests.exceptions.ConnectionError:
            return False, "Connection error: Backend server not running", None
        except Exception as e:
            return False, str(e), None
    
    def delete_dataset(self, dataset_id: int) -> Tuple[bool, str]:
        """Delete a dataset."""
        try:
            response = self.session.delete(f"{self.base_url}/equipment/datasets/{dataset_id}/")
            if response.status_code == 204:
                return True, "Dataset deleted"
            else:
                return False, "Failed to delete dataset"
        except requests.exceptions.ConnectionError:
            return False, "Connection error: Backend server not running"
        except Exception as e:
            return False, str(e)
    
    def get_data_summary(self) -> Tuple[bool, str, Optional[Dict]]:
        """Get data summary (total count, averages, distribution)."""
        try:
            response = self.session.get(f"{self.base_url}/equipment/summary/")
            if response.status_code == 200:
                return True, "Summary loaded", response.json()
            else:
                return False, "Failed to load summary", None
        except requests.exceptions.ConnectionError:
            return False, "Connection error: Backend server not running", None
        except Exception as e:
            return False, str(e), None
    
    def export_pdf(self, dataset_id: int) -> Tuple[bool, str, Optional[bytes]]:
        """Export dataset as PDF."""
        try:
            response = self.session.get(f"{self.base_url}/equipment/datasets/{dataset_id}/export-pdf/")
            if response.status_code == 200:
                return True, "PDF exported", response.content
            else:
                return False, "Failed to export PDF", None
        except requests.exceptions.ConnectionError:
            return False, "Connection error: Backend server not running", None
        except Exception as e:
            return False, str(e), None
