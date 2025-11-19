from puzzle import Puzzle
import logging

def bfs(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", logger: logging.Logger = None) -> Puzzle:
    queue = [puzzle]
    visited = set()
    i = 0

    while queue:
        i+= 1
        current_puzzle = queue.pop(0)
        
        if logger:
            logger.info(f"Iter {i}: depth={len(current_puzzle.history)}, queue={len(queue)}, visited={len(visited)}")
        
        if current_puzzle.is_solved():
            if logger:
                logger.info(f"Solution found! Iterations: {i}, Moves: {len(current_puzzle.history)}")
            return current_puzzle
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

        moves_added = []
        for move in order:
            if move in move_operations:
                can_move, operation = move_operations[move]
                if can_move:
                    new_puzzle = current_puzzle.copy()
                    operation(new_puzzle)
                    queue.append(new_puzzle)
                    moves_added.append(move)
        
        if logger and moves_added:
            logger.debug(f"BFS - Added moves: {moves_added}, new queue size: {len(queue)}")