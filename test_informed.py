"""Test informed search algorithms on harder puzzles."""

import sys
sys.path.insert(0, '.')

from puzzle import Puzzle
from utils.logging_config import setup_logging
from utils.solver import solve_puzzle
import time

# Test on the 20-move puzzle (harder)
puzzle_file = "inputs/puzzle_4x4_20moves.txt"

# Only informed search algorithms
algorithms = [
    ("Best-First h=1 (Manhattan)", "bf", "1"),
    ("Best-First h=2 (Hamming)", "bf", "2"),
    ("A* h=1 (Manhattan)", "astar", "1"),
    ("A* h=2 (Hamming)", "astar", "2"),
    ("SMA* h=1 (Manhattan)", "sma", "1"),
    ("SMA* h=2 (Hamming)", "sma", "2"),
]

# Read puzzle
with open(puzzle_file, 'r') as f:
    lines = f.readlines()
    rows, cols = map(int, lines[0].split())
    state = []
    for line in lines[1:]:
        state.extend([int(x) if x != '' else 0 for x in line.split()])
    initial_puzzle = Puzzle(size=rows, data=state)

results = []

print("=" * 100)
print(f"Testing informed search algorithms on {puzzle_file}")
print(f"Initial state:")
print(initial_puzzle)
print("=" * 100)

for name, algorithm, parameter in algorithms:
    print(f"\n{'=' * 100}")
    print(f"Running: {name}")
    print("=" * 100)
    
    # Setup logging for this algorithm
    logger, log_file = setup_logging(algorithm)
    
    start_time = time.time()
    
    try:
        puzzle = initial_puzzle.copy()
        solved, iterations, max_frontier = solve_puzzle(puzzle, algorithm, parameter, logger)
        elapsed = time.time() - start_time
        
        if solved is not None:
            moves = len(solved.history)
            solution = ''.join(solved.history)
            print(f"[OK] Solution: {moves} moves, {iterations:,} iterations, max frontier: {max_frontier:,} in {elapsed:.2f}s")
            print(f"  Moves: {solution}")
            results.append((name, moves, solution, elapsed, iterations, max_frontier, "SUCCESS"))
        else:
            print(f"[FAIL] No solution found, {iterations:,} iterations, max frontier: {max_frontier:,} in {elapsed:.2f}s")
            results.append((name, -1, "", elapsed, iterations, max_frontier, "NO SOLUTION"))
    
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"[INTERRUPTED] Interrupted after {elapsed:.2f}s")
        results.append((name, -1, "", elapsed, None, None, "INTERRUPTED"))
        break
    
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"[EXCEPTION] Exception: {e}")
        results.append((name, -1, "", elapsed, None, None, "EXCEPTION"))

print("\n" + "=" * 100)
print("SUMMARY - Informed Search Algorithms on Harder Puzzle")
print("=" * 100)
print(f"{'Algorithm':<30} {'Moves':<8} {'Iterations':<15} {'Max Frontier':<15} {'Time (s)':<12} {'Status':<15}")
print("-" * 100)

for name, moves, solution, elapsed, iterations, max_frontier, status in results:
    moves_str = str(moves) if moves >= 0 else "N/A"
    iter_str = f"{iterations:,}" if iterations is not None else "N/A"
    frontier_str = f"{max_frontier:,}" if max_frontier is not None else "N/A"
    print(f"{name:<30} {moves_str:<8} {iter_str:<15} {frontier_str:<15} {elapsed:<12.2f} {status:<15}")

print("=" * 100)

# Performance comparison
print("\nPERFORMANCE ANALYSIS")
print("=" * 100)

if len(results) > 1:
    successful = [(name, iterations, max_frontier, elapsed) for name, moves, _, elapsed, iterations, max_frontier, status 
                  in results if status == "SUCCESS" and iterations is not None]
    
    if successful:
        print("\nBest Performance by Metric:")
        print("-" * 100)
        
        # Best by iterations
        best_iter = min(successful, key=lambda x: x[1])
        print(f"Fewest Iterations:  {best_iter[0]:<30} {best_iter[1]:,} iterations")
        
        # Best by frontier
        best_frontier = min(successful, key=lambda x: x[2])
        print(f"Smallest Frontier:  {best_frontier[0]:<30} {best_frontier[2]:,} states")
        
        # Best by time
        best_time = min(successful, key=lambda x: x[3])
        print(f"Fastest Time:       {best_time[0]:<30} {best_time[3]:.2f}s")
        
        print("\n" + "=" * 100)
