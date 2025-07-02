import heapq #priority queue usage

GRID_COL = 6
GRID_ROW = 6

# State: 
#   - list() of occupied positioned of the vehicle
#   - vertical or horizontal
#

class Vehicle: 
    def __init__(self, vehicle_id, positions, orientation):
        self.id = vehicle_id
        self.positions = positions
        self.orientation = orientation
        self.length = len(positions)
    
    def get_start_position(self):
        """Top-left position of the vehicle"""
        return min(self.positions)
    
    def get_end_position(self):
        """Bottom-right position of the vehicle"""
        return max(self.positions)


# State as dictionary mapping vehicle_id to list of positions
state = {
    'A': [(2, 1), (2, 2)],           # Target car (horizontal)
    'B': [(0, 0), (0, 1), (0, 2)],   # Truck (horizontal) 
    'C': [(3, 0), (4, 0), (5, 0)]    # Truck (vertical)
}

def is_horizontal(current_state, vehicle):
    return current_state[vehicle][0][0] == current_state[vehicle][1][0]
        
        
def try_move_vehicle(state, vehicle_id, direction):
    new_positions = []
    if (direction == 'left'):
        for pos in state[vehicle_id]:
            if (pos[1] - 1 < 0):
                return None
            new_positions.append((pos[0], pos[1] - 1))
        
            
    if (direction == 'right'):
        for pos in state[vehicle_id]:
            if (pos[1] + 1 >= GRID_COL):
                return None
            new_positions.append((pos[0], pos[1] + 1))
        
        
    if (direction == 'up'):
        for pos in state[vehicle_id]:
            if (pos[0] - 1 < 0):
                return None
            new_positions.append((pos[0] - 1, pos[1]))
        
        
    if (direction == 'down'):
        for pos in state[vehicle_id]:
            if (pos[0] + 1 >= GRID_ROW):
                return None
            new_positions.append((pos[0] + 1, pos[1]))
    
    # Check Collision
    for other_vehicle_id, other_positions in state.items():
        if (other_vehicle_id != vehicle_id):
            for new_pos in new_positions:
                if (new_pos in other_positions):
                    return None
    
    # Return the new state
    new_state = state.copy()
    new_state[vehicle_id] = new_positions
        
    return new_state
        


def get_valid_moves(current_state):
    valid_moves = []
    
    for vehicle_id in current_state:
        if (is_horizontal(current_state, vehicle_id)):
            new_state_left = try_move_vehicle(current_state, vehicle_id, 'left')
            new_state_right = try_move_vehicle(current_state, vehicle_id, 'right')
            if new_state_left:
                valid_moves.append(new_state_left)
            if new_state_right:
                valid_moves.append(new_state_right)
            
        else:
            new_state_up = try_move_vehicle(current_state, vehicle_id, 'up')
            new_state_down = try_move_vehicle(current_state, vehicle_id, 'down')
            if new_state_up:
                valid_moves.append(new_state_up)
            if new_state_down:
                valid_moves.append(new_state_down)
            
    return valid_moves

def goal_state(current_state):
    target_car = 'A'
    curr_pos = current_state[target_car]
    rightmost_col = max(pos[1] for pos in curr_pos)
    
    exit_row = 2
    is_on_exit_row = all(pos[0] == exit_row for pos in curr_pos)
    can_exit = rightmost_col >= 4
    
    return is_on_exit_row and can_exit

def state_to_hash(curr_state):
    return tuple(sorted((vehicle_id, tuple(positions)) for vehicle_id, positions in curr_state.items()))

def ucs(initial_state):
    pq = []
    counter = 0
    heapq.heappush(pq, (0, counter, initial_state, [])) # (cost, counter, state, path)
    frontier = set()
    
    while pq:
        cost, _, curr_state, path = heapq.heappop(pq)
        
        curr_state_hash = state_to_hash(curr_state)
        
        if (curr_state_hash in frontier):
            continue
        
        if (goal_state(curr_state)):
            return cost, curr_state, path
        
        frontier.add(curr_state_hash)
        
        next_moves = get_valid_moves(curr_state)
        for move in next_moves:
            move_hash = state_to_hash(move)
            if (move_hash not in frontier):
                # Find which vehicle moved by comparing curr_state and move
                moved_vehicle = None
                for vehicle_id in curr_state:
                    if curr_state[vehicle_id] != move[vehicle_id]:
                        moved_vehicle = vehicle_id
                        break
                
                # Calculate cost based on vehicle length
                vehicle_length = len(curr_state[moved_vehicle])
                move_cost = 1 * vehicle_length
                
                new_path = path + [move]
                counter += 1
                heapq.heappush(pq, (cost + move_cost, counter, move, new_path))
        
    return None, -1, -1

def display_map(state):
    """
    Displays the Rush Hour grid based on the current state.
    """
    grid = [['.' for _ in range(GRID_COL)] for _ in range(GRID_ROW)]

    for vehicle_id, positions in state.items():
        for row, col in positions:
            grid[row][col] = vehicle_id

    for row in grid:
        print(' '.join(row))
    print("-" * (2 * GRID_COL - 1))

def load_map_from_file(filename):
    """
    Load a map from a text file and return the state dictionary.
    Format: VehicleID: [(row1, col1), (row2, col2), ...]
    """
    import os
    import ast
    
    # Get the path to the map file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(os.path.dirname(current_dir), 'map', filename)
    
    state = {}
    try:
        with open(map_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Parse lines like "A: [(2, 1), (2, 2)]"
                    vehicle_id, positions_str = line.split(': ')
                    positions = ast.literal_eval(positions_str)
                    state[vehicle_id] = positions
    except FileNotFoundError:
        print(f"Map file {filename} not found.")
        return None
    except Exception as e:
        print(f"Error loading map {filename}: {e}")
        return None
    
    return state

if __name__ == "__main__":
    # Test cases using map files
    test_files = [
        ("test_simple.txt", "Simple solvable puzzle", True),
        ("test_solved.txt", "Already solved puzzle", True),
        ("test_unsolvable.txt", "Unsolvable puzzle", False),
        ("test_complex.txt", "Complex solvable puzzle", True)
    ]

    for i, (filename, description, expected) in enumerate(test_files):
        print(f"Running Test Case {i + 1}: {description}")
        
        initial_state = load_map_from_file(filename)
        if initial_state is None:
            print(f"Failed to load {filename}")
            continue
            
        print("Initial state:")
        display_map(initial_state)
        
        result = ucs(initial_state)
        
        if len(result) == 3 and result[0] is not None:
            cost, final_state, path = result
            print("Final state:")
            display_map(final_state)
            solution_found = True
        else:
            cost, final_state, path = None, None, []
            solution_found = False

        print(f"Expected: {expected}, Got: {solution_found}")
        print("Path to solution:" if solution_found else "No solution found.")
        if solution_found:
            print(f'Cost: {cost}')
            print("Solution path:")
            for step_num, step in enumerate(path, 1):
                print(f"Step {step_num}:")
                display_map(step)
        print("-" * 40)



