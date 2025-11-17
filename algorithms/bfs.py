from puzzle import Puzzle
import logging

def bfs(puzzle: Puzzle, depth_limit: int, logger: logging.Logger = None) -> Puzzle:
    queue = [puzzle]
    visited = set()
    i = 0

    while queue:
        i+= 1
        print(f"\rBFS iteration {i}, queue size: {len(queue)}       ", end="")
        current_puzzle = queue.pop(0)
        
        if logger:
            logger.debug(f"BFS - Iteration {i}: popped puzzle with {len(current_puzzle.history)} moves, queue size: {len(queue)}, history: {' '.join(current_puzzle.history) if current_puzzle.history else 'empty'}")
        
        if current_puzzle.is_solved():
            if logger:
                logger.info(f"BFS - Solution found at iteration {i} with {len(current_puzzle.history)} moves, history: {' '.join(current_puzzle.history)}")
            return current_puzzle
        if current_puzzle.__repr__() in visited:
            if logger:
                logger.debug(f"BFS - Already visited, skipping")
            continue
        visited.add(current_puzzle.__repr__())

        # Skip if depth limit exceeded
        if len(current_puzzle.history) >= depth_limit:
            if logger:
                logger.debug(f"BFS - Depth limit {depth_limit} reached, skipping expansion")
            continue

        moves_added = []
        if current_puzzle.can_move("U") and current_puzzle.previous_move() != "D":
            new_puzzle = current_puzzle.copy()
            new_puzzle.up()
            queue.append(new_puzzle)
            moves_added.append("U")
        if current_puzzle.can_move("D") and current_puzzle.previous_move() != "U":
            new_puzzle = current_puzzle.copy()
            new_puzzle.down()
            queue.append(new_puzzle)
            moves_added.append("D")
        if current_puzzle.can_move("L") and current_puzzle.previous_move() != "R":
            new_puzzle = current_puzzle.copy()
            new_puzzle.left()
            queue.append(new_puzzle)
            moves_added.append("L")
        if current_puzzle.can_move("R") and current_puzzle.previous_move() != "L":
            new_puzzle = current_puzzle.copy()
            new_puzzle.right()
            queue.append(new_puzzle)
            moves_added.append("R")
        
        if logger and moves_added:
            logger.debug(f"BFS - Added moves: {moves_added}, new queue size: {len(queue)}")