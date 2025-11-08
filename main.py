from puzzle import Puzzle
from algorithms.bfs import bfs

if __name__ == "__main__":
    puzzle = Puzzle(size=3)
    print("Initial puzzle state:")
    print(puzzle)
    
    solved = bfs(puzzle)
    
    print("\nSolved puzzle state:")
    print(solved)
    print(f"Moves to solve: {' '.join(solved.history)}")