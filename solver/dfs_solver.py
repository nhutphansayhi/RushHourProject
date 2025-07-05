def dfs_solver(start_state, max_depth=1000):
    stack = [(start_state, [])]  # (current_state, path_so_far)
    visited = set()

    while stack:
        current_state, path = stack.pop()
        state_key = current_state.to_string()

        if state_key in visited:
            continue
        visited.add(state_key)

        if current_state.is_solved():
            return path  # List of (vehicle_id, direction) moves

        if len(path) >= max_depth:
            continue  # Prevent infinite loops

        for move in current_state.get_all_possible_moves():
            vehicle_id, direction = move
            new_state = current_state.move_vehicle(vehicle_id, direction)
            if new_state:
                stack.append((new_state, path + [move]))

    return None  # No solution found