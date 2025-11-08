import numpy as np

class Puzzle:
    def __init__(self, size=4):
        self.size = size
        self.array = np.zeros((size, size), dtype=int)
        self.shuffle()

    def shuffle(self) -> None:
        nums = list(range(1, self.size * self.size)) + [0]
        np.random.shuffle(nums)
        self.array = np.array(nums).reshape((self.size, self.size))

    def __repr__(self) -> str:
        return '\n'.join('\t'.join(f"{num if num != 0 else ' '}" for num in row) for row in self.array)