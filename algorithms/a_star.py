from typing import Optional, Tuple
from puzzle import Puzzle
import logging
import heapq
from algorithms.heuristics import manhattan_distance


def a_star(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", heuristic=None, logger: logging.Logger = None) -> Tuple[Optional[Puzzle], int]:
    """A* algorithm using a heuristic function.
    
    Uses a priority queue where states are prioritized by f(n) = g(n) + h(n):
    - g(n): actual cost from start (number of moves so far)
    - h(n): heuristic estimate to goal
    - f(n): estimated total cost through this state
    """
    if heuristic is None:
        heuristic = manhattan_distance
    
    # Priority queue: (f_value, counter, puzzle)
    # counter ensures FIFO ordering for ties in f value
    counter = 0
    g = 0  # initial cost
    h = heuristic(puzzle)
    f = g + h
    pq = [(f, counter, puzzle)]
    visited = set()
    i = 0

    while pq:
        i += 1
        current_f, _, current_puzzle = heapq.heappop(pq)
        current_g = len(current_puzzle.history)
        current_h = current_f - current_g
        
        if logger:
            logger.info(f"Iter {i}: depth={len(current_puzzle.history)}, queue={len(pq)}, visited={len(visited)}, f={current_f}")
        
        if current_puzzle.is_solved():
            if logger:
                logger.info(f"Solution found! Iterations: {i}, Moves: {len(current_puzzle.history)}")
            return (current_puzzle, i)
        
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
                    new_g = len(new_puzzle.history)
                    new_h = heuristic(new_puzzle)
                    new_f = new_g + new_h
                    counter += 1
                    heapq.heappush(pq, (new_f, counter, new_puzzle))
    
    if logger:
        logger.info(f"No solution found. Iterations: {i}, Depth limit: {depth_limit}")
    return (None, i)
