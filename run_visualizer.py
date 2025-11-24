"""
Helper script to run visualizer with puzzle file and solution
"""

import sys
import subprocess


def main():
    if len(sys.argv) < 3:
        print("Usage: python run_visualizer.py <puzzle_file> <solution>")
        print("\nExample:")
        print('  python run_visualizer.py inputs/puzzle_4x4_15moves.txt RULDDRDLULUUL')
        sys.exit(1)
    
    puzzle_file = sys.argv[1]
    solution = sys.argv[2]
    
    try:
        # Read puzzle file
        with open(puzzle_file, 'r') as f:
            puzzle_content = f.read().strip()
        
        # Prepare input for visualizer
        input_data = f"{puzzle_content}\n{solution}\n"
        
        # Run visualizer
        python_exe = "C:/dev/15_puzzle/.venv/Scripts/python.exe"
        process = subprocess.Popen(
            [python_exe, "visualizer.py"],
            stdin=subprocess.PIPE,
            text=True
        )
        process.communicate(input=input_data)
        
    except FileNotFoundError:
        print(f"Error: Puzzle file '{puzzle_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
