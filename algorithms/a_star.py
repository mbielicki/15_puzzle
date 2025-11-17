from puzzle import Puzzle
import logging
import heapq
from algorithms.heuristics import manhattan_distance


def a_star(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", logger: logging.Logger = None) -> Puzzle:
    """A* algorithm using Manhattan distance heuristic.
    
    Uses a priority queue where states are prioritized by f(n) = g(n) + h(n):
    - g(n): actual cost from start (number of moves so far)
    - h(n): heuristic estimate to goal (Manhattan distance)
    - f(n): estimated total cost through this state
    """
    # Priority queue: (f_value, counter, puzzle)
    # counter ensures FIFO ordering for ties in f value
    counter = 0
    g = 0  # initial cost
    h = manhattan_distance(puzzle)
    f = g + h
    pq = [(f, counter, puzzle)]
    visited = set()
    i = 0

    while pq:
        i += 1
        current_f, _, current_puzzle = heapq.heappop(pq)
        current_g = len(current_puzzle.history)
        current_h = current_f - current_g
        
        print(f"\rA* iteration {i}, queue size: {len(pq)}, f={current_f} (g={current_g}, h={current_h})       ", end="")
        
        if logger:
            logger.debug(f"A* - Iteration {i}: popped puzzle with f={current_f} (g={current_g}, h={current_h}), queue size: {len(pq)}, history: {' '.join(current_puzzle.history) if current_puzzle.history else 'empty'}")
        
        if current_puzzle.is_solved():
            if logger:
                logger.info(f"A* - Solution found at iteration {i} with {len(current_puzzle.history)} moves, history: {' '.join(current_puzzle.history)}")
            return current_puzzle
        
        state = current_puzzle.__repr__()
        if state in visited:
            if logger:
                logger.debug(f"A* - Already visited, skipping")
            continue
        visited.add(state)

        # Skip if depth limit exceeded
        if len(current_puzzle.history) >= depth_limit:
            if logger:
                logger.debug(f"A* - Depth limit {depth_limit} reached, skipping expansion")
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
                    new_h = manhattan_distance(new_puzzle)
                    new_f = new_g + new_h
                    counter += 1
                    heapq.heappush(pq, (new_f, counter, new_puzzle))
                    moves_added.append(move)
        
        if logger and moves_added:
            logger.debug(f"A* - Added moves: {moves_added}, new queue size: {len(pq)}")
    
    if logger:
        logger.info(f"A* - No solution found within depth limit {depth_limit}")
    return None
