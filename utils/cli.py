"""Command-line argument parsing for puzzle solver."""

import argparse


def parse_arguments():
    """Parse command line arguments.
    
    Returns:
        Namespace: Parsed command-line arguments
    """
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
