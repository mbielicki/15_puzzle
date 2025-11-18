import sys
import argparse
import random
from puzzle import Puzzle
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.iddfs import iddfs
from algorithms.best_first_search import best_first_search
from algorithms.a_star import a_star
from algorithms.sma_star import sma_star
from algorithms.heuristics import get_heuristic


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='15-Puzzle Solver', add_help=False)
    
    # Add custom help
    parser.add_argument('--help', action='help', help='Show this help message and exit')
    
    # Create mutually exclusive group for algorithms
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-b', '--bfs', metavar='ORDER', help='Breadth-first search with move order')
    group.add_argument('-d', '--dfs', metavar='ORDER', help='Depth-first search with move order')
    group.add_argument('-i', '--idfs', metavar='ORDER', help='Iterative deepening DFS with move order')
    group.add_argument('-h', '--bf', metavar='HEURISTIC', help='Best-first strategy with heuristic ID')
    group.add_argument('-a', '--astar', metavar='HEURISTIC', help='A* strategy with heuristic ID')
    group.add_argument('-s', '--sma', metavar='HEURISTIC', help='SMA* strategy with heuristic ID')
    
    return parser.parse_args()


def read_puzzle():
    """Read puzzle configuration from standard input.
    
    Returns:
        Puzzle: Initialized puzzle object
    """
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
        print("Error: Only square puzzles are supported", file=sys.stderr)
        sys.exit(1)
    
    size = rows
    
    # Read puzzle data
    data = []
    for _ in range(rows):
        line = input().strip().split()
        data.extend([int(x) for x in line])
    
    return Puzzle(size=size, data=data)


def get_move_order(order_str):
    """Process move order string.
    
    Args:
        order_str: String defining move order (e.g., 'DULR' or 'RANDU')
    
    Returns:
        str: Processed move order. If starts with 'R', returns random permutation.
    """
    if order_str.upper().startswith('R'):
        # Random order
        moves = ['L', 'R', 'U', 'D']
        random.shuffle(moves)
        return ''.join(moves)
    else:
        return order_str.upper()


def solve_puzzle(puzzle, algorithm, parameter, depth_limit=50):
    """Solve the puzzle using the specified algorithm.
    
    Args:
        puzzle: Puzzle object to solve
        algorithm: Algorithm name ('bfs', 'dfs', 'idfs', 'bf', 'astar', 'sma')
        parameter: Move order or heuristic ID
        depth_limit: Maximum search depth
    
    Returns:
        Puzzle or None: Solved puzzle if solution found, None otherwise
    """
    if algorithm in ['bfs', 'dfs', 'idfs']:
        order = get_move_order(parameter)
        
        if algorithm == 'bfs':
            return bfs(puzzle, depth_limit, order)
        elif algorithm == 'dfs':
            return dfs(puzzle, depth_limit, order)
        elif algorithm == 'idfs':
            return iddfs(puzzle, depth_limit, order)
    
    elif algorithm in ['bf', 'astar', 'sma']:
        # For heuristic-based algorithms
        heuristic_id = parameter
        heuristic = get_heuristic(heuristic_id)
        order = 'UDLR'  # Default order for heuristic searches
        
        if algorithm == 'bf':
            return best_first_search(puzzle, depth_limit, order, heuristic)
        elif algorithm == 'astar':
            return a_star(puzzle, depth_limit, order, heuristic)
        elif algorithm == 'sma':
            return sma_star(puzzle, depth_limit, max_nodes=10000, order=order, heuristic=heuristic)
    
    return None


def main():
    """Main entry point for the puzzle solver."""
    args = parse_arguments()
    
    # Read puzzle from stdin
    try:
        puzzle = read_puzzle()
    except Exception as e:
        print(f"Error reading puzzle: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Determine which algorithm to use
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
    
    # Solve the puzzle
    try:
        solved = solve_puzzle(puzzle, algorithm, parameter)
    except KeyboardInterrupt:
        print("\nSearch interrupted", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during search: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Output results
    if solved is None:
        print(-1)
        print()
    else:
        solution = ''.join(solved.history)
        print(len(solution))
        print(solution)


if __name__ == "__main__":
    main()
