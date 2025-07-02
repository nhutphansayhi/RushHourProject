from .vehicle import Vehicle

class State:
    def __init__(self, vehicles):
        self.vehicles = vehicles
        self.target_vehicle_id = None
        
        self.board = []
        for i in range(6):
            row = []
            for j in range(6):
                row.append(None)
            self.board.append(row)
        
        for vehicle in vehicles:
            if vehicle.is_target:
                self.target_vehicle_id = vehicle.id
            
            positions = vehicle.get_occupied_possitions()
            for row, col in positions:
                self.board[row][col] = vehicle.id
    
    def get_vehicle_by_id(self, id):
        for vehicle in self.vehicles:
            if vehicle.id == id:
                return vehicle 
        return None

    def display(self):
        print("=== Rush Hour Board ===")
        for i in range(6):
            print(f"{i} ", end="")
            for j in range(6):
                if self.board[i][j] is None:
                    print(". ", end="")
                else:
                    print(f"{self.board[i][j]} ", end="")
            print()  # New line after each row
        print()
        print(f"Target vehicle: {self.target_vehicle_id}")
    
    def copy(self):
        copied_vehicles = []
        for vehicle in self.vehicles:
            copied_vehicle = Vehicle(vehicle.id, vehicle.row, vehicle.col, 
                                   vehicle.length, vehicle.orientation, vehicle.is_target)
            copied_vehicles.append(copied_vehicle)
        
        return State(copied_vehicles)
    
    def is_solved(self):
        """Check if the puzzle is solved (target vehicle reached exit)."""
        if not self.target_vehicle_id:
            return False
        
        target_vehicle = self.get_vehicle_by_id(self.target_vehicle_id)
        if not target_vehicle:
            return False
        
        if target_vehicle.orientation == 'H' and target_vehicle.col + target_vehicle.length - 1 >=4 and target_vehicle.row == 2:
            return True
        return False

    def to_string(self):
        vehicle_positions = []
        for vehicle in self.vehicles:
            vehicle_positions.append(f"{vehicle.id}:{vehicle.row},{vehicle.col}")
        return "|".join(sorted(vehicle_positions))

    def get_all_possible_moves(self):
        possible_moves = []
        
        for vehicle in self.vehicles:
            valid_directions = vehicle.get_possible_moves()
            
            for direction in valid_directions:
                # Check if move is valid (no collision with other vehicles)
                if self.is_move_valid(vehicle.id, direction):
                    possible_moves.append((vehicle.id, direction))
        return possible_moves

    def is_move_valid(self, vehicle_id, direction):
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            return False
        
        # Get the moved vehicle's new positions
        moved_vehicle = vehicle.move(direction)
        new_positions = moved_vehicle.get_occupied_possitions()
        
        # Check collision with other vehicles
        for other_vehicle in self.vehicles:
            if other_vehicle.id != vehicle_id:
                other_positions = other_vehicle.get_occupied_possitions()
                
                # Check for overlap
                for pos in new_positions:
                    if pos in other_positions:
                        return False  # Collision detected
        
        return True

    def move_vehicle(self, vehicle_id, direction):
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if not vehicle or not self.is_move_valid(vehicle_id, direction):
            return None
        
        # Create new vehicles list with moved vehicle
        new_vehicles = []
        for v in self.vehicles:
            if v.id == vehicle_id:
                new_vehicles.append(v.move(direction))
            else:
                new_vehicles.append(v)
        
        return State(new_vehicles)