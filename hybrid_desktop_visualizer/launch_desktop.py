#!/usr/bin/env python
"""Test launcher with visible output."""
import sys
import os

# Change to the script directory
os.chdir(r"C:\Users\Surjeet Kumar\chemical_visualizer\hybrid_desktop_visualizer")

# Add parent directory to path
sys.path.insert(0, os.getcwd())

print("="*70)
print("STARTING CHEMICAL VISUALIZER DESKTOP APP")
print("="*70)
print(f"Current directory: {os.getcwd()}")
print(f"Python: {sys.executable}")
print()

# Import and run
from main import ChemicalVisualizerApp

try:
    print("Creating app...")
    app = ChemicalVisualizerApp()
    print("Running app...")
    app.run()
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
