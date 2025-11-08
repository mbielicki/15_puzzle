import numpy as np
import random

class Puzzle:
    def __init__(self, size=4):
        self.size = size
        # build the solved/correct board first
        items = list(range(1, self.size * self.size)) + [0]
        self.correct = np.array(items).reshape((self.size, self.size)).T

        # initialize state
        self.array = np.zeros((size, size), dtype=int)
        self.history = []

        # shuffle from the solved state
        self.shuffle()

    def shuffle(self) -> None:
        # Start from the solved configuration and perform 100 random moves.
        # Avoid immediately reversing the previous move when possible.
        self.array = self.correct.copy()

        opposite = {"R": "L", "L": "R", "U": "D", "D": "U"}
        prev_move = None

        for _ in range(10):
            allowed = self.allowed_moves()

            # try to avoid reversing the previous move
            options = [m for m in allowed if prev_move is None or m != opposite.get(prev_move)]
            if not options:
                options = allowed

            move = random.choice(options)
            self.move(move)
            prev_move = move
        
        self.history = []

    def previous_move(self) -> str:
        if not self.history:
            return None
        return self.history[-1]
    
    def copy(self) -> 'Puzzle':
        new_puzzle = Puzzle(size=self.size)
        new_puzzle.array = self.array.copy()
        new_puzzle.history = self.history.copy()
        return new_puzzle
    
    def __repr__(self) -> str:
        return '\n'.join('\t'.join(f"{num if num != 0 else ' '}" for num in col) for col in self.array.T)
    
    def __getitem__(self, index) -> int:
        return self.array[index]
    
    def __setitem__(self, index, value) -> None:
        self.array[index] = value

    def is_solved(self) -> bool:
        return np.array_equal(self.array, self.correct)
    
    def right(self) -> None:
        zero_pos = tuple(np.argwhere(self.array == 0)[0])
        if not self.can_move("R"):
            raise IndexError("Cannot move right")
        
        tile_pos = (zero_pos[0] - 1, zero_pos[1])
        self.array[zero_pos], self.array[tile_pos] = self.array[tile_pos], self.array[zero_pos]
        self.history.append("R")

    def left(self) -> None:
        zero_pos = tuple(np.argwhere(self.array == 0)[0])
        if not self.can_move("L"):
            raise IndexError("Cannot move left")
        
        tile_pos = (zero_pos[0] + 1, zero_pos[1])
        self.array[zero_pos], self.array[tile_pos] = self.array[tile_pos], self.array[zero_pos]
        self.history.append("L")

    def up(self) -> None:
        zero_pos = tuple(np.argwhere(self.array == 0)[0])
        if not self.can_move("U"):
            raise IndexError("Cannot move up")
        
        tile_pos = (zero_pos[0], zero_pos[1] + 1)
        self.array[zero_pos], self.array[tile_pos] = self.array[tile_pos], self.array[zero_pos]
        self.history.append("U")

    def down(self) -> None:
        zero_pos = tuple(np.argwhere(self.array == 0)[0])
        if not self.can_move("D"):
            raise IndexError("Cannot move down")
        
        tile_pos = (zero_pos[0], zero_pos[1] - 1)
        self.array[zero_pos], self.array[tile_pos] = self.array[tile_pos], self.array[zero_pos]
        self.history.append("D")

    def move(self, direction: str) -> None:
        if direction == "R":
            self.right()
        elif direction == "L":
            self.left()
        elif direction == "U":
            self.up()
        elif direction == "D":
            self.down()
        else:
            raise ValueError("Invalid direction") 

    def can_move(self, direction: str) -> bool:
        zero_pos = tuple(np.argwhere(self.array == 0)[0])
        if direction == "R":
            return zero_pos[0] > 0
        elif direction == "L":
            return zero_pos[0] < self.size - 1
        elif direction == "U":
            return zero_pos[1] < self.size - 1
        elif direction == "D":
            return zero_pos[1] > 0
        else:
            raise ValueError("Invalid direction") 
        
        
    def allowed_moves(self) -> list:
        allowed = []
        if self.can_move("R"):
            allowed.append("R")
        if self.can_move("L"):
            allowed.append("L")
        if self.can_move("U"):
            allowed.append("U")
        if self.can_move("D"):
            allowed.append("D")

        return allowed