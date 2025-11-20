from puzzle import Puzzle
import logging
import random
from typing import Tuple, Optional

def bfs(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", logger: logging.Logger = None) -> Tuple[Optional[Puzzle], int, int]:
    queue = [puzzle]
    visited = set()
    i = 0
    max_frontier_size = 1

    while queue:
        i+= 1
        max_frontier_size = max(max_frontier_size, len(queue))
        current_puzzle = queue.pop(0)
        
        if logger:
            logger.info(f"Iter {i}: depth={len(current_puzzle.history)}, queue={len(queue)}, visited={len(visited)}")
        
        if current_puzzle.is_solved():
            if logger:
                logger.info(f"Solution found! Iterations: {i}, Moves: {len(current_puzzle.history)}, Max frontier: {max_frontier_size}")
            return (current_puzzle, i, max_frontier_size)
        if current_puzzle.__repr__() in visited:
            continue
        visited.add(current_puzzle.__repr__())

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

        # Shuffle order at each node if RAND
        if order == "RAND":
            current_order = ['U', 'D', 'L', 'R']
            random.shuffle(current_order)
        else:
            current_order = list(order)
        
        for move in current_order:
            if move in move_operations:
                can_move, operation = move_operations[move]
                if can_move:
                    new_puzzle = current_puzzle.copy()
                    operation(new_puzzle)
                    queue.append(new_puzzle)
    
    if logger:
        logger.info(f"No solution found. Iterations: {i}, Depth limit: {depth_limit}, Max frontier: {max_frontier_size}")
    return (None, i, max_frontier_size)