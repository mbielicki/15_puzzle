"""Test all algorithms on puzzle and collect results."""

import sys
sys.path.insert(0, '.')

from puzzle import Puzzle
from utils.logging_config import setup_logging
from utils.solver import solve_puzzle
import time

puzzle_file = "inputs/puzzle_4x4_10moves.txt"

algorithms = [
    ("BFS UDLR", "bfs", "UDLR"),
    ("BFS DULR", "bfs", "DULR"),
    ("BFS LRUD", "bfs", "LRUD"),
    ("BFS RDUL", "bfs", "RDUL"),
    ("DFS UDLR", "dfs", "UDLR"),
    ("DFS DULR", "dfs", "DULR"),
    ("DFS LRUD", "dfs", "LRUD"),
    ("DFS RDUL", "dfs", "RDUL"),
    ("IDDFS UDLR", "idfs", "UDLR"),
    ("IDDFS DULR", "idfs", "DULR"),
    ("IDDFS LRUD", "idfs", "LRUD"),
    ("A* h=0", "astar", "0"),
    ("A* h=1 (Manhattan)", "astar", "1"),
    ("A* h=2 (Hamming)", "astar", "2"),
    ("Best-First h=0", "bf", "0"),
    ("Best-First h=1 (Manhattan)", "bf", "1"),
    ("Best-First h=2 (Hamming)", "bf", "2"),
    ("SMA* h=0", "sma", "0"),
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
print(f"Testing all algorithms on {puzzle_file}")
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
        solved, iterations = solve_puzzle(puzzle, algorithm, parameter, logger)
        elapsed = time.time() - start_time
        
        if solved is not None:
            moves = len(solved.history)
            solution = ''.join(solved.history)
            print(f"[OK] Solution: {moves} moves, {iterations:,} iterations in {elapsed:.2f}s")
            print(f"  Moves: {solution}")
            results.append((name, moves, solution, elapsed, iterations, "SUCCESS"))
        else:
            print(f"[FAIL] No solution found, {iterations:,} iterations in {elapsed:.2f}s")
            results.append((name, -1, "", elapsed, iterations, "NO SOLUTION"))
    
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"[INTERRUPTED] Interrupted after {elapsed:.2f}s")
        results.append((name, -1, "", elapsed, None, "INTERRUPTED"))
        break
    
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"[EXCEPTION] Exception: {e}")
        results.append((name, -1, "", elapsed, None, "EXCEPTION"))

print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"{'Algorithm':<30} {'Moves':<8} {'Iterations':<15} {'Time (s)':<12} {'Status':<15}")
print("-" * 100)

for name, moves, solution, elapsed, iterations, status in results:
    moves_str = str(moves) if moves >= 0 else "N/A"
    iter_str = f"{iterations:,}" if iterations is not None else "N/A"
    print(f"{name:<30} {moves_str:<8} {iter_str:<15} {elapsed:<12.2f} {status:<15}")

print("=" * 100)
