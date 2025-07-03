import heapq #priority queue usage
import sys
import os

# Add parent directory to path to access utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.state import State
from utils.vehicle import Vehicle
GRID_COL = 6
GRID_ROW = 6

def ucs(initial_state):
    pq = []
    counter = 0
    heapq.heappush(pq, (0, counter, initial_state, [])) # (cost, counter, state, path)
    frontier = set()
    
    while pq:
        cost, _, curr_state, path = heapq.heappop(pq)
        
        if (curr_state in frontier):
            continue
        
        if (curr_state.is_solved()):
            return cost, curr_state, path
        
        # Add to frontier
        frontier.add(curr_state)
        
        next_moves = curr_state.get_all_possible_moves()
        
        for v_id, move in next_moves:
           new_state = curr_state.move_vehicle(v_id, move)
           if new_state is None:
               continue
           
           # Check if new state has already been explored
           if new_state in frontier:
               continue
           
           move_cost = 1 * curr_state.get_vehicle_by_id(v_id).length
           new_path = path + [(v_id, move)]
           counter += 1
           heapq.heappush(pq, (cost + move_cost, counter, new_state, new_path))
           
           
    return None, -1, -1