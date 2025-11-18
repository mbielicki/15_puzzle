from puzzle import Puzzle
import numpy as np


def zero_heuristic(puzzle: Puzzle) -> int:
    """Zero heuristic - always returns 0.
    
    This effectively turns A* into uniform cost search (equivalent to BFS).
    """
    return 0


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


def hamming_distance(puzzle: Puzzle) -> int:
    """Calculate the Hamming distance heuristic for the puzzle.
    
    Hamming distance is the number of tiles that are not in their correct position.
    This is an admissible but less informed heuristic than Manhattan distance.
    """
    misplaced = 0
    size = puzzle.size
    
    for i in range(size):
        for j in range(size):
            value = puzzle.array[i, j]
            if value != 0:  # Skip the empty tile
                # Check if tile is in correct position
                if value != puzzle.correct[i, j]:
                    misplaced += 1
    
    return misplaced


def get_heuristic(heuristic_id: str):
    """Get heuristic function by ID.
    
    Args:
        heuristic_id: String ID of the heuristic ('0', '1', or '2')
    
    Returns:
        Callable heuristic function
    """
    heuristics = {
        '0': zero_heuristic,
        '1': manhattan_distance,
        '2': hamming_distance
    }
    
    return heuristics.get(heuristic_id, manhattan_distance)
