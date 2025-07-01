# Test the import function
from utils.utils import import_map
from utils.state import State

# Load vehicles from map1.txt
vehicles = import_map(1)

if vehicles:
    print(f"Loaded {len(vehicles)} vehicles:")
    for vehicle in vehicles:
        print(f"  {vehicle.id}: pos=({vehicle.row},{vehicle.col}), len={vehicle.length}, ori={vehicle.orientation}, target={vehicle.is_target}")
    
    # Create game state
    game_state = State(vehicles)
    game_state.display()
else:
    print("Failed to load map!")
