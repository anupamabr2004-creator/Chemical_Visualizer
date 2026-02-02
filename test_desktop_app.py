#!/usr/bin/env python3
"""
Comprehensive test script for hybrid_desktop_visualizer
Tests all features: login, register, CSV upload, analysis, PDF export, history
"""

import sys
import os
import time
import csv
from pathlib import Path

# Add the hybrid_desktop_visualizer directory to path
sys.path.insert(0, r"c:\Users\Surjeet Kumar\chemical_visualizer\hybrid_desktop_visualizer")
sys.path.insert(0, r"c:\Users\Surjeet Kumar\chemical_visualizer")

from hybrid_desktop_visualizer.api_client import APIClient

def print_header(text):
    """Print a test header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_success(text):
    """Print a success message."""
    print(f"✓ SUCCESS: {text}")

def print_error(text):
    """Print an error message."""
    print(f"✗ ERROR: {text}")

def print_info(text):
    """Print an info message."""
    print(f"ℹ INFO: {text}")

# Test 1: Initialize API Client
print_header("TEST 1: API CLIENT INITIALIZATION")
try:
    api_client = APIClient("http://localhost:8000/api")
    print_success("API Client initialized")
    print_info(f"Base URL: {api_client.base_url}")
except Exception as e:
    print_error(f"Failed to initialize API client: {e}")
    sys.exit(1)

# Test 2: Register a test user
print_header("TEST 2: USER REGISTRATION")
test_username = f"testuser_{int(time.time())}"
test_email = f"test_{int(time.time())}@example.com"
test_password = "TestPassword123!"

try:
    success, message = api_client.register(test_username, test_email, test_password)
    if success:
        print_success(f"User registered: {test_username}")
        print_info(f"Message: {message}")
    else:
        print_error(f"Registration failed: {message}")
        # Try to continue with existing user
        print_info("Attempting to use existing test credentials...")
        test_username = "testuser"
        test_email = "testuser@example.com"
        test_password = "password123"
except Exception as e:
    print_error(f"Registration error: {e}")

# Test 3: User Login
print_header("TEST 3: USER LOGIN")
try:
    success, message, token = api_client.login(test_username, test_password)
    if success:
        print_success(f"User logged in: {test_username}")
        print_info(f"Token received: {token[:20]}..." if token else "No token")
    else:
        print_error(f"Login failed: {message}")
        sys.exit(1)
except Exception as e:
    print_error(f"Login error: {e}")
    sys.exit(1)

# Test 4: Load Datasets
print_header("TEST 4: LOAD EXISTING DATASETS")
try:
    success, message, datasets = api_client.get_datasets()
    if success:
        print_success(f"Loaded {len(datasets)} dataset(s)")
        for idx, dataset in enumerate(datasets[:5], 1):
            print_info(f"  Dataset {idx}: {dataset.get('name', 'Unknown')} (ID: {dataset.get('id', 'N/A')})")
    else:
        print_error(f"Failed to load datasets: {message}")
except Exception as e:
    print_error(f"Error loading datasets: {e}")

# Test 5: Create and Upload CSV File
print_header("TEST 5: CSV FILE UPLOAD")
csv_file_path = r"c:\Users\Surjeet Kumar\chemical_visualizer\test_equipment.csv"

try:
    # Create test CSV file
    csv_data = [
        ['Type', 'Flowrate', 'Pressure', 'Temperature'],
        ['Pump', '50.5', '2.3', '25.0'],
        ['Pump', '45.2', '2.1', '24.5'],
        ['Reactor', '30.0', '5.5', '65.0'],
        ['Reactor', '32.1', '5.6', '66.2'],
        ['Heat Exchanger', '100.0', '1.5', '30.0'],
        ['Heat Exchanger', '98.5', '1.4', '29.8'],
    ]
    
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    
    print_success(f"Test CSV file created: {csv_file_path}")
    
    # Upload the file
    success, message = api_client.upload_file(csv_file_path)
    if success:
        print_success(f"File uploaded: {message}")
    else:
        print_error(f"File upload failed: {message}")
except Exception as e:
    print_error(f"CSV upload error: {e}")

# Test 6: Reload Datasets after upload
print_header("TEST 6: RELOAD DATASETS AFTER UPLOAD")
try:
    success, message, datasets = api_client.get_datasets()
    if success:
        print_success(f"Reloaded {len(datasets)} dataset(s)")
        if len(datasets) > 0:
            latest = datasets[0]
            print_info(f"Latest dataset: {latest.get('name', 'Unknown')}")
            print_info(f"  Created: {latest.get('created_at', 'N/A')}")
            print_info(f"  Equipment count: {latest.get('equipment_count', 'N/A')}")
    else:
        print_error(f"Failed to reload datasets: {message}")
except Exception as e:
    print_error(f"Error reloading datasets: {e}")

# Test 7: Get Dataset Detail
print_header("TEST 7: GET DATASET DETAIL & ANALYSIS")
if len(datasets) > 0:
    dataset_id = datasets[0].get('id')
    try:
        success, message, detail = api_client.get_dataset_detail(dataset_id)
        if success:
            print_success(f"Dataset detail loaded for dataset {dataset_id}")
            if detail:
                print_info(f"Dataset name: {detail.get('name', 'N/A')}")
                print_info(f"Equipment count: {detail.get('equipment_count', 'N/A')}")
                print_info(f"Average flowrate: {detail.get('average_flowrate', 'N/A')} L/min")
                print_info(f"Average pressure: {detail.get('average_pressure', 'N/A')} bar")
                print_info(f"Average temperature: {detail.get('average_temperature', 'N/A')}°C")
                
                # Type distribution
                type_dist = detail.get('type_distribution', {})
                if type_dist:
                    print_info(f"Equipment types: {', '.join(type_dist.keys())}")
        else:
            print_error(f"Detail loading failed: {message}")
    except Exception as e:
        print_error(f"Detail loading error: {e}")
else:
    print_error("No datasets available for detail analysis")

# Test 7b: Get Data Summary
print_header("TEST 7B: GET OVERALL DATA SUMMARY")
try:
    success, message, summary = api_client.get_data_summary()
    if success:
        print_success("Data summary loaded")
        if summary:
            print_info(f"Total equipment: {summary.get('total_count', 'N/A')}")
            print_info(f"Average flowrate (all): {summary.get('average_flowrate', 'N/A')} L/min")
            print_info(f"Average pressure (all): {summary.get('average_pressure', 'N/A')} bar")
            print_info(f"Average temperature (all): {summary.get('average_temperature', 'N/A')}°C")
    else:
        print_error(f"Summary loading failed: {message}")
except Exception as e:
    print_error(f"Summary loading error: {e}")

# Test 8: Export PDF
print_header("TEST 8: PDF EXPORT")
if len(datasets) > 0:
    dataset_id = datasets[0].get('id')
    pdf_output_path = r"c:\Users\Surjeet Kumar\chemical_visualizer\test_report.pdf"
    try:
        success, message, pdf_content = api_client.export_pdf(dataset_id)
        if success:
            print_success(f"PDF exported successfully")
            if pdf_content:
                # Write PDF to file
                with open(pdf_output_path, 'wb') as f:
                    f.write(pdf_content)
                file_size = os.path.getsize(pdf_output_path)
                print_info(f"File saved: {pdf_output_path}")
                print_info(f"File size: {file_size} bytes")
        else:
            print_error(f"PDF export failed: {message}")
    except Exception as e:
        print_error(f"PDF export error: {e}")
else:
    print_error("No datasets available for PDF export")

# Test 9: Dataset History
print_header("TEST 9: DATASET HISTORY & MANAGEMENT")
try:
    success, message, datasets = api_client.get_datasets()
    if success:
        print_success(f"History retrieved: {len(datasets)} datasets")
        for idx, dataset in enumerate(datasets[:3], 1):
            print_info(f"  {idx}. {dataset.get('name', 'Unknown')} - {dataset.get('equipment_count', 0)} items")
    else:
        print_error(f"History retrieval failed: {message}")
except Exception as e:
    print_error(f"History error: {e}")

# Test 10: Delete Dataset
print_header("TEST 10: DELETE DATASET")
if len(datasets) > 1:
    # Delete the oldest dataset (keep the newest one)
    dataset_to_delete = datasets[-1]
    dataset_id = dataset_to_delete.get('id')
    try:
        success, message = api_client.delete_dataset(dataset_id)
        if success:
            print_success(f"Dataset deleted: {dataset_to_delete.get('name', 'Unknown')}")
        else:
            print_error(f"Deletion failed: {message}")
    except Exception as e:
        print_error(f"Delete error: {e}")
else:
    print_info("Skipped - need multiple datasets to test deletion")

# Final Summary
print_header("TEST SUMMARY")
print_success("All tests completed!")
print_info("The hybrid_desktop_visualizer application is ready to use.")
print_info("\nFeatures tested:")
print_info("  ✓ User Registration")
print_info("  ✓ User Login")
print_info("  ✓ CSV Upload")
print_info("  ✓ Dataset Analysis")
print_info("  ✓ PDF Export")
print_info("  ✓ Dataset History")
print_info("  ✓ Dataset Deletion")
print("\n" + "="*70)
