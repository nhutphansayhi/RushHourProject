from collections import deque
import copy
import time
import heapq
from queue import Queue
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.vehicle import Vehicle
from utils.state import State

# Lớp PriorityQueue đã sửa
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def put(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))  # Sử dụng priority trực tiếp
        self._index += 1

    def get(self):
        if self.is_empty():
            raise IndexError("Cannot get from an empty priority queue.")
        return heapq.heappop(self._queue)[2]

    def is_empty(self):
        return len(self._queue) == 0

    def size(self):
        return len(self._queue)

# Hàm heuristic
# def heuristic(state):
#     grid = [["_"]*6 for _ in range(6)]
#     for vehicle in state.vehicles:
#         if vehicle[3] == "H":
#             for i in range(vehicle[4]):
#                 grid[vehicle[1]][vehicle[2] + i] = vehicle[0]
#         elif vehicle[3] == "V":
#             for i in range(vehicle[4]):
#                 grid[vehicle[1] + i][vehicle[2]] = vehicle[0]
    
#     # Đếm số ô bị chặn trên đường của X
#     heu = 0
#     x_pos = None
#     for vehicle in state.vehicles:
#         if vehicle[0] == "X":
#             x_pos = vehicle[2]  # Vị trí cột của X
#             break
    
#     # Kiểm tra từ sau X đến cột 5 trên hàng 2
#     for col in range(x_pos + 2, 6):
#         if grid[2][col] != "_":
#             heu += 1
    
#     return heu

def routeShouldEmptyOfVehicle(vehicle,vehicleCenter,state):# vehicleCenter: [1,2]
    route = []
    
    if (vehicle[0] == "X"):
        for i in range(vehicle[2]+2 ,6):
            route.append([vehicle[1], i])  
    elif (vehicle[3] == "H"):
        From = max(0,vehicleCenter[1]- vehicle[4]) 
        To = min (5,vehicleCenter[1] + vehicle[4]) + 1 # +1 for the threshold of for
        for i in range(From,To):
            route.append([vehicle[1],i])
    elif (vehicle[3] == "V"):
        From = max(0,vehicleCenter[0] - vehicle[4])
        To = min (5,vehicleCenter[0] + vehicle[4]) + 1 # +1 for the threshold of for
        for i in range(From,To):
            route.append([i,vehicle[2]])
    return route


def heuristic(state):
    
    # tạo bảng đồ có tên xe từng đoạn
    grid = [["_"]*6 for _ in range(6)]
    for vehicle in state.vehicles:
        if vehicle[3] == "H":
            for i in range(vehicle[4]):
                try:
                    grid[vehicle[1]][vehicle[2] + i] = vehicle[0]
                except:
                    print("H:",vehicle[1],vehicle[2] + i)
        if vehicle[3] == "V":
            for i in range(vehicle[4]):
                try:
                    grid[vehicle[1] + i][vehicle[2]] = vehicle[0]
                except:
                    print("V:",vehicle[1] + i,vehicle[2])
    
    


    heu = 0
    cores = Queue() # core = [[pairOfVehicle,position],...] / put get
    # lấy center -> không cần 
    # tính heuristic luôn
    queue = Queue() # vehicle, position be run over 
    queue.put([state.vehicles[0],[]])  # vehicles and positions of it which got run over
    NodeExpanded = [] #pair of name, name 1 is vehicle run over, name 2 is vehicle got run over, => NodeExpand = [[A,B],[C,D]]
    while not queue.empty(): 
        vehicle_vehicleCenter = queue.get()  
        vehicle = vehicle_vehicleCenter[0]
        position = vehicle_vehicleCenter[1]
        vehicleRunOver = vehicle[0]
        
        for pos in routeShouldEmptyOfVehicle(vehicle ,position ,state): 
            if grid[pos[0]][pos[1]] != ".":
                vehicleGotRunOver = grid[pos[0]][pos[1]] 
                flag = True
                #kiem tra xem co trong NodeExpanded chưa
                if vehicleRunOver == vehicleGotRunOver:
                    flag = False
                    continue 
                for pairOfVehicle in NodeExpanded: # NodeExpanđe = [[A,B], [D,E], ...]
                    if  (pairOfVehicle[0] == vehicleRunOver and pairOfVehicle[1] == vehicleGotRunOver ):
                        flag = False 
                        break
                if flag: # đảm bảo các pairs khác nhau và đảm bảo không cán lên chính nó 
                    NodeExpanded.append([vehicleRunOver,vehicleGotRunOver]) # NodeExpand là trong toàn giai đoạn 
                    cores.put([[vehicleRunOver, vehicleGotRunOver],pos]) 
                elif flag == False:
                    continue 
        
                
        while not cores.empty(): # cores =[ [[A,B],[1,2]] , [[D,C],[5,3]] ,...]
            heu+=1
            core = cores.get()
            for vehicle in state.vehicles:
                if  core[0][1] == vehicle[0]:
                    queue.put([vehicle,core[1]])  
    return heu




# Thuật toán A*
def aStart_solver(initial_state):
    start_time = time.time()
    queue = PriorityQueue()
    queue.put((initial_state, []), heuristic(initial_state))
    visited = set()
    nodes_expanded = 0
    
    while not queue.is_empty():
        state, path = queue.get()
        
        if str(state.vehicles) in visited:
            continue
        visited.add(str(state.vehicles))
        nodes_expanded += 1
        
        if is_goal(state):
            end_time = time.time()
            return path, nodes_expanded, end_time - start_time
        
        for move in get_valid_moves(state):
            new_state = make_move(state, move)
            if str(new_state.vehicles) not in visited:
                new_path = path + [move]
                g_cost = len(new_path)
                h_cost = heuristic(new_state)
                f_cost = g_cost + h_cost
                queue.put((new_state, new_path), f_cost)
    
    return None, nodes_expanded, time.time() - start_time

# Dữ liệu đầu vào
# initial_vehicles = [
#     ["X", 2, 0, "H", 2],
#     ["A", 4, 0, "V", 2],
#     ["B", 4, 1, "H", 3],
#     ["C", 4, 4, "V", 2],
#     ["D", 2, 3, "V", 2],
#     ["E", 2, 4, "V", 2],
#     ["F", 1, 5, "V", 3],
#     ["G", 0, 3, "V", 2],
#     ["H", 0, 4, "H", 2]
# ]
initial_vehicles = [
    ["X",2,0,"H",2],
    ["A",3,1,"V",2],
    ["B",0,2,"V",3],
    ["C",4,2,"H",2],
    ["D",3,4,"V",3],
    ["E",1,5,"V",2]
]
initial_state = State(initial_vehicles)

# Chạy và hiển thị kết quả
print("Step 0:")
for line in initial_state.vehicles:
    print(line)
solution, nodes_expanded, search_time = aStart_solver(initial_state)
if solution:
    print(f"Solution found with {len(solution)} moves:")
    current_state = initial_state
    for i, move in enumerate(solution, 1):
        vehicle_idx, direction = move
        vehicle_id = current_state.vehicles[vehicle_idx][0]
        # Logic in hướng đã sửa
        if current_state.vehicles[vehicle_idx][3] == "H":
            direction_str = "left" if direction == -1 else "right"
        else:
            direction_str = "up" if direction == -1 else "down"
        print(f"Step {i}: Move vehicle {vehicle_id} {direction_str}")
        current_state = make_move(current_state, move)
        print_grid(current_state)
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Search time: {search_time:.4f} seconds")
else:
    print("No solution found")