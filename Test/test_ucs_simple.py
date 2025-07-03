#!/usr/bin/env python3
"""
Simple test for UCS Rush Hour Solver
"""
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.utils import import_map
from utils.state import State
from solver.ucs_solver import ucs

def simple_test():
    """Simple test of UCS solver with map1"""
    print("🎯 Simple UCS Test")
    print("=" * 40)
    
    # Load map
    vehicles = import_map(1)
    if not vehicles:
        print("❌ Failed to load map1.txt")
        return
    
    # Create state
    initial_state = State(vehicles)
    print("Initial State:")
    initial_state.display()
    
    # Solve
    print("Solving with UCS...")
    result = ucs(initial_state)
    
    if result[0] is not None:
        cost, final_state, path = result
        print(f"\n✅ Solution found!")
        print(f"Cost: {cost}")
        print(f"Steps: {len(path)}")
        print("\nFinal State:")
        final_state.display()
        
        print("\nSolution moves:")
        for i, (vehicle_id, direction) in enumerate(path, 1):
            print(f"  {i}. Move {vehicle_id} {direction}")
    else:
        print("❌ No solution found")

if __name__ == "__main__":
    simple_test()
