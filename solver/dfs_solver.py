import sys

sys.setrecursionlimit(5000)

def dfs_handler(current_state, path, visited, node_expanded, cancel_flag):
    
    if cancel_flag and cancel_flag.is_set():
            return None
    
    node_expanded[0] += 1
    state_key = current_state.to_string()

    if state_key in visited:
        return None
    visited.add(state_key)

    if current_state.is_solved():
        return path

    for move in current_state.get_all_possible_moves():
        vehicle_id, direction = move
        new_state = current_state.move_vehicle(vehicle_id, direction)
        if new_state:
            result = dfs_handler(new_state, path + [move], visited, node_expanded, cancel_flag)
            if result is not None:
                return result

    return None

def dfs_solver(start_state, cancel_flag=None):
    visited = set()
    node_expanded = [0]
    path = dfs_handler(start_state, [], visited, node_expanded, cancel_flag)

    if path is not None:
        return len(path), node_expanded[0], path
    else:
        return None, 0, []
