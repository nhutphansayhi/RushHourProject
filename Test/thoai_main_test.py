from utils import Vehicle, State, import_map

def main():
    vehicles = import_map(1)    
    if not vehicles:
        print("Failed to load map!")
        return
    
    state = State(vehicles)
    print("Original state:")
    state.display()
    
    # Create a new state with moved vehicle
    target_vehicle = state.get_vehicle_by_id('X')
    if target_vehicle and target_vehicle.can_move('RIGHT'):
        # Move the vehicle and create new state
        moved_vehicle = target_vehicle.move('RIGHT')
        
        # Create new vehicles list with the moved vehicle
        new_vehicles = []
        for vehicle in state.vehicles:
            if vehicle.id == 'X':
                new_vehicles.append(moved_vehicle)  # Replace with moved vehicle
            else:
                new_vehicles.append(vehicle)        # Keep other vehicles same
        
        # Create new state with updated vehicles
        new_state = State(new_vehicles)
        print(f"\nAfter moving X right:")
        new_state.display()
    else:
        print("X cannot move right!")

if __name__ == "__main__":
    main()
