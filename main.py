from algorithms.iddfs import iddfs
from puzzle import Puzzle
from algorithms.dfs import dfs, dfs_iterative
from algorithms.bfs import bfs
import logging
from datetime import datetime
import os

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging with timestamp-based filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/iddfs_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Logging to {log_file}")
    
    puzzle = Puzzle(size=3, data=[1, 2, 0, 3, 5, 6, 7, 8, 4])
    print("Initial puzzle state:")
    print(puzzle)
    
    solved = iddfs(puzzle, 20, logger)

    if solved is None:
        print("\nNo solution found within the depth limit.")
    else:
        print("\nSolved puzzle state:")
        print(solved)
        print(f"Moves to solve: {' '.join(solved.history)}")