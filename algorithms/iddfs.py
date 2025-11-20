import logging
from algorithms.dfs import dfs
from puzzle import Puzzle
from typing import Tuple, Optional


def iddfs(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", logger: logging.Logger = None) -> Tuple[Optional[Puzzle], int, int]:
    total_iterations = 0
    max_frontier_size = 0
    for depth in range(depth_limit):
        if logger:
            logger.info(f"IDDFS - Depth {depth}/{depth_limit-1}: starting search")
        
        result, iterations, frontier_size = dfs(puzzle, depth, order, logger)
        total_iterations += iterations
        max_frontier_size = max(max_frontier_size, frontier_size)
        
        if logger:
            logger.info(f"IDDFS - Depth {depth} complete: {iterations} iterations, total: {total_iterations}")
        
        if result is not None:
            if logger:
                logger.info(f"Solution found! Iterations: {total_iterations}, Moves: {len(result.history)}, Max frontier: {max_frontier_size}")
            return (result, total_iterations, max_frontier_size)
    
    if logger:
        logger.info(f"No solution found. Iterations: {total_iterations}, Max frontier: {max_frontier_size}")
    return (None, total_iterations, max_frontier_size)