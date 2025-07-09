from collections import deque
import copy
import time
import heapq

# Biểu diễn trạng thái trò chơi
class State:
    def __init__(self, vehicles):
        self.vehicles = vehicles
        self._hash = None  # Cache hash value
        self._str = None   # Cache string representation
    
    def __eq__(self, other):
        return self.vehicles == other.vehicles
    
    def __hash__(self):
        if self._hash is None:
            self._hash = hash(str(self.vehicles))
        return self._hash
    
    def __str__(self):
        if self._str is None:
            self._str = str(self.vehicles)
        return self._str

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
                moves.append((i, -1))
            # Di chuyển phải
            if col + length < 6 and grid[row][col + length] == 0:
                moves.append((i, 1))
        else:  # direction == "V"
            # Di chuyển lên
            if row > 0 and grid[row-1][col] == 0:
                moves.append((i, -1))
            # Di chuyển xuống
            if row + length < 6 and grid[row + length][col] == 0:
                moves.append((i, 1))
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

# Lớp PriorityQueue đã tối ưu
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def put(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def get(self):
        if self.is_empty():
            raise IndexError("Cannot get from an empty priority queue.")
        return heapq.heappop(self._queue)[2]

    def is_empty(self):
        return len(self._queue) == 0

    def size(self):
        return len(self._queue)

def routeShouldEmptyOfVehicle(vehicle, vehicleCenter, state):
    route = []
    
    if vehicle[0] == "X":
        for i in range(vehicle[2] + 2, 6):
            route.append([vehicle[1], i])
    elif vehicle[3] == "H":
        From = max(0, vehicleCenter[1] - vehicle[4])
        To = min(5, vehicleCenter[1] + vehicle[4]) + 1
        for i in range(From, To):
            route.append([vehicle[1], i])
    elif vehicle[3] == "V":
        From = max(0, vehicleCenter[0] - vehicle[4])
        To = min(5, vehicleCenter[0] + vehicle[4]) + 1
        for i in range(From, To):
            route.append([i, vehicle[2]])
    return route

def heuristic(state):
    # Tạo bảng đồ có tên xe từng đoạn
    grid = [["_"]*6 for _ in range(6)]
    for vehicle in state.vehicles:
        if vehicle[3] == "H":
            for i in range(vehicle[4]):
                if 0 <= vehicle[1] < 6 and 0 <= vehicle[2] + i < 6:
                    grid[vehicle[1]][vehicle[2] + i] = vehicle[0]
        elif vehicle[3] == "V":
            for i in range(vehicle[4]):
                if 0 <= vehicle[1] + i < 6 and 0 <= vehicle[2] < 6:
                    grid[vehicle[1] + i][vehicle[2]] = vehicle[0]
    
    heu = 0
    cores = []  # Thay Queue bằng list để tối ưu
    queue = []  # Thay Queue bằng list để tối ưu
    queue.append([state.vehicles[0], []])
    NodeExpanded = set()
    
    while queue:
        vehicle_vehicleCenter = queue.pop(0)
        vehicle = vehicle_vehicleCenter[0]
        position = vehicle_vehicleCenter[1]
        vehicleRunOver = vehicle[0]
        
        for pos in routeShouldEmptyOfVehicle(vehicle, position, state):
            if 0 <= pos[0] < 6 and 0 <= pos[1] < 6 and grid[pos[0]][pos[1]] != "_":
                vehicleGotRunOver = grid[pos[0]][pos[1]]
                
                if vehicleRunOver == vehicleGotRunOver:
                    continue
                
                # Tối ưu: kiểm tra cả 2 chiều trong 1 lần
                pair = (vehicleRunOver, vehicleGotRunOver)
                pair_reverse = (vehicleGotRunOver, vehicleRunOver)
                
                if pair not in NodeExpanded and pair_reverse not in NodeExpanded:
                    NodeExpanded.add(pair)
                    cores.append([[vehicleRunOver, vehicleGotRunOver], pos])
        
        while cores:
            heu += 1
            core = cores.pop(0)
            
            # Tối ưu: break sớm khi tìm thấy
            for vehicle in state.vehicles:
                if core[0][1] == vehicle[0]:
                    queue.append([vehicle, core[1]])
                    break
    
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
        
        # Sử dụng cached string representation
        state_str = str(state)
        if state_str in visited:
            continue
        visited.add(state_str)
        nodes_expanded += 1
        
        if is_goal(state):
            end_time = time.time()
            return path, nodes_expanded, end_time - start_time
        
        for move in get_valid_moves(state):
            new_state = make_move(state, move)
            new_state_str = str(new_state)
            if new_state_str not in visited:
                new_path = path + [move]
                g_cost = len(new_path)
                h_cost = heuristic(new_state)
                f_cost = g_cost + h_cost
                queue.put((new_state, new_path), f_cost)
    
    return None, nodes_expanded, time.time() - start_time

# Dữ liệu đầu vào
initial_vehicles = [
    ["X", 2, 0, "H", 2],
    ["A", 3, 1, "V", 2],
    ["B", 0, 2, "V", 3],
    ["C", 4, 2, "H", 2],
    ["D", 3, 4, "V", 3],
    ["E", 1, 5, "V", 2]
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