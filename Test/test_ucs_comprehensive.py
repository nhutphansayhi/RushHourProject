#!/usr/bin/env python3
"""
Test functions for UCS Rush Hour Solver
"""
import sys
import os
import time

# Add parent directory to path to access modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.utils import import_map
from utils.state import State
from solver.ucs_solver import ucs

def test_ucs_with_map(map_id, description="", expected_solvable=True):
    """
    Test UCS solver with a specific map
    
    Args:
        map_id (int): Map number to load (e.g., 1 for map1.txt)
        description (str): Description of the test case
        expected_solvable (bool): Whether the puzzle should be solvable
    
    Returns:
        dict: Test results containing success, cost, time, etc.
    """
    print(f"\n{'='*60}")
    print(f"Testing Map {map_id}: {description}")
    print(f"{'='*60}")
    
    # Load vehicles from map file
    vehicles = import_map(map_id)
    if not vehicles:
        return {
            'success': False,
            'error': f'Failed to load map{map_id}.txt',
            'map_id': map_id
        }
    
    print(f"Loaded {len(vehicles)} vehicles:")
    for vehicle in vehicles:
        target_str = " (TARGET)" if vehicle.is_target else ""
        print(f"  {vehicle.id}: pos=({vehicle.row},{vehicle.col}), len={vehicle.length}, ori={vehicle.orientation}{target_str}")
    
    # Create initial state
    initial_state = State(vehicles)
    print(f"\nInitial State:")
    initial_state.display()
    
    # Check if already solved
    if initial_state.is_solved():
        print("Puzzle is already solved!")
        return {
            'success': True,
            'already_solved': True,
            'cost': 0,
            'steps': 0,
            'time': 0,
            'map_id': map_id
        }
    
    # Run UCS solver
    print("Running UCS solver...")
    start_time = time.time()
    
    try:
        result = ucs(initial_state)
        end_time = time.time()
        solve_time = end_time - start_time
        
        if result[0] is not None:  # Solution found
            cost, final_state, path = result
            steps = len(path)
            
            print(f"\n✅ SOLUTION FOUND!")
            print(f"Cost: {cost}")
            print(f"Steps: {steps}")
            print(f"Time: {solve_time:.3f} seconds")
            
            print(f"\nFinal State:")
            final_state.display()
            
            # Show solution path
            if steps > 0 and steps <= 10:  # Only show path for short solutions
                print(f"\nSolution Path:")
                for i, (vehicle_id, direction) in enumerate(path, 1):
                    print(f"  Step {i}: Move vehicle '{vehicle_id}' {direction}")
            elif steps > 10:
                print(f"\nSolution path has {steps} steps (too long to display)")
            
            return {
                'success': True,
                'solvable': True,
                'cost': cost,
                'steps': steps,
                'time': solve_time,
                'map_id': map_id,
                'matches_expected': expected_solvable
            }
        else:  # No solution
            print(f"\n❌ NO SOLUTION FOUND")
            print(f"Time: {solve_time:.3f} seconds")
            
            return {
                'success': True,
                'solvable': False,
                'time': solve_time,
                'map_id': map_id,
                'matches_expected': not expected_solvable
            }
            
    except Exception as e:
        end_time = time.time()
        solve_time = end_time - start_time
        print(f"\n💥 ERROR occurred: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'time': solve_time,
            'map_id': map_id
        }

def run_comprehensive_tests():
    """
    Run tests on multiple maps and summarize results
    """
    print("🚀 Starting Comprehensive UCS Tests")
    print("=" * 80)
    
    # Define test cases
    test_cases = [
        (1, "Basic puzzle", True),
        (2, "Medium puzzle", True),
        (3, "Complex puzzle", True),
        (4, "Another test case", True),
        (5, "Challenge puzzle", True),
        # Add more test cases as needed
    ]
    
    results = []
    total_time = 0
    
    for map_id, description, expected_solvable in test_cases:
        result = test_ucs_with_map(map_id, description, expected_solvable)
        results.append(result)
        if 'time' in result:
            total_time += result['time']
    
    # Summary
    print(f"\n{'='*80}")
    print("🏁 TEST SUMMARY")
    print(f"{'='*80}")
    
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    solvable_puzzles = [r for r in successful_tests if r.get('solvable', False)]
    
    print(f"Total tests run: {len(results)}")
    print(f"Successful tests: {len(successful_tests)}")
    print(f"Failed tests: {len(failed_tests)}")
    print(f"Solvable puzzles: {len(solvable_puzzles)}")
    print(f"Total execution time: {total_time:.3f} seconds")
    
    if solvable_puzzles:
        avg_cost = sum(r['cost'] for r in solvable_puzzles) / len(solvable_puzzles)
        avg_steps = sum(r['steps'] for r in solvable_puzzles) / len(solvable_puzzles)
        print(f"Average cost: {avg_cost:.2f}")
        print(f"Average steps: {avg_steps:.2f}")
    
    # Detailed results
    print(f"\n📊 DETAILED RESULTS:")
    for result in results:
        map_id = result['map_id']
        if result['success']:
            if result.get('solvable', False):
                cost = result.get('cost', 0)
                steps = result.get('steps', 0)
                time_taken = result.get('time', 0)
                print(f"  Map {map_id}: ✅ SOLVED (Cost: {cost}, Steps: {steps}, Time: {time_taken:.3f}s)")
            elif result.get('already_solved', False):
                print(f"  Map {map_id}: ✅ ALREADY SOLVED")
            else:
                time_taken = result.get('time', 0)
                print(f"  Map {map_id}: ❌ NO SOLUTION (Time: {time_taken:.3f}s)")
        else:
            error = result.get('error', 'Unknown error')
            print(f"  Map {map_id}: 💥 ERROR - {error}")

def test_specific_functionality():
    """
    Test specific functionality of the solver
    """
    print(f"\n{'='*60}")
    print("🔧 Testing Specific Functionality")
    print(f"{'='*60}")
    
    # Test 1: State creation and hashing
    print("\n1. Testing State creation and hashing...")
    vehicles = import_map(1)
    if vehicles:
        state1 = State(vehicles)
        state2 = State(vehicles)
        
        print(f"   State1 hash: {hash(state1)}")
        print(f"   State2 hash: {hash(state2)}")
        print(f"   States equal: {state1 == state2}")
        print(f"   States in set: {len({state1, state2})} (should be 1)")
    
    # Test 2: Move generation
    print("\n2. Testing move generation...")
    if vehicles:
        state = State(vehicles)
        moves = state.get_all_possible_moves()
        print(f"   Possible moves: {len(moves)}")
        for vehicle_id, direction in moves[:5]:  # Show first 5 moves
            print(f"     {vehicle_id} -> {direction}")
        if len(moves) > 5:
            print(f"     ... and {len(moves) - 5} more moves")

if __name__ == "__main__":
    # You can run individual tests or comprehensive tests
    
    # Option 1: Test a specific map
    # test_ucs_with_map(1, "Simple test puzzle", True)
    
    # Option 2: Run comprehensive tests
    run_comprehensive_tests()
    
    # Option 3: Test specific functionality
    test_specific_functionality()
