#!/usr/bin/env python3
"""
Direct launcher for UCS Test Interface
Run from project root directory
"""
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import and run the test GUI
from gui.test_interface import main

if __name__ == "__main__":
    main()
