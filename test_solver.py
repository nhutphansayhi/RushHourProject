from solver.bfs_solver import bfs_solver
from utils import import_map, State

def main():
    # Load puzzle
    vehicles = import_map(1)
    initial_state = State(vehicles)
    
    print("Solving puzzle with BFS...")
    initial_state.display()
    
    # Solve with BFS
    solution, nodes, time_taken = bfs_solver(initial_state)
    
    if solution:
        print(f"\n🎉 SOLVED in {len(solution)} moves!")
        print(f"📊 Stats: {nodes} states explored, {time_taken:.3f}s")
        
        # Show solution steps
        current_state = initial_state
        for i, (vehicle_id, direction) in enumerate(solution, 1):
            print(f"\nStep {i}: Move {vehicle_id} {direction}")
            # Apply move to show progression
            new_vehicles = []
            for v in current_state.vehicles:
                if v.id == vehicle_id:
                    new_vehicles.append(v.move(direction))
                else:
                    new_vehicles.append(v)
            current_state = State(new_vehicles)
            current_state.display()
    else:
        print("❌ No solution found!")

if __name__ == "__main__":
    main()
