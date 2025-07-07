import heapq #priority queue usage
import sys
import os

# Add parent directory to path to access utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.state import State
from utils.vehicle import Vehicle
GRID_COL = 6
GRID_ROW = 6

def ucs(initial_state):
    pq = []
    counter = 0
    expanded_nodes = 0
    heapq.heappush(pq, (0, counter, initial_state, [])) # (cost, counter, state, path)
    frontier = set()
    
    while pq:
        cost, _, curr_state, path = heapq.heappop(pq)
        
        if (curr_state in frontier):
            continue
        
        if (curr_state.is_solved()):
            return cost, expanded_nodes, path
        
        # Add to frontier and increment expanded nodes
        frontier.add(curr_state)
        expanded_nodes += 1
        
        next_moves = curr_state.get_all_possible_moves()
        
        for v_id, move in next_moves:
           new_state = curr_state.move_vehicle(v_id, move)
           if new_state is None:
               continue
           
           # Check if new state has already been explored
           if new_state in frontier:
               continue
           
           move_cost = 1 * curr_state.get_vehicle_by_id(v_id).length
           new_path = path + [(v_id, move)]
           counter += 1
           heapq.heappush(pq, (cost + move_cost, counter, new_state, new_path))
           
           
    return None, expanded_nodes, []

def test_ucs_solver():
    """Test the UCS solver and verify it returns cost, expanded_nodes, and path"""
    import sys
    import os
    
    # Add parent directory to path to access utils
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    
    from utils.utils import import_map
    
    print("🧪 UCS Solver Test - Return Format Verification")
    print("=" * 60)
    
    # Test maps that should have solutions
    test_maps = [1, 2, 3, 4]
    
    for map_id in test_maps:
        print(f"\n📋 Testing Map {map_id}")
        print("-" * 30)
        
        try:
            # Load map
            vehicles = import_map(map_id)
            if not vehicles:
                print(f"❌ Failed to load map{map_id}.txt")
                continue
            
            print(f"Vehicles loaded: {len(vehicles)}")
            
            # Create initial state
            initial_state = State(vehicles)
            
            # Check if already solved
            if initial_state.is_solved():
                print("✅ Puzzle is already solved!")
                continue
            
            # Run UCS solver
            print("🚀 Running UCS solver...")
            result = ucs(initial_state)
            
            # Verify return format
            if len(result) != 3:
                print(f"❌ ERROR: Expected 3 return values, got {len(result)}")
                continue
            
            cost, expanded_nodes, path = result
            
            # Check return types
            if cost is None:
                print(f"❌ NO SOLUTION FOUND")
                print(f"   Expanded nodes: {expanded_nodes}")
                print(f"   Path: {path}")
            else:
                print(f"✅ SOLUTION FOUND!")
                print(f"   Cost: {cost} (type: {type(cost).__name__})")
                print(f"   Expanded nodes: {expanded_nodes} (type: {type(expanded_nodes).__name__})")
                print(f"   Path length: {len(path)} (type: {type(path).__name__})")
                
                # Verify path format
                if isinstance(path, list) and len(path) > 0:
                    print(f"   First move: {path[0]}")
                    print(f"   Last move: {path[-1]}")
                
                # Verify solution by applying path
                print("🔍 Verifying solution...")
                current_state = initial_state
                for i, (vehicle_id, direction) in enumerate(path):
                    current_state = current_state.move_vehicle(vehicle_id, direction)
                    if current_state is None:
                        print(f"❌ Invalid move at step {i+1}: {vehicle_id} {direction}")
                        break
                
                if current_state and current_state.is_solved():
                    print("✅ Solution verified successfully!")
                    print(f"   Algorithm efficiency: {expanded_nodes/len(path):.1f} nodes per step")
                else:
                    print("❌ Solution verification failed!")
                    
        except Exception as e:
            print(f"💥 ERROR: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 UCS Solver test completed!")

if __name__ == "__main__":
    test_ucs_solver()