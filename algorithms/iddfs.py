import logging
from algorithms.dfs import dfs
from puzzle import Puzzle


def iddfs(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", logger: logging.Logger = None) -> Puzzle:
    for depth in range(depth_limit):
        if logger:
            logger.info(f"IDDFS - Starting depth-limited DFS with depth limit: {depth}")
        result = dfs(puzzle, depth, order, logger)
        if result is not None:
            if logger:
                logger.info(f"IDDFS - Solution found at depth limit: {depth}")
            return result
    if logger:
        logger.info(f"IDDFS - No solution found within depth limit: {depth_limit}")
    return None