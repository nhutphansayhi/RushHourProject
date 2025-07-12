import sys
import os
import queue

# Add parent directory to path to access utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import Vehicle, State, import_map

def bfs_solver(initial_state):
    
    if initial_state.is_solved():
        return [], 0, 0
    
    q = queue.Queue()
    q.put((initial_state, []))  # (state, path)
    visited = set()
    nodes_expanded = 0
    visited.add(initial_state.to_string())
    while not q.empty():
        current_state, path = q.get()
        nodes_expanded += 1
        possible_moves = current_state.get_all_possible_moves()
        
        for vehicle_id, direction in possible_moves:
            new_state = current_state.move_vehicle(vehicle_id, direction)
            
            if new_state is None: 
                continue
                
            state_string = new_state.to_string()
            
            if state_string not in visited:
                visited.add(state_string)
                new_path = path + [(vehicle_id, direction)]
                
                q.put((new_state, new_path))
                if new_state.is_solved():
                    # cost = 0
                    # for vehicle_id, _ in new_path:
                    #     cost += new_state.get_vehicle_by_id(vehicle_id).length
                    return len(new_path), nodes_expanded, new_path
    return None, 0, nodes_expanded

# def main():
#     """Test the BFS solver on multiple maps and show detailed statistics"""
#     print("🔍 BFS Solver Test - Rush Hour Puzzle")
#     print("=" * 50)
    
#     # Test maps
#     test_maps = [12]  # Include the newly created map12
    
#     total_solved = 0
#     total_time = 0
    
#     for map_id in test_maps:
#         print(f"\n📋 Testing Map {map_id}")
#         print("-" * 30)
        
#         try:
#             # Load map
#             vehicles = import_map(map_id)
#             if not vehicles:
#                 print(f"❌ Failed to load map{map_id}.txt")
#                 continue
            
#             print(f"Vehicles loaded: {len(vehicles)}")
#             for vehicle in vehicles:
#                 target_str = " (TARGET)" if vehicle.is_target else ""
#                 print(f"  {vehicle.id}: pos=({vehicle.row},{vehicle.col}), len={vehicle.length}, ori={vehicle.orientation}{target_str}")
            
#             # Create initial state
#             initial_state = State(vehicles)
            
#             # Check if already solved
#             if initial_state.is_solved():
#                 print("✅ Puzzle is already solved!")
#                 continue
            
#             # Run BFS solver
#             print("\n🚀 Running BFS solver...")
#             result = bfs_solver(initial_state)
            
#             if result and result[0] is not None:
#                 path, nodes_expanded, solve_time = result
#                 steps = len(path)
#                 total_solved += 1
#                 total_time += solve_time
                
#                 print(f"✅ SOLUTION FOUND!")
#                 print(f"   Steps: {steps}")
#                 print(f"   Nodes expanded: {nodes_expanded}")
#                 print(f"   Time: {solve_time:.3f} seconds")
#                 print(f"   Efficiency: {nodes_expanded/steps:.1f} nodes per step")
                
#                 # Show solution path if reasonable length
#                 if steps <= 15:
#                     print(f"\n📋 Solution Path:")
#                     for i, (vehicle_id, direction) in enumerate(path, 1):
#                         print(f"   {i:2d}. Move '{vehicle_id}' {direction}")
#                 else:
#                     print(f"\n📋 Solution has {steps} steps (too long to display)")
                
#                 # Verify solution
#                 print(f"\n🔍 Verifying solution...")
#                 current_state = initial_state
#                 for i, (vehicle_id, direction) in enumerate(path):
#                     current_state = current_state.move_vehicle(vehicle_id, direction)
#                     if current_state is None:
#                         print(f"❌ Invalid move at step {i+1}: {vehicle_id} {direction}")
#                         break
                
#                 if current_state and current_state.is_solved():
#                     print("✅ Solution verified successfully!")
#                 else:
#                     print("❌ Solution verification failed!")
                    
#             else:
#                 path, nodes_expanded, solve_time = result
#                 print(f"❌ NO SOLUTION FOUND")
#                 print(f"   Nodes expanded: {nodes_expanded}")
#                 print(f"   Time: {solve_time:.3f} seconds")
                
#         except Exception as e:
#             print(f"💥 Error testing map {map_id}: {str(e)}")
#             import traceback
#             traceback.print_exc()
    
#     # Summary
#     print(f"\n{'='*50}")
#     print(f"📊 SUMMARY")
#     print(f"{'='*50}")
#     print(f"Maps tested: {len(test_maps)}")
#     print(f"Solutions found: {total_solved}")
#     print(f"Success rate: {(total_solved/len(test_maps)*100):.1f}%")
#     if total_solved > 0:
#         print(f"Average solve time: {total_time/total_solved:.3f} seconds")

# if __name__ == "__main__":
#     main()

