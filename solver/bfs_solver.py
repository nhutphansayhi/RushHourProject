from utils import Vehicle, State, import_map
import queue
import time

def bfs_solver(initial_state):
    start_time = time.time()
    
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
                
                if new_state.is_solved():
                    end_time = time.time()
                    return new_path, nodes_expanded, end_time - start_time
                
                q.put((new_state, new_path))
    return None, nodes_expanded, time.time() - start_time

def __main__: 
    map = {
        ["X",2,0,"H",2],
        ["A",3,1,"V",2],
        ["B",0,2,"V",3],
        ["C",4,2,"H",2],
        ["D",3,4,"V",3],
        ["E",1,5,"V",2]
    }