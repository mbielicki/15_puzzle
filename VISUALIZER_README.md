# Puzzle Solution Visualizer

A GUI application to visualize 15-puzzle solutions step-by-step.

## Quick Start

The easiest way to use the visualizer is with the helper script:

```bash
python run_visualizer.py <puzzle_file> <solution>
```

### Example

```powershell
# First, solve a puzzle to get the solution
Get-Content inputs/puzzle_4x4_15moves.txt | C:/dev/15_puzzle/.venv/Scripts/python.exe main.py -a 1

# Then visualize it (using the solution from above)
C:/dev/15_puzzle/.venv/Scripts/python.exe run_visualizer.py inputs/puzzle_4x4_15moves.txt RULDDRDLULUUL
```

## Manual Usage

Run the visualizer directly:

```bash
python visualizer.py
```

### Input Format

1. Enter puzzle dimensions and initial state (same format as puzzle input files):

```text
4 4
5 1 3 4
2 10 6 8
14 0 7 12
9 13 11 15
```

2. Enter the solution string (e.g., `RULDDRDLULUUL`)

## Controls

- **Next → button** or **Right Arrow**: Move to next step
- **← Previous button** or **Left Arrow**: Move to previous step
- **Reset button** or **Home key**: Return to initial state
- **End key**: Jump to final state

## Features

- Visual representation of puzzle states
- Step-by-step navigation through the solution
- Display of current move and step number
- Solution length and complete solution string
- Keyboard shortcuts for quick navigation
- Color-coded tiles for better visibility

