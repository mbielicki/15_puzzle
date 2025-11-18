from puzzle import Puzzle
import logging


def dfs_iterative(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", logger: logging.Logger = None) -> Puzzle:
    stack = [puzzle]
    i = 0

    while stack:
        i += 1
        current_puzzle = stack.pop()
        
        if logger:
            logger.debug(f"Iterative - Iteration {i}: popped puzzle with {len(current_puzzle.history)} moves, stack size: {len(stack)}, history: {' '.join(current_puzzle.history) if current_puzzle.history else 'empty'}")
        
        if current_puzzle.is_solved():
            if logger:
                logger.info(f"Iterative - Solution found at iteration {i} with {len(current_puzzle.history)} moves, history: {' '.join(current_puzzle.history)}")
            return current_puzzle

        # Skip if depth limit exceeded
        if len(current_puzzle.history) >= depth_limit:
            if logger:
                logger.debug(f"Iterative - Depth limit {depth_limit} reached, skipping expansion")
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
                    stack.append(new_puzzle)
                    moves_added.append(move)
        
        if logger and moves_added:
            logger.debug(f"Iterative - Added moves: {moves_added}, new stack size: {len(stack)}")


def dfs(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", logger: logging.Logger = None) -> Puzzle:
    iteration_count = [0]  # Using list to allow modification in nested function
    
    def dfs_recursive(current_puzzle: Puzzle, depth: int) -> Puzzle:
        iteration_count[0] += 1
        
        if logger:
            logger.debug(f"Recursive - Iteration {iteration_count[0]}: depth={depth}, moves={len(current_puzzle.history)}, history: {' '.join(current_puzzle.history) if current_puzzle.history else 'empty'}")
        
        if current_puzzle.is_solved():
            if logger:
                logger.info(f"Recursive - Solution found at iteration {iteration_count[0]}, depth={depth}, moves={len(current_puzzle.history)}, history: {' '.join(current_puzzle.history)}")
            return current_puzzle
        
        # Skip if depth limit exceeded
        if len(current_puzzle.history) >= depth_limit:
            if logger:
                logger.debug(f"Recursive - Depth limit {depth_limit} reached at depth {depth}, returning None")
            return None
        
        # Define move operations
        move_operations = {
            "U": (current_puzzle.can_move("U") and current_puzzle.previous_move() != "D", lambda p: p.up()),
            "D": (current_puzzle.can_move("D") and current_puzzle.previous_move() != "U", lambda p: p.down()),
            "L": (current_puzzle.can_move("L") and current_puzzle.previous_move() != "R", lambda p: p.left()),
            "R": (current_puzzle.can_move("R") and current_puzzle.previous_move() != "L", lambda p: p.right())
        }
        
        # Try moves in the specified order
        moves = [move for move in order if move in move_operations and move_operations[move][0]]
        
        if logger and moves:
            logger.debug(f"Recursive - Trying moves: {moves}")
        
        for move in moves:
            new_puzzle = current_puzzle.copy()
            move_operations[move][1](new_puzzle)
            
            if logger:
                logger.debug(f"Recursive - Exploring move {move}")
            result = dfs_recursive(new_puzzle, depth + 1)
            if result is not None:
                if logger:
                    logger.debug(f"Recursive - Move {move} led to solution, returning")
                return result
        
        if logger:
            logger.debug(f"Recursive - No solution found from this state, returning None")
        return None
    
    return dfs_recursive(puzzle, 0)
