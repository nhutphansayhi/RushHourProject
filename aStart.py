from collections import deque
import copy
import time
from queue import Queue
# Biểu diễn trạng thái trò chơi
class State:
    def __init__(self, vehicles):
        self.vehicles = vehicles  # Danh sách các xe: [[ID, row/col, direction, length], ...]
    
    def __eq__(self, other):
        return self.vehicles == other.vehicles
    
    def __hash__(self):
        return hash(str(self.vehicles))

# Kiểm tra trạng thái mục tiêu
def is_goal(state):
    for vehicle in state.vehicles:
        if vehicle[0] == "X":  # Xe mục tiêu
            if vehicle[3] == "H" and vehicle[2] + vehicle[4] - 1 == 5:  # Xe ngang, đạt cột 6
                return True
    return False

# Lấy các bước di chuyển hợp lệ
def get_valid_moves(state):
    moves = []
    grid = [[0]*6 for _ in range(6)]  # Lưới 6x6, 0 là ô trống, 1 là ô bị chiếm
    
    # Đánh dấu các ô bị chiếm
    for vehicle in state.vehicles:
        row, col, direction, length = vehicle[1], vehicle[2], vehicle[3], vehicle[4]
        if direction == "H":
            for c in range(col, col + length):
                grid[row][c] = 1
        else:  # direction == "V"
            for r in range(row, row + length):
                grid[r][col] = 1
    
    # Kiểm tra từng xe
    for i, vehicle in enumerate(state.vehicles):
        row, col, direction, length = vehicle[1], vehicle[2], vehicle[3], vehicle[4]
        if direction == "H":
            # Di chuyển trái
            if col > 0 and grid[row][col-1] == 0:
                moves.append((i, -1))  # Di chuyển xe i về trái 1 ô
            # Di chuyển phải
            if col + length < 6 and grid[row][col + length] == 0:
                moves.append((i, 1))  # Di chuyển xe i về phải 1 ô
        else:  # direction == "V"
            # Di chuyển lên
            if row > 0 and grid[row-1][col] == 0:
                moves.append((i, -1))  # Di chuyển xe i lên 1 ô
            # Di chuyển xuống
            if row + length < 6 and grid[row + length][col] == 0:
                moves.append((i, 1))  # Di chuyển xe i xuống 1 ô
    return moves

# Tạo trạng thái mới sau khi di chuyển
def make_move(state, move):
    vehicle_idx, direction = move
    new_vehicles = copy.deepcopy(state.vehicles)
    vehicle = new_vehicles[vehicle_idx]
    if vehicle[2] == "H":
        vehicle[1] += direction  # Cập nhật cột
    else:
        vehicle[1] += direction  # Cập nhật hàng
    return State(new_vehicles)

# Hiển thị lưới để dễ hình dung
def print_grid(state):
    grid = [["."]*6 for _ in range(6)]
    for vehicle in state.vehicles:
        row, col, direction, length = vehicle[1], vehicle[1], vehicle[2], vehicle[3]
        vehicle_id = vehicle[0]
        if direction == "H":
            for c in range(col, col + length):
                grid[row][c] = vehicle_id
        else:
            for r in range(row, row + length):
                grid[r][col] = vehicle_id
    for row in grid:
        print(" ".join(row))
    print()

# Thuật toán BFS
def bfs_solver(initial_state):
    start_time = time.time()
    queue = deque([(initial_state, [])])
    visited = set()
    nodes_expanded = 0
    
    while queue:
        state, path = queue.popleft()
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
                queue.append((new_state, new_path))
    
    return None, nodes_expanded, time.time() - start_time


# [S]Declare for priority queue of web
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []  # Internal list to store elements as a min-heap
        self._index = 0   # Used to handle tie-breaking for elements with same priority

    def put(self, item, priority):
        """
        Inserts an item into the priority queue with a given priority.
        Lower priority values indicate higher priority.
        """
        # We store a tuple: (-priority, index, item)
        # The negative priority ensures min-heap behavior for highest priority items.
        # The index is for stable sorting (FIFO) when priorities are equal.
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def get(self):
        """
        Removes and returns the item with the highest priority.
        """
        if self.is_empty():
            raise IndexError("Cannot get from an empty priority queue.")
        # We only return the actual item, discarding priority and index.
        return heapq.heappop(self._queue)[2]

    def is_empty(self):
        """
        Checks if the priority queue is empty.
        """
        return len(self._queue) == 0

    def size(self):
        """
        Returns the number of items in the priority queue.
        """
        return len(self._queue)
# [E]Declare for priority queue of web

    


# Map phức tạp
# initial_vehicles = [
#     ["X", 2, 2, "H", 2],  
#     ["A", 3, 1, "V", 2],  
#     ["B", 3, 2, "V", 3],  
#     ["C", 0, 4, "V", 3],  
#     ["D", 1, 5, "V", 2],  
#     ["E", 4, 4, "H", 2]
# ]

initial_vehicles = [
    ["X",2,0,"H",2],
    ["A",4,0,"V",2],
    ["B",4,1,"H",3],
    ["C",4,4,"V",2],
    ["D",2,3,"V",2],
    ["E",2,4,"V",2],
    ["F",1,5,"V",3],
    ["G",0,3,"V",2],
    ["H",0,4,"H",2]
]
initial_state = State(initial_vehicles)

def routeShouldEmptyOfVehicle(vehicle,vehicleCenter,state):# vehicleCenter: [1,2]
    route = []
    
    if (vehicle[0] == "X"):
        for i in range(6):
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
    
    for i in range(len(grid)):
        print(grid[i])


    heu = 0
    cores = Queue() # core = [[pairOfVehicle,position],...] / put get
    # lấy center -> không cần 
    # tính heuristic luôn
    array = [] # chỉ để debug
    queue = Queue() # vehicle, position be run over 
    queue.put([state.vehicles[0],[]])  # vehicles and positions of it which got run over
    NodeExpanded = [] #pair of name, name 1 is vehicle run over, name 2 is vehicle got run over, => NodeExpand = [[A,B],[C,D]]
    while not queue.empty(): 
        for i in list(queue.queue):
            array.append(i)
        vehicle_vehicleCenter = queue.get()  
        vehicle = vehicle_vehicleCenter[0]
        position = vehicle_vehicleCenter[1]
        vehicleRunOver = vehicle[0]
        
        for pos in routeShouldEmptyOfVehicle(vehicle ,position ,state): 
            if grid[pos[0]][pos[1]] != "_":
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

print(heuristic(initial_state))

# Chạy BFS và hiển thị kết quả
# print("Initial grid:")
# print_grid(initial_state)




# solution, nodes_expanded, search_time = bfs_solver(initial_state)
# if solution:
#     print(f"Solution found with {len(solution)} moves:")
#     current_state = initial_state
#     for i, move in enumerate(solution, 1):
#         vehicle_idx, direction = move
#         vehicle_id = current_state.vehicles[vehicle_idx][0]
#         direction_str = "left" if direction == -1 else "right" if current_state.vehicles[vehicle_idx][2] == "H" else "up" if direction == -1 else "down"
#         print(f"Step {i}: Move vehicle {vehicle_id} {direction_str}")
#         current_state = make_move(current_state, move)
#         print_grid(current_state)
#     print(f"Nodes expanded: {nodes_expanded}")
#     print(f"Search time: {search_time:.4f} seconds")
# else:
#     print("No solution found")

 
# Uncomment dòng dưới để chạy
# main()