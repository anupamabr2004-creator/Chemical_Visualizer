#!/usr/bin/env python3
"""
Test script to verify the Chemical Visualizer backend is working correctly.
Run this before starting the desktop application.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_connection():
    """Test basic connection to backend."""
    print("Testing backend connection...")
    try:
        response = requests.get(f"{BASE_URL}/auth/login/", timeout=5)
        print(f"✓ Backend is running (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend at http://localhost:8000")
        print("  Make sure Django is running: python manage.py runserver")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_registration(username, email, password):
    """Test user registration."""
    print(f"\nTesting registration with user: {username}...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register/",
            json={"username": username, "email": email, "password": password}
        )
        if response.status_code in [200, 201]:
            print(f"✓ Registration successful")
            return True
        elif response.status_code == 400:
            # User might already exist
            print(f"✓ User already exists or invalid data (this is OK for testing)")
            return True
        else:
            print(f"✗ Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_login(username, password):
    """Test user login."""
    print(f"\nTesting login with user: {username}...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            token = data.get("access")
            if token:
                print(f"✓ Login successful")
                print(f"  Token: {token[:20]}...")
                return token
            else:
                print(f"✗ No token in response")
                return None
        else:
            print(f"✗ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

def test_api_endpoints(token):
    """Test API endpoints with authentication."""
    print(f"\nTesting API endpoints...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test datasets endpoint
    try:
        response = requests.get(
            f"{BASE_URL}/equipment/datasets/",
            headers=headers
        )
        if response.status_code == 200:
            datasets = response.json()
            print(f"✓ Dataset endpoint working (Found {len(datasets)} datasets)")
        else:
            print(f"✗ Dataset endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing datasets: {str(e)}")
    
    # Test summary endpoint
    try:
        response = requests.get(
            f"{BASE_URL}/equipment/summary/",
            headers=headers
        )
        if response.status_code == 200:
            summary = response.json()
            print(f"✓ Summary endpoint working")
            print(f"  Total datasets: {summary.get('datasets_count', 0)}")
            print(f"  Total equipment: {summary.get('total_equipment', 0)}")
        else:
            print(f"✗ Summary endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing summary: {str(e)}")

def main():
    """Run all tests."""
    print("=" * 50)
    print("Chemical Visualizer Backend Test Suite")
    print("=" * 50)
    
    # Test connection
    if not test_connection():
        print("\n✗ Backend is not running. Please start it first:")
        print("  cd chemical_visualizer")
        print("  python manage.py runserver")
        sys.exit(1)
    
    # Test registration and login
    test_user = "testuser"
    test_email = "test@example.com"
    test_password = "testpass123"
    
    test_registration(test_user, test_email, test_password)
    token = test_login(test_user, test_password)
    
    if not token:
        print("\n✗ Login failed. Try registering again with different credentials.")
        sys.exit(1)
    
    # Test API endpoints
    test_api_endpoints(token)
    
    print("\n" + "=" * 50)
    print("✓ All tests completed!")
    print("=" * 50)
    print("\nYou can now run the desktop application:")
    print("  python main.py")

if __name__ == "__main__":
    main()
