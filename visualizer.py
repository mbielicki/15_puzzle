"""
Puzzle Solution Visualizer
Displays puzzle states step-by-step with navigation controls
"""

import tkinter as tk
from tkinter import ttk
import sys
from puzzle import Puzzle


class PuzzleVisualizer:
    def __init__(self, root, initial_puzzle, solution):
        self.root = root
        self.root.title("15-Puzzle Solution Visualizer")
        
        self.initial_puzzle = initial_puzzle
        self.solution = solution
        self.current_step = 0
        
        # Generate all puzzle states
        self.states = self._generate_states()
        
        # Setup UI
        self._setup_ui()
        self._update_display()
    
    def _generate_states(self):
        """Generate all puzzle states from initial state and solution"""
        states = [self.initial_puzzle.copy()]
        current = self.initial_puzzle.copy()
        
        for move in self.solution:
            try:
                current.move(move)
                states.append(current.copy())
            except (ValueError, IndexError) as e:
                raise ValueError(f"Invalid move '{move}' in solution: {e}")
        
        return states
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text=f"{self.initial_puzzle.size}x{self.initial_puzzle.size} Puzzle Solution",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Puzzle grid frame
        self.puzzle_frame = ttk.Frame(main_frame)
        self.puzzle_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Step info
        self.step_label = ttk.Label(
            main_frame,
            text="",
            font=("Arial", 12)
        )
        self.step_label.grid(row=2, column=0, columnspan=3, pady=5)
        
        # Solution text
        solution_label = ttk.Label(
            main_frame,
            text=f"Solution: {self.solution}",
            font=("Arial", 10)
        )
        solution_label.grid(row=3, column=0, columnspan=3, pady=5)
        
        solution_info = ttk.Label(
            main_frame,
            text=f"Solution length: {len(self.solution)} moves",
            font=("Arial", 10)
        )
        solution_info.grid(row=4, column=0, columnspan=3, pady=(0, 15))
        
        # Navigation buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        self.prev_button = ttk.Button(
            button_frame,
            text="← Previous",
            command=self._previous_step,
            width=15
        )
        self.prev_button.grid(row=0, column=0, padx=5)
        
        self.reset_button = ttk.Button(
            button_frame,
            text="Reset",
            command=self._reset,
            width=15
        )
        self.reset_button.grid(row=0, column=1, padx=5)
        
        self.next_button = ttk.Button(
            button_frame,
            text="Next →",
            command=self._next_step,
            width=15
        )
        self.next_button.grid(row=0, column=2, padx=5)
        
        # Keyboard bindings
        self.root.bind('<Left>', lambda e: self._previous_step())
        self.root.bind('<Right>', lambda e: self._next_step())
        self.root.bind('<Home>', lambda e: self._reset())
        self.root.bind('<End>', lambda e: self._go_to_end())
    
    def _create_tile(self, parent, value, row, col, size=80):
        """Create a single tile"""
        tile = tk.Frame(
            parent,
            width=size,
            height=size,
            relief=tk.RAISED if value != 0 else tk.FLAT,
            borderwidth=2,
            bg="#34495e" if value != 0 else "#ecf0f1"
        )
        tile.grid(row=row, column=col, padx=2, pady=2)
        tile.grid_propagate(False)
        
        if value != 0:
            label = tk.Label(
                tile,
                text=str(value),
                font=("Arial", 24, "bold"),
                bg="#34495e",
                fg="white"
            )
            label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def _update_display(self):
        """Update the puzzle display"""
        # Clear existing puzzle
        for widget in self.puzzle_frame.winfo_children():
            widget.destroy()
        
        # Get current state
        current_state = self.states[self.current_step]
        
        # Create tiles
        for row in range(current_state.size):
            for col in range(current_state.size):
                value = current_state.array[col][row]
                self._create_tile(self.puzzle_frame, value, row, col)
        
        # Update step label
        if self.current_step == 0:
            step_text = "Initial State"
            move_text = ""
        elif self.current_step == len(self.states) - 1:
            step_text = "Goal State Reached!"
            move_text = f"Last move: {self.solution[self.current_step - 1]}"
        else:
            step_text = f"Step {self.current_step} of {len(self.solution)}"
            move_text = f"Move: {self.solution[self.current_step - 1]}"
        
        self.step_label.config(text=f"{step_text}   {move_text}")
        
        # Update button states
        self.prev_button.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_step < len(self.states) - 1 else tk.DISABLED)
    
    def _previous_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self._update_display()
    
    def _next_step(self):
        """Go to next step"""
        if self.current_step < len(self.states) - 1:
            self.current_step += 1
            self._update_display()
    
    def _reset(self):
        """Reset to initial state"""
        self.current_step = 0
        self._update_display()
    
    def _go_to_end(self):
        """Go to final state"""
        self.current_step = len(self.states) - 1
        self._update_display()


def read_puzzle_input():
    """Read puzzle dimensions and initial state from stdin"""
    first_line = input().strip().split()
    rows, cols = int(first_line[0]), int(first_line[1])
    
    if rows != cols:
        raise ValueError("Only square puzzles are supported")
    
    size = rows
    
    data = []
    for _ in range(rows):
        row = list(map(int, input().strip().split()))
        data.extend(row)
    
    return Puzzle(size=size, data=data)


def main():
    print("Enter puzzle dimensions and initial state:")
    print("(Format: rows cols, then board rows)")
    
    try:
        puzzle = read_puzzle_input()
        
        print("\nEnter solution (e.g., URRRDDLURULLL):")
        solution = input().strip()
        
        if not solution:
            print("Error: Solution cannot be empty")
            sys.exit(1)
        
        # Validate solution characters
        valid_moves = {'U', 'D', 'L', 'R'}
        if not all(move in valid_moves for move in solution):
            print("Error: Solution contains invalid moves. Use only U, D, L, R")
            sys.exit(1)
        
        # Create GUI
        root = tk.Tk()
        app = PuzzleVisualizer(root, puzzle, solution)
        root.mainloop()
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
