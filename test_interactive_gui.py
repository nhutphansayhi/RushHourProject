#!/usr/bin/env python3
"""
Simple test script for the interactive GUI features
"""
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from utils.utils import import_map
from utils.state import State
from solver.ucs_solver import ucs

def test_interactive_features():
    """Test the core functionality that the GUI uses"""
    print("🧪 Testing Interactive GUI Core Features")
    print("=" * 50)
    
    # Test 1: Load a map
    print("\n1. Testing map loading...")
    vehicles = import_map(1)
    if vehicles:
        print(f"✅ Successfully loaded {len(vehicles)} vehicles from map1")
        for vehicle in vehicles:
            print(f"   {vehicle.id}: ({vehicle.row},{vehicle.col}) len={vehicle.length} ori={vehicle.orientation}")
    else:
        print("❌ Failed to load map1")
        return False
    
    # Test 2: Create states
    print("\n2. Testing state creation...")
    try:
        initial_state = State(vehicles)
        print("✅ Successfully created initial state")
        print(f"   Solved: {initial_state.is_solved()}")
    except Exception as e:
        print(f"❌ Failed to create state: {e}")
        return False
    
    # Test 3: Vehicle copying
    print("\n3. Testing vehicle copying...")
    try:
        test_vehicle = vehicles[0]
        copied_vehicle = test_vehicle.copy()
        print(f"✅ Successfully copied vehicle {test_vehicle.id}")
        print(f"   Original: ({test_vehicle.row},{test_vehicle.col})")
        print(f"   Copy: ({copied_vehicle.row},{copied_vehicle.col})")
    except Exception as e:
        print(f"❌ Failed to copy vehicle: {e}")
        return False
    
    # Test 4: Manual move simulation
    print("\n4. Testing manual move simulation...")
    try:
        # Find a vehicle that can move
        target_vehicle = None
        for vehicle in vehicles:
            if vehicle.orientation == 'H' and vehicle.col > 0:
                target_vehicle = vehicle
                break
            elif vehicle.orientation == 'V' and vehicle.row > 0:
                target_vehicle = vehicle
                break
        
        if target_vehicle:
            # Create new state with moved vehicle
            new_vehicles = []
            direction = ""
            moved_vehicle = None
            
            for vehicle in vehicles:
                if vehicle.id == target_vehicle.id:
                    moved_vehicle = vehicle.copy()
                    if vehicle.orientation == 'H':
                        moved_vehicle.col -= 1
                        direction = "left"
                    else:
                        moved_vehicle.row -= 1
                        direction = "up"
                    new_vehicles.append(moved_vehicle)
                else:
                    new_vehicles.append(vehicle)
            
            new_state = State(new_vehicles)
            print(f"✅ Successfully simulated moving {target_vehicle.id} {direction}")
            print(f"   Original position: ({target_vehicle.row},{target_vehicle.col})")
            if moved_vehicle:
                print(f"   New position: ({moved_vehicle.row},{moved_vehicle.col})")
        else:
            print("⚠️  No moveable vehicle found for testing")
    except Exception as e:
        print(f"❌ Failed to simulate manual move: {e}")
        return False
    
    # Test 5: UCS solving and path replay
    print("\n5. Testing UCS solving...")
    try:
        result = ucs(initial_state)
        if result[0] is not None:
            cost, final_state, path = result
            print(f"✅ UCS found solution with cost {cost} and {len(path)} steps")
            
            # Test path replay
            print(f"   Testing path replay...")
            current_state = initial_state
            for i, (vehicle_id, direction) in enumerate(path[:3]):  # Test first 3 moves
                print(f"   Step {i+1}: Move {vehicle_id} {direction}")
                # This simulates what the GUI does during step-by-step playback
                new_vehicles = []
                for vehicle in current_state.vehicles:
                    if vehicle.id == vehicle_id:
                        new_vehicle = vehicle.copy()
                        if direction in ['UP']:
                            new_vehicle.row -= 1
                        elif direction in ['DOWN']:
                            new_vehicle.row += 1
                        elif direction in ['LEFT']:
                            new_vehicle.col -= 1
                        elif direction in ['RIGHT']:
                            new_vehicle.col += 1
                        new_vehicles.append(new_vehicle)
                    else:
                        new_vehicles.append(vehicle)
                current_state = State(new_vehicles)
            
            print("✅ Path replay simulation successful")
        else:
            print("⚠️  UCS found no solution for map1")
    except Exception as e:
        print(f"❌ Failed UCS solving: {e}")
        return False
    
    print("\n🎉 All interactive GUI core features tested successfully!")
    return True

def test_multiple_maps():
    """Test loading multiple maps"""
    print("\n🗺️  Testing multiple map loading...")
    successful_loads = 0
    
    for map_id in range(1, 6):  # Test maps 1-5
        vehicles = import_map(map_id)
        if vehicles:
            state = State(vehicles)
            print(f"✅ Map {map_id}: {len(vehicles)} vehicles, solved: {state.is_solved()}")
            successful_loads += 1
        else:
            print(f"❌ Map {map_id}: Failed to load")
    
    print(f"\n📊 Successfully loaded {successful_loads}/5 maps")
    return successful_loads > 0

if __name__ == "__main__":
    print("🚀 Interactive GUI Feature Test Suite")
    print("=====================================")
    
    success = test_interactive_features()
    
    if success:
        test_multiple_maps()
        print("\n✅ All tests completed successfully!")
        print("🎮 The interactive GUI should work properly.")
    else:
        print("\n❌ Some tests failed. Check the issues above.")
        sys.exit(1)
