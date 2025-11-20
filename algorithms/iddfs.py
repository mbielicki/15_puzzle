import logging
from algorithms.dfs import dfs
from puzzle import Puzzle
from typing import Tuple, Optional


def iddfs(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", logger: logging.Logger = None) -> Tuple[Optional[Puzzle], int]:
    total_iterations = 0
    for depth in range(depth_limit):
        if logger:
            logger.info(f"IDDFS - Depth {depth}/{depth_limit-1}: starting search")
        
        result, iterations = dfs(puzzle, depth, order, logger)
        total_iterations += iterations
        
        if logger:
            logger.info(f"IDDFS - Depth {depth} complete: {iterations} iterations, total: {total_iterations}")
        
        if result is not None:
            if logger:
                logger.info(f"Solution found! Iterations: {total_iterations}, Moves: {len(result.history)}")
            return (result, total_iterations)
    
    if logger:
        logger.info(f"No solution found. Iterations: {total_iterations}")
    return (None, total_iterations)