import os
from .vehicle import Vehicle

def import_map(map_id):
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    file_name = os.path.join(project_root, "map", f"map{map_id}.txt")
    
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Map file {file_name} not found!")
        return None
    
    vehicles = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        try:
            # Remove parentheses and split by comma
            line = line.strip('()')
            parts = [part.strip().strip('"') for part in line.split(',')]
            
            if len(parts) != 6:
                print(f"Warning: Invalid line format: {line}")
                continue
            
            # Extract data
            vehicle_id = parts[0].strip('"')
            row = int(parts[1])
            col = int(parts[2])
            length = int(parts[3])
            orientation = parts[4].strip('"')
            is_target = bool(int(parts[5]))
            
            # Create Vehicle object
            vehicle = Vehicle(vehicle_id, row, col, length, orientation, is_target)
            vehicles.append(vehicle)
            
        except (ValueError, IndexError) as e:
            print(f"Error parsing line '{line}': {e}")
            continue
    
    return vehicles

