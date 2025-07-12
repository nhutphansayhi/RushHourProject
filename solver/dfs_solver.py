import sys
sys.setrecursionlimit(5000)

def dfs_handler(current_state, path, visited, node_expanded):
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
            result = dfs_handler(new_state, path + [move], visited, node_expanded)
            if result is not None:
                return result

    return None

def dfs_solver(start_state):
    visited = set()
    node_expanded = [0]
    path = dfs_handler(start_state, [], visited, node_expanded)

<<<<<<< HEAD
    while stack:
        current_state, path = stack.pop()
        node_expanded += 1
        state_key = current_state.to_string()

        if state_key in visited:
            continue
        visited.add(state_key)

        if current_state.is_solved():
            cost = 0
            for vehicle_id, _ in path:
                cost += current_state.get_vehicle_by_id(vehicle_id).length
            return cost, node_expanded, path

        if len(path) >= max_depth:
            continue  # Prevent infinite loops

        for move in current_state.get_all_possible_moves():
            vehicle_id, direction = move
            new_state = current_state.move_vehicle(vehicle_id, direction)
            if new_state:
                stack.append((new_state, path + [move]))

    return None, 0, []
=======
    if path is not None:
        return len(path), node_expanded[0], path
    else:
        return None, 0, []
>>>>>>> 70fd0b924307a5c4b2707570d70c185b611d15c6
