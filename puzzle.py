import numpy as np

class Puzzle:
    def __init__(self, size=4):
        self.size = size
        self.array = np.zeros((size, size), dtype=int)
        self.shuffle()
        self.history = []

    def shuffle(self) -> None:
        nums = list(range(1, self.size * self.size)) + [0]
        np.random.shuffle(nums)
        self.array = np.array(nums).reshape((self.size, self.size))

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
        items = list(range(1, self.size * self.size)) + [0]
        expected = np.array(items).reshape((self.size, self.size)).T
        return np.array_equal(self.array, expected)
    
    def right(self) -> None:
        zero_pos = tuple(np.argwhere(self.array == 0)[0])
        if zero_pos[0] == 0:
            raise IndexError("Cannot move right")
        
        tile_pos = (zero_pos[0] - 1, zero_pos[1])
        self.array[zero_pos], self.array[tile_pos] = self.array[tile_pos], self.array[zero_pos]
        self.history.append("R")

    def left(self) -> None:
        zero_pos = tuple(np.argwhere(self.array == 0)[0])
        if zero_pos[0] == self.size - 1:
            raise IndexError("Cannot move left")
        
        tile_pos = (zero_pos[0] + 1, zero_pos[1])
        self.array[zero_pos], self.array[tile_pos] = self.array[tile_pos], self.array[zero_pos]
        self.history.append("L")

    def up(self) -> None:
        zero_pos = tuple(np.argwhere(self.array == 0)[0])
        if zero_pos[1] == self.size - 1:
            raise IndexError("Cannot move up")
        
        tile_pos = (zero_pos[0], zero_pos[1] + 1)
        self.array[zero_pos], self.array[tile_pos] = self.array[tile_pos], self.array[zero_pos]
        self.history.append("U")

    def down(self) -> None:
        zero_pos = tuple(np.argwhere(self.array == 0)[0])
        if zero_pos[1] == 0:
            raise IndexError("Cannot move down")
        
        tile_pos = (zero_pos[0], zero_pos[1] - 1)
        self.array[zero_pos], self.array[tile_pos] = self.array[tile_pos], self.array[zero_pos]
        self.history.append("D")

    def can_move(self, direction: str) -> bool:
        zero_pos = tuple(np.argwhere(self.array == 0)[0])
        if direction == "right":
            return zero_pos[0] > 0
        elif direction == "left":
            return zero_pos[0] < self.size - 1
        elif direction == "up":
            return zero_pos[1] < self.size - 1
        elif direction == "down":
            return zero_pos[1] > 0
        else:
            raise ValueError("Invalid direction") 