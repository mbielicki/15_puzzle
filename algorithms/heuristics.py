from puzzle import Puzzle
import numpy as np


def manhattan_distance(puzzle: Puzzle) -> int:
    """Calculate the Manhattan distance heuristic for the puzzle.
    
    Manhattan distance is the sum of the distances each tile is from its goal position.
    """
    distance = 0
    size = puzzle.size
    
    for i in range(size):
        for j in range(size):
            value = puzzle.array[i, j]
            if value != 0:  # Skip the empty tile
                # Find where this value should be in the correct configuration
                goal_pos = np.argwhere(puzzle.correct == value)[0]
                # Add Manhattan distance (|x1-x2| + |y1-y2|)
                distance += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
    
    return distance
