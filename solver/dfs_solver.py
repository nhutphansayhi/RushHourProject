import sys
import os
import time

def dfs(start_state, max_depth=100000):
    stack = [(start_state, [])]  # (current_state, path_so_far)
    visited = set()
#    node_expandeds = 0
#    start_time = time.time()

    while stack:
        current_state, path = stack.pop()
#        node_expandeds += 1
        state_key = current_state.to_string()

        if state_key in visited:
            continue
        visited.add(state_key)

        if current_state.is_solved():
            return path#, node_expandeds, time.time() - start_time   # List of (vehicle_id, direction) moves

        if len(path) >= max_depth:
            continue  # Prevent infinite loops

        for move in current_state.get_all_possible_moves():
            vehicle_id, direction = move
            new_state = current_state.move_vehicle(vehicle_id, direction)
            if new_state:
                stack.append((new_state, path + [move]))

    return None#, node_expandeds, time.time() - start_time  # No solution found