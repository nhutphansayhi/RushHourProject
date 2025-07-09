from collections import deque
import copy
import time
import heapq
from queue import Queue

# Biểu diễn trạng thái trò chơi
class State:
    def __init__(self, vehicles):
        self.vehicles = vehicles  # Danh sách các xe: [[ID, row, col, direction, length], ...]
    
    def __eq__(self, other):
        return self.vehicles == other.vehicles
    
    def __hash__(self):
        return hash(str(self.vehicles))

# Kiểm tra trạng thái mục tiêu
def is_goal(state):
    for vehicle in state.vehicles:
        if vehicle[0] == "X":  # Xe mục tiêu
            if vehicle[3] == "H" and vehicle[2] + vehicle[4] - 1 == 5:  # Xe ngang, đạt cột 5
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
                if 0 <= row < 6 and 0 <= c < 6:
                    grid[row][c] = 1
        else:  # direction == "V"
            for r in range(row, row + length):
                if 0 <= r < 6 and 0 <= col < 6:
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
    if vehicle[3] == "H":  # Xe ngang
        vehicle[2] += direction  # Cập nhật cột
    else:  # Xe dọc
        vehicle[1] += direction  # Cập nhật hàng
    return State(new_vehicles)

# Hiển thị lưới để dễ hình dung
def print_grid(state):
    grid = [["."]*6 for _ in range(6)]
    for vehicle in state.vehicles:
        row, col, direction, length = vehicle[1], vehicle[2], vehicle[3], vehicle[4]
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

# Thuật toán A* với heapq
def aStart_solver(initial_state):
    start_time = time.time()
    queue = []
    counter = 0  # Để tránh so sánh State objects
    
    # Push vào heap: (f_cost, counter, state, path)
    heapq.heappush(queue, (heuristic(initial_state), counter, initial_state, []))
    counter += 1
    
    visited = set()
    nodes_expanded = 0
    
    while queue:  # Thay vì queue.is_empty()
        # Pop từ heap: bỏ qua f_cost và counter
        _, _, state, path = heapq.heappop(queue)
        
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
                
                # Push vào heap với counter
                heapq.heappush(queue, (f_cost, counter, new_state, new_path))
                counter += 1
    
    return None, nodes_expanded, time.time() - start_time

# Dữ liệu đầu vào
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