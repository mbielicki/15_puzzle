"""
Generate a shuffled puzzle and save it to the inputs/ directory.

Usage:
    python generate_puzzle.py [--size SIZE] [--moves MOVES] [--name NAME]
"""

import argparse
import random
import os
from puzzle import Puzzle


def generate_shuffled_puzzle(size=4, num_moves=100):
    """
    Generate a shuffled puzzle by applying random valid moves.
    
    Args:
        size: Size of the puzzle (3 for 3x3, 4 for 4x4, etc.)
        num_moves: Number of random moves to apply
        
    Returns:
        Puzzle: A shuffled puzzle instance
    """
    # Create puzzle and shuffle it
    puzzle = Puzzle(size=size)
    puzzle.shuffle(num_moves)
    
    return puzzle


def save_puzzle(puzzle, filename):
    """
    Save puzzle to file in the format expected by main.py.
    
    Args:
        puzzle: Puzzle instance to save
        filename: Path to output file
    """
    # Ensure inputs directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        # Write dimensions
        f.write(f"{puzzle.size} {puzzle.size}\n")
        
        # Write grid
        for row in puzzle.array.T:
            f.write(' '.join(map(str, row)) + '\n')


def main():
    parser = argparse.ArgumentParser(
        description='Generate a shuffled puzzle and save it to inputs/ directory',
        add_help=True
    )
    parser.add_argument(
        '--size', '-s',
        type=int,
        default=4,
        help='Size of the puzzle (default: 4 for 4x4)'
    )
    parser.add_argument(
        '--moves', '-m',
        type=int,
        default=100,
        help='Number of random moves to apply (default: 100)'
    )
    parser.add_argument(
        '--name', '-n',
        type=str,
        default=None,
        help='Output filename (default: puzzle_SIZExSIZE_MOVES.txt)'
    )
    
    args = parser.parse_args()
    
    # Generate puzzle
    print(f"Generating {args.size}x{args.size} puzzle with {args.moves} random moves...")
    puzzle = generate_shuffled_puzzle(args.size, args.moves)
    
    # Determine output filename
    if args.name:
        filename = f"inputs/{args.name}"
        if not filename.endswith('.txt'):
            filename += '.txt'
    else:
        filename = f"inputs/puzzle_{args.size}x{args.size}_{args.moves}moves.txt"
    
    # Save puzzle
    save_puzzle(puzzle, filename)
    print(f"Puzzle saved to: {filename}")
    
    # Display puzzle
    print("\nGenerated puzzle:")
    print(puzzle)


if __name__ == '__main__':
    main()
