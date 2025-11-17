from puzzle import Puzzle
import logging


def dfs_iterative(puzzle: Puzzle, depth_limit: int, logger: logging.Logger = None) -> Puzzle:
    stack = [puzzle]
    i = 0

    while stack:
        i += 1
        current_puzzle = stack.pop()
        print(f"\rDFS iteration {i}, stack size: {len(stack)}, moves: {len(current_puzzle.history)}       ", end="")
        
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

        moves_added = []
        if current_puzzle.can_move("R") and current_puzzle.previous_move() != "L":
            new_puzzle = current_puzzle.copy()
            new_puzzle.right()
            stack.append(new_puzzle)
            moves_added.append("R")
        if current_puzzle.can_move("L") and current_puzzle.previous_move() != "R":
            new_puzzle = current_puzzle.copy()
            new_puzzle.left()
            stack.append(new_puzzle)
            moves_added.append("L")
        if current_puzzle.can_move("D") and current_puzzle.previous_move() != "U":
            new_puzzle = current_puzzle.copy()
            new_puzzle.down()
            stack.append(new_puzzle)
            moves_added.append("D")
        if current_puzzle.can_move("U") and current_puzzle.previous_move() != "D":
            new_puzzle = current_puzzle.copy()
            new_puzzle.up()
            stack.append(new_puzzle)
            moves_added.append("U")
        
        if logger and moves_added:
            logger.debug(f"Iterative - Added moves: {moves_added}, new stack size: {len(stack)}")


def dfs(puzzle: Puzzle, depth_limit: int, logger: logging.Logger = None) -> Puzzle:
    iteration_count = [0]  # Using list to allow modification in nested function
    
    def dfs_recursive(current_puzzle: Puzzle, depth: int) -> Puzzle:
        iteration_count[0] += 1
        print(f"\rDFS iteration {iteration_count[0]}, depth: {depth}, moves: {len(current_puzzle.history)}       ", end="")
        
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
        
        # Try all possible moves
        moves = []
        if current_puzzle.can_move("U") and current_puzzle.previous_move() != "D":
            moves.append("U")
        if current_puzzle.can_move("D") and current_puzzle.previous_move() != "U":
            moves.append("D")
        if current_puzzle.can_move("L") and current_puzzle.previous_move() != "R":
            moves.append("L")
        if current_puzzle.can_move("R") and current_puzzle.previous_move() != "L":
            moves.append("R")
        
        if logger and moves:
            logger.debug(f"Recursive - Trying moves: {moves}")
        
        for move in moves:
            new_puzzle = current_puzzle.copy()
            if move == "U":
                new_puzzle.up()
            elif move == "D":
                new_puzzle.down()
            elif move == "L":
                new_puzzle.left()
            elif move == "R":
                new_puzzle.right()
            
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
