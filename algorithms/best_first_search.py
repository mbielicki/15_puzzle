from puzzle import Puzzle
import logging
import heapq
from algorithms.heuristics import manhattan_distance
from typing import Tuple, Optional


def best_first_search(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", heuristic=None, logger: logging.Logger = None) -> Tuple[Optional[Puzzle], int, int]:
    """Best First Search using a heuristic function.
    
    Uses a priority queue where states are prioritized by their heuristic value
    from the goal state (lower distance = higher priority).
    """
    if heuristic is None:
        heuristic = manhattan_distance
    
    # Priority queue: (heuristic_value, counter, puzzle)
    # counter ensures FIFO ordering for ties in heuristic value
    counter = 0
    initial_h = heuristic(puzzle)
    pq = [(initial_h, counter, puzzle)]
    visited = set()
    i = 0
    max_frontier_size = 1

    while pq:
        i += 1
        max_frontier_size = max(max_frontier_size, len(pq))
        h, _, current_puzzle = heapq.heappop(pq)
        
        if logger:
            logger.info(f"Iter {i}: depth={len(current_puzzle.history)}, queue={len(pq)}, visited={len(visited)}, h={h}")
        
        if current_puzzle.is_solved():
            if logger:
                logger.info(f"Solution found! Iterations: {i}, Moves: {len(current_puzzle.history)}, Max frontier: {max_frontier_size}")
            return (current_puzzle, i, max_frontier_size)
        
        state = current_puzzle.__repr__()
        if state in visited:
            continue
        visited.add(state)

        # Skip if depth limit exceeded
        if len(current_puzzle.history) >= depth_limit:
            continue

        # Define move operations
        move_operations = {
            "U": (current_puzzle.can_move("U") and current_puzzle.previous_move() != "D", lambda p: p.up()),
            "D": (current_puzzle.can_move("D") and current_puzzle.previous_move() != "U", lambda p: p.down()),
            "L": (current_puzzle.can_move("L") and current_puzzle.previous_move() != "R", lambda p: p.left()),
            "R": (current_puzzle.can_move("R") and current_puzzle.previous_move() != "L", lambda p: p.right())
        }

        moves_added = []
        for move in order:
            if move in move_operations:
                can_move, operation = move_operations[move]
                if can_move:
                    new_puzzle = current_puzzle.copy()
                    operation(new_puzzle)
                    h = heuristic(new_puzzle)
                    counter += 1
                    heapq.heappush(pq, (h, counter, new_puzzle))
    
    if logger:
        logger.info(f"No solution found. Iterations: {i}, Depth limit: {depth_limit}, Max frontier: {max_frontier_size}")
    return (None, i, max_frontier_size)
