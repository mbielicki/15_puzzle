"""Test all algorithms on puzzle_4x4_10moves.txt and collect results."""

import subprocess
import time
import re

puzzle_file = "inputs/puzzle_4x4_10moves.txt"
python_exe = "C:/dev/15_puzzle/.venv/Scripts/python.exe"

algorithms = [
    ("BFS UDLR", "-b", "UDLR"),
    ("BFS DULR", "-b", "DULR"),
    ("BFS LRUD", "-b", "LRUD"),
    ("BFS RDUL", "-b", "RDUL"),
    ("DFS UDLR", "-d", "UDLR"),
    ("DFS DULR", "-d", "DULR"),
    ("DFS LRUD", "-d", "LRUD"),
    ("DFS RDUL", "-d", "RDUL"),
    ("IDDFS UDLR", "-i", "UDLR"),
    ("IDDFS DULR", "-i", "DULR"),
    ("IDDFS LRUD", "-i", "LRUD"),
    ("A* h=0", "-a", "0"),
    ("A* h=1 (Manhattan)", "-a", "1"),
    ("A* h=2 (Hamming)", "-a", "2"),
    ("Best-First h=0", "-h", "0"),
    ("Best-First h=1 (Manhattan)", "-h", "1"),
    ("Best-First h=2 (Hamming)", "-h", "2"),
    ("SMA* h=0", "-s", "0"),
    ("SMA* h=1 (Manhattan)", "-s", "1"),
    ("SMA* h=2 (Hamming)", "-s", "2"),
]

results = []

print("=" * 100)
print(f"Testing all algorithms on {puzzle_file}")
print("=" * 100)

for name, flag, param in algorithms:
    print(f"\n{'=' * 100}")
    print(f"Running: {name}")
    print(f"Command: python main.py {flag} {param}")
    print("=" * 100)
    
    start_time = time.time()
    
    try:
        with open(puzzle_file, 'r') as f:
            result = subprocess.run(
                [python_exe, "main.py", flag, param],
                stdin=f,
                capture_output=True,
                text=True,
                timeout=120
            )
        
        elapsed = time.time() - start_time
        
        # Extract iterations from stderr log (whether successful or not)
        iterations = None
        if "Iterations:" in result.stderr:
            # Try both "Iterations:" and "Total iterations:" formats
            match = re.search(r'(?:Total )?Iterations:\s*(\d+)', result.stderr)
            if match:
                iterations = int(match.group(1))
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                moves = int(lines[0])
                solution = lines[1] if len(lines) > 1 else ""
                iter_str = f"{iterations:,}" if iterations else "N/A"
                print(f"[OK] Solution: {moves} moves, {iter_str} iterations in {elapsed:.2f}s")
                print(f"  Moves: {solution}")
                results.append((name, moves, solution, elapsed, iterations, "SUCCESS"))
            else:
                print(f"[FAIL] No solution found in {elapsed:.2f}s")
                results.append((name, -1, "", elapsed, iterations, "NO SOLUTION"))
        else:
            print(f"[ERROR] Error (exit code {result.returncode}) in {elapsed:.2f}s")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
            results.append((name, -1, "", elapsed, iterations, "ERROR"))
    
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"[TIMEOUT] Timeout after {elapsed:.2f}s")
        results.append((name, -1, "", elapsed, None, "TIMEOUT"))
    
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
    iter_str = f"{iterations:,}" if iterations else "N/A"
    print(f"{name:<30} {moves_str:<8} {iter_str:<15} {elapsed:<12.2f} {status:<15}")

print("=" * 100)

