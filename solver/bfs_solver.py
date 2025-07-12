import queue

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
                    return len(new_path), nodes_expanded, new_path
    return None, 0, nodes_expanded