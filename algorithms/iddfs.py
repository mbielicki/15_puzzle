import logging
from algorithms.dfs import dfs
from puzzle import Puzzle


def iddfs(puzzle: Puzzle, depth_limit: int, order: str = "UDLR", logger: logging.Logger = None) -> Puzzle:
    total_iterations = 0
    for depth in range(depth_limit):
        if logger:
            logger.info(f"IDDFS - Depth {depth}/{depth_limit-1}: starting search")
        
        # Create a wrapper to count iterations from DFS
        iteration_count = [0]
        original_logger = logger
        
        # Wrap logger to count iterations
        class IterationCountingLogger:
            def __init__(self, original_logger):
                self.original_logger = original_logger
                
            def info(self, msg):
                if msg.startswith("Iter "):
                    iteration_count[0] += 1
                if self.original_logger:
                    self.original_logger.info(msg)
            
            def debug(self, msg):
                if self.original_logger:
                    self.original_logger.debug(msg)
            
            def warning(self, msg):
                if self.original_logger:
                    self.original_logger.warning(msg)
            
            def error(self, msg):
                if self.original_logger:
                    self.original_logger.error(msg)
        
        counting_logger = IterationCountingLogger(original_logger) if logger else None
        result = dfs(puzzle, depth, order, counting_logger)
        total_iterations += iteration_count[0]
        
        if logger:
            logger.info(f"IDDFS - Depth {depth} complete: {iteration_count[0]} iterations, total: {total_iterations}")
        
        if result is not None:
            if logger:
                logger.info(f"Solution found! Total iterations: {total_iterations}, Moves: {len(result.history)}")
            return result
    
    if logger:
        logger.info(f"IDDFS - No solution found. Total iterations: {total_iterations}")
    return None