#!/usr/bin/env python
"""Test API endpoints."""
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Test register endpoint
print("Testing REGISTER endpoint...")
response = requests.post(
    f"{BASE_URL}/auth/register/",
    json={"username": "testuser", "email": "test@test.com", "password": "testpass123"}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}\n")

# Test login endpoint
print("Testing LOGIN endpoint...")
response = requests.post(
    f"{BASE_URL}/auth/login/",
    json={"username": "testuser", "password": "testpass123"}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}\n")
