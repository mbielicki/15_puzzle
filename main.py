"""15-Puzzle Solver - Main entry point."""

import sys
from utils.cli import parse_arguments
from utils.logging_config import setup_logging
from utils.io_utils import read_puzzle
from utils.solver import solve_puzzle


def main():
    """Main entry point for the puzzle solver."""
    args = parse_arguments()
    
    # Determine which algorithm to use (before logging setup)
    algorithm = None
    parameter = None
    
    if args.bfs:
        algorithm = 'bfs'
        parameter = args.bfs
    elif args.dfs:
        algorithm = 'dfs'
        parameter = args.dfs
    elif args.idfs:
        algorithm = 'idfs'
        parameter = args.idfs
    elif args.bf:
        algorithm = 'bf'
        parameter = args.bf
    elif args.astar:
        algorithm = 'astar'
        parameter = args.astar
    elif args.sma:
        algorithm = 'sma'
        parameter = args.sma
    
    # Setup logging with algorithm name
    logger, log_file = setup_logging(algorithm)
    logger.info(f"Log file: {log_file}")
    
    # Read puzzle from stdin
    try:
        puzzle = read_puzzle(logger)
    except Exception as e:
        print(f"Error reading puzzle: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Solve the puzzle
    try:
        logger.info("=" * 60)
        logger.info(f"Solving puzzle using {algorithm.upper()}")
        solved, iterations = solve_puzzle(puzzle, algorithm, parameter, logger)
    except KeyboardInterrupt:
        logger.warning("Search interrupted by user")
        print("\nSearch interrupted", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during search: {e}", exc_info=True)
        print(f"Error during search: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Output results
    if solved is None:
        logger.info("No solution found")
        print(-1)
        print()
    else:
        solution = ''.join(solved.history)
        logger.info(f"Solution found! Length: {len(solution)} moves")
        logger.info(f"Solution: {solution}")
        logger.info("=" * 60)
        print(len(solution))
        print(solution)


if __name__ == "__main__":
    main()

