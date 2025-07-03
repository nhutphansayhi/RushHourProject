class Vehicle:
    def __init__(self, id, row, col, length, orientation, is_target):
        self.id = id
        self.row = row
        self.col = col
        self.length = length 
        self.orientation = orientation
        self.is_target = is_target
        
        # Validate input parameters
        if row < 0 or col < 0:
            raise ValueError(f"Position cannot be negative: row={row}, col={col}")
        
        if row >= 6 or col >= 6:
            raise ValueError(f"Position out of bounds: row={row}, col={col}. Board is 6x6 (0-5)")
        
        if length < 2:
            raise ValueError(f"Vehicle length must be at least 2, got {length}")
        
        if orientation not in ['H', 'V']:
            raise ValueError(f"Orientation must be 'H' or 'V', got '{orientation}'")
        
        # Check if vehicle fits on the board
        if orientation.upper() == 'H' and col + length > 6:
            raise ValueError(f"Horizontal vehicle extends beyond board: col={col}, length={length}")
        elif orientation.upper() == 'V' and row + length > 6:
            raise ValueError(f"Vertical vehicle extends beyond board: row={row}, length={length}")

    def copy(self):
        """Create a copy of this vehicle"""
        return Vehicle(self.id, self.row, self.col, self.length, self.orientation, self.is_target)

    def get_occupied_possitions(self):
        positions_list = []
        if self.orientation == 'H':
            for i in range(self.length):
                positions_list.append((self.row, self.col + i))
        else:
            for i in range(self.length):
                positions_list.append((self.row + i, self.col))
        return positions_list

    def can_move(self, direction):
        
        if self.orientation == 'H' and direction not in ['LEFT', 'RIGHT']:
            return False
        if self.orientation == 'V' and direction not in ['UP', 'DOWN']:
            return False
        
        if direction == 'LEFT':
            return self.col > 0
        elif direction == 'RIGHT':
            return self.col + self.length < 6
        elif direction == 'UP':
            return self.row > 0
        elif direction == 'DOWN':
            return self.row + self.length < 6
        
        return False

    def move(self, direction):
        if direction == 'LEFT':
            return Vehicle(self.id, self.row, self.col - 1, self.length, self.orientation, self.is_target)
        elif direction == 'RIGHT':
            return Vehicle(self.id, self.row, self.col + 1, self.length, self.orientation, self.is_target)
        elif direction == 'UP':
            return Vehicle(self.id, self.row - 1, self.col, self.length, self.orientation, self.is_target)
        else:  # direction == 'DOWN'
            return Vehicle(self.id, self.row + 1, self.col, self.length, self.orientation, self.is_target)

        
    def get_possible_moves(self):
        possible_moves = []
        
        if self.orientation == 'H':
            if self.can_move('LEFT'):
                possible_moves.append('LEFT')
            if self.can_move('RIGHT'):
                possible_moves.append('RIGHT')
        else:
            if self.can_move('UP'):
                possible_moves.append('UP')
            if self.can_move('DOWN'):
                possible_moves.append('DOWN')
        return possible_moves