#!/usr/bin/env python3
"""
Quick test of the multi-algorithm interface
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_algorithm_loading():
    """Test that algorithms load correctly"""
    print("Testing algorithm loading...")
    
    # Import solvers individually
    try:
        from solver.bfs_solver import bfs_solver
        print("✅ BFS solver imported successfully")
    except ImportError as e:
        print(f"❌ BFS solver import failed: {e}")
    
    try:
        from solver.dfs_solver import dfs
        print("✅ DFS solver imported successfully")
    except ImportError as e:
        print(f"❌ DFS solver import failed: {e}")
    
    try:
        from solver.ucs_solver import ucs
        print("✅ UCS solver imported successfully")
    except ImportError as e:
        print(f"❌ UCS solver import failed: {e}")
    
    # Test creating the GUI class
    try:
        import tkinter as tk
        from gui.test_interface import MultiAlgorithmTestGUI
        
        root = tk.Tk()
        root.withdraw()  # Hide the window for testing
        app = MultiAlgorithmTestGUI(root)
        
        print(f"✅ GUI created successfully")
        print(f"Available algorithms: {list(app.algorithms.keys())}")
        
        for algo_name, algo_info in app.algorithms.items():
            print(f"  - {algo_name}: {algo_info['name']}")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ GUI creation failed: {e}")
        import traceback
        traceback.print_exc()

def test_map_loading():
    """Test that maps can be loaded"""
    print("\nTesting map loading...")
    
    try:
        from utils.utils import import_map
        from utils.state import State
        
        # Test loading map 1
        vehicles = import_map(1)
        if vehicles:
            print(f"✅ Map 1 loaded successfully with {len(vehicles)} vehicles")
            
            # Test creating state
            state = State(vehicles)
            print(f"✅ State created successfully")
            print(f"  Solved: {state.is_solved()}")
            print(f"  Possible moves: {len(state.get_all_possible_moves())}")
        else:
            print("❌ Failed to load map 1")
            
    except Exception as e:
        print(f"❌ Map loading failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Testing Multi-Algorithm Rush Hour Interface")
    print("=" * 50)
    
    test_algorithm_loading()
    test_map_loading()
    
    print("\n✅ All tests completed!")
