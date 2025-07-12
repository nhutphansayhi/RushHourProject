def dfs_solver(start_state, max_depth=100000):
    stack = [(start_state, [])]  # (current_state, path_so_far)
    visited = set()
    node_expanded = 0

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