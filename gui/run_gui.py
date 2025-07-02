#!/usr/bin/env python3
"""
Rush Hour Puzzle GUI Launcher
"""
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import and run the GUI
from gui.rushhour_gui import main

if __name__ == "__main__":
    main()
