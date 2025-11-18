from puzzle import Puzzle
import logging
import heapq
from algorithms.heuristics import manhattan_distance


def best_first_search(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", heuristic=None, logger: logging.Logger = None) -> Puzzle:
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

    while pq:
        i += 1
        h, _, current_puzzle = heapq.heappop(pq)
        
        if logger:
            logger.debug(f"BestFS - Iteration {i}: popped puzzle with h={h}, moves={len(current_puzzle.history)}, queue size: {len(pq)}, history: {' '.join(current_puzzle.history) if current_puzzle.history else 'empty'}")
        
        if current_puzzle.is_solved():
            if logger:
                logger.info(f"BestFS - Solution found at iteration {i} with {len(current_puzzle.history)} moves, history: {' '.join(current_puzzle.history)}")
            return current_puzzle
        
        state = current_puzzle.__repr__()
        if state in visited:
            if logger:
                logger.debug(f"BestFS - Already visited, skipping")
            continue
        visited.add(state)

        # Skip if depth limit exceeded
        if len(current_puzzle.history) >= depth_limit:
            if logger:
                logger.debug(f"BestFS - Depth limit {depth_limit} reached, skipping expansion")
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
                    new_h = heuristic(new_puzzle)
                    counter += 1
                    heapq.heappush(pq, (new_h, counter, new_puzzle))
                    moves_added.append(move)
        
        if logger and moves_added:
            logger.debug(f"BestFS - Added moves: {moves_added}, new queue size: {len(pq)}")
    
    if logger:
        logger.info(f"BestFS - No solution found within depth limit {depth_limit}")
    return None
