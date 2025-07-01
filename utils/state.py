from vehicle import Vehicle

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