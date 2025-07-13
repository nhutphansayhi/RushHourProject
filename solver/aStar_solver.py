import heapq
import sys
import os

# Thư viện cần thiết
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

# from utils.state import State
# from utils.vehicle import Vehicle
# from utils.utils import import_map

# Biểu diễn trạng thái trò chơi
# class State:
#     def __init__(self, vehicles):
#         self.vehicles = vehicles  # Danh sách các xe: [[ID, row, col, direction, length], ...]
    
#     def __eq__(self, other):
#         return self.vehicles == other.vehicles
    
#     def __hash__(self):
#         return hash(str(self.vehicles))

# # Kiểm tra trạng thái mục tiêu
# def is_goal(state):
#     for vehicle in state.vehicles:
#         if vehicle[0] == "X":  # Xe mục tiêu
#             if vehicle[3] == "H" and vehicle[2] + vehicle[4] - 1 == 5:  # Xe ngang, đạt cột 5
#                 return True
#     return False

# # Lấy các bước di chuyển hợp lệ
# def get_valid_moves(state):
#     moves = []
#     grid = [[0]*6 for _ in range(6)]  # Lưới 6x6, 0 là ô trống, 1 là ô bị chiếm
    
#     # Đánh dấu các ô bị chiếm
#     for vehicle in state.vehicles:
#         row, col, direction, length = vehicle[1], vehicle[2], vehicle[3], vehicle[4]
#         if direction == "H":
#             for c in range(col, col + length):
#                 if 0 <= row < 6 and 0 <= c < 6:
#                     grid[row][c] = 1
#         else:  # direction == "V"
#             for r in range(row, row + length):
#                 if 0 <= r < 6 and 0 <= col < 6:
#                     grid[r][col] = 1
    
#     # Kiểm tra từng xe
#     for i, vehicle in enumerate(state.vehicles):
#         row, col, direction, length = vehicle[1], vehicle[2], vehicle[3], vehicle[4]
#         if direction == "H":
#             # Di chuyển trái
#             if col > 0 and grid[row][col-1] == 0:
#                 moves.append((i, -1))  # Di chuyển xe i về trái 1 ô
#             # Di chuyển phải
#             if col + length < 6 and grid[row][col + length] == 0:
#                 moves.append((i, 1))  # Di chuyển xe i về phải 1 ô
#         else:  # direction == "V"
#             # Di chuyển lên
#             if row > 0 and grid[row-1][col] == 0:
#                 moves.append((i, -1))  # Di chuyển xe i lên 1 ô
#             # Di chuyển xuống
#             if row + length < 6 and grid[row + length][col] == 0:
#                 moves.append((i, 1))  # Di chuyển xe i xuống 1 ô
#     return moves

# # Tạo trạng thái mới sau khi di chuyển
# def make_move(state, move):
#     vehicle_idx, direction = move
#     new_vehicles = copy.deepcopy(state.vehicles)
#     vehicle = new_vehicles[vehicle_idx]
#     if vehicle[3] == "H":  # Xe ngang
#         vehicle[2] += direction  # Cập nhật cột
#     else:  # Xe dọc
#         vehicle[1] += direction  # Cập nhật hàng
#     return State(new_vehicles)

# # Hiển thị lưới để dễ hình dung
# def print_grid(state):
#     grid = [["."]*6 for _ in range(6)]
#     for vehicle in state.vehicles:
#         row, col, direction, length = vehicle[1], vehicle[2], vehicle[3], vehicle[4]
#         vehicle_id = vehicle[0]
#         if direction == "H":
#             for c in range(col, col + length):
#                 grid[row][c] = vehicle_id
#         else:
#             for r in range(row, row + length):
#                 grid[r][col] = vehicle_id
#     for row in grid:
#         print(" ".join(row))
#     print()

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

def heuristic(state):
    heu = 0
    # tính tổng số ô mà xe mục tiêu chưa đi
    target_vehicle = state.vehicles[0]
    if target_vehicle:
        target_row, target_col = target_vehicle.row, target_vehicle.col
        target_length = target_vehicle.length
        
        # Tính số ô mà xe mục tiêu chưa đi
        if target_vehicle.orientation == "H":
            for i in range(target_col + target_length, 6):
                if state.board[target_row][i] != "X":
                    heu += target_vehicle.length  # Chiều dài của xe mục tiêu
      # Chiều dài của xe mục tiêu
    
    # Tính chiều dài của những chiếc xe nằm chắn đường xe mục tiêu
    nameOfVehicleList = []
    for i in range(min(5, target_col + 2),5,1):
        if state.board[target_row][i] != "X" and state.board[target_row][i]!= ".":
            nameOfVehicleList.append(state.board[target_row][i])

    for vehicle in state.vehicles:
        if vehicle.id in nameOfVehicleList:
            heu += vehicle.length
            
    return heu
    

# Thuật toán A*
def aStar_solver(initial_state, cancel_flag=None):
    queue = PriorityQueue()
    
    # B: Cache initial state string
    queue.put((initial_state, []), heuristic(initial_state))
    visited = set()
    nodes_expanded = 0
    
    while not queue.is_empty():
        if cancel_flag and cancel_flag.is_set():
            return None
        
        state, path = queue.get()
        
        # B: Cache state string - tính 1 lần duy nhất
        state_key = state.to_string()
        if state_key in visited:
            continue

        visited.add(state_key)  # Sử dụng cached string
        nodes_expanded += 1
        
        if state.is_solved():
            cost = 0
            for vehicle_id, _ in path:
                cost += state.get_vehicle_by_id(vehicle_id).length

            return cost, nodes_expanded, path
        
        possible_moves = state.get_all_possible_moves()
        for vehicle_id, direction in possible_moves:
            new_state = state.move_vehicle(vehicle_id, direction)
            
            # B: Cache new state string - tính 1 lần duy nhất
            new_state_key = new_state.to_string()
            if new_state_key not in visited:
                new_path = path + [(vehicle_id, direction)]
                g_cost = len(new_path)
                h_cost = heuristic(new_state)
                f_cost = g_cost + h_cost
                queue.put((new_state, new_path), f_cost)
                
    return None, nodes_expanded, []


# initial_vehicle = import_map(1)  # Nhập dữ liệu từ file map12.txt
# initial_state = State(initial_vehicle)
# # Chạy và hiển thị kết quả
# print("Step 0:")
# for line in initial_state.vehicles:
#     print(line.id, line.row, line.col, line.length, line.orientation, line.is_target)

# solution, nodes_expanded, search_time = aStar_solver(initial_state)
# if solution:
#     print(f"Solution found with {len(solution)} moves:")
#     current_state = initial_state
#     for i, move in enumerate(solution, 1):
#         vehicle_idx, direction = move
#         # vehicle_id = current_state.vehicles[vehicle_idx][0]
#         # Logic in hướng đã sửa
#         # if current_state.vehicles[vehicle_idx][3] == "H":
#         #     direction_str = "left" if direction == -1 else "right"
#         # else:
#         #     direction_str = "up" if direction == -1 else "down"
        
#         print(f"Step {i}: Move vehicle {vehicle_idx} {direction}")
#         current_state = current_state.move_vehicle(vehicle_idx, direction)
#         current_state.display()
#     print(f"Nodes expanded: {nodes_expanded}")
#     print(f"Search time: {search_time:.4f} seconds")
# else:
#     print("No solution found")