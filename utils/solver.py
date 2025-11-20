"""Solver orchestration for puzzle algorithms."""

import random
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.iddfs import iddfs
from algorithms.best_first_search import best_first_search
from algorithms.a_star import a_star
from algorithms.sma_star import sma_star
from algorithms.heuristics import get_heuristic


def get_move_order(order_str, logger):
    """Process move order string.
    
    Args:
        order_str: String defining move order (e.g., 'DULR' or 'RAND')
        logger: Logger instance for logging
    
    Returns:
        str: Processed move order. Returns 'RAND' for random ordering at each node.
    """
    if order_str.upper() == 'RAND':
        logger.info(f"Using random move order (shuffled at each node)")
        return 'RAND'
    else:
        logger.info(f"Using move order: {order_str.upper()}")
        return order_str.upper()


def solve_puzzle(puzzle, algorithm, parameter, logger, depth_limit=15):
    """Solve the puzzle using the specified algorithm.
    
    Args:
        puzzle: Puzzle object to solve
        algorithm: Algorithm name ('bfs', 'dfs', 'idfs', 'bf', 'astar', 'sma')
        parameter: Move order or heuristic ID
        logger: Logger instance for logging
        depth_limit: Maximum search depth
    
    Returns:
        Tuple[Puzzle or None, int]: (Solved puzzle if found, iteration count)
    """
    logger.info(f"Starting {algorithm.upper()} algorithm with depth limit {depth_limit}")
    
    if algorithm in ['bfs', 'dfs', 'idfs']:
        order = get_move_order(parameter, logger)
        
        if algorithm == 'bfs':
            logger.info("Running Breadth-First Search")
            return bfs(puzzle, depth_limit, order, logger)
        elif algorithm == 'dfs':
            logger.info("Running Depth-First Search")
            return dfs(puzzle, depth_limit, order, logger)
        elif algorithm == 'idfs':
            logger.info("Running Iterative Deepening DFS")
            return iddfs(puzzle, depth_limit, order, logger)
    
    elif algorithm in ['bf', 'astar', 'sma']:
        # For heuristic-based algorithms
        heuristic_id = parameter
        heuristic = get_heuristic(heuristic_id)
        order = 'UDLR'  # Default order for heuristic searches
        logger.info(f"Using heuristic ID: {heuristic_id}")
        
        if algorithm == 'bf':
            logger.info("Running Best-First Search")
            return best_first_search(puzzle, depth_limit, order, heuristic, logger)
        elif algorithm == 'astar':
            logger.info("Running A* Search")
            return a_star(puzzle, depth_limit, order, heuristic, logger)
        elif algorithm == 'sma':
            logger.info("Running SMA* Search")
            return sma_star(puzzle, depth_limit, max_nodes=10000, order=order, heuristic=heuristic, logger=logger)
    
    return (None, 0)
