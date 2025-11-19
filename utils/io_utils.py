"""Input/output utilities for puzzle solver."""

import sys
from puzzle import Puzzle


def read_puzzle(logger):
    """Read puzzle configuration from standard input.
    
    Args:
        logger: Logger instance for logging
        
    Returns:
        Puzzle: Initialized puzzle object
    """
    logger.info("Reading puzzle from stdin")
    
    # Read dimensions - handle both "4 4" and "4" followed by "4" formats
    first_line = input().strip().split()
    rows = int(first_line[0])
    
    if len(first_line) > 1:
        # Dimensions on same line
        cols = int(first_line[1])
    else:
        # Dimensions on separate lines
        second_line = input().strip().split()
        cols = int(second_line[0])
    
    if rows != cols:
        logger.error(f"Non-square puzzle: {rows}x{cols}")
        print("Error: Only square puzzles are supported", file=sys.stderr)
        sys.exit(1)
    
    size = rows
    logger.info(f"Puzzle size: {size}x{size}")
    
    # Read puzzle data
    data = []
    for _ in range(rows):
        line = input().strip().split()
        data.extend([int(x) for x in line])
    
    puzzle = Puzzle(size=size, data=data)
    logger.info(f"Puzzle loaded successfully")
    logger.debug(f"Initial state:\n{puzzle}")
    
    return puzzle
