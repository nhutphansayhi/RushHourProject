from collections import deque
import copy
import time

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
    if vehicle[3] == "H":
        vehicle[2] += direction  # Cập nhật cột
    else:
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

# Map phức tạp
initial_vehicles = [
    ["X", 2, 0, "H", 2],  # Xe mục tiêu: hàng 2, cột 0-1, ngang, dài 2
    ["A", 0, 2, "V", 3],  # Xe tải A: hàng 0-2, cột 2, dọc, dài 3
    ["B", 0, 3, "H", 2],  # Xe B: hàng 0, cột 3-4, ngang, dài 2
    ["C", 3, 2, "V", 2],  # Xe C: hàng 3-4, cột 2, dọc, dài 2
    ["D", 4, 4, "H", 2],  # Xe D: hàng 4, cột 4-5, ngang, dài 2
    ["E", 3, 5, "V", 3],  # Xe tải E: hàng 3-5, cột 5, dọc, dài 3
]
initial_state = State(initial_vehicles)

# Chạy BFS và hiển thị kết quả
print("Initial grid:")
print_grid(initial_state)

solution, nodes_expanded, search_time = bfs_solver(initial_state)
if solution:
    print(f"Solution found with {len(solution)} moves:")
    current_state = initial_state
    for i, move in enumerate(solution, 1):
        vehicle_idx, direction = move
        vehicle_id = current_state.vehicles[vehicle_idx][0]
        direction_str = "left" if direction == -1 else "right" if current_state.vehicles[vehicle_idx][3] == "H" else "up" if direction == -1 else "down"
        print(f"Step {i}: Move vehicle {vehicle_id} {direction_str}")
        current_state = make_move(current_state, move)
        print_grid(current_state)
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Search time: {search_time:.4f} seconds")
else:
    print("No solution found")