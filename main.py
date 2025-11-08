from puzzle import Puzzle
from algorithms.dfs import dfs
from algorithms.bfs import bfs

if __name__ == "__main__":
    puzzle = Puzzle(size=3, data=[1, 2, 0, 3, 5, 6, 7, 8, 4])
    print("Initial puzzle state:")
    print(puzzle)
    
    solved = dfs(puzzle)
    
    print("\nSolved puzzle state:")
    print(solved)
    print(f"Moves to solve: {' '.join(solved.history)}")