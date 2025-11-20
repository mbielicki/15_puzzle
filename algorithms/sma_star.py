from puzzle import Puzzle
import logging
import heapq
from algorithms.heuristics import manhattan_distance
from typing import Tuple, Optional


class SMAStarNode:
    """Node class for SMA* algorithm to track f-values and maintain tree structure."""
    
    def __init__(self, puzzle: Puzzle, g: int, h: int, parent=None):
        self.puzzle = puzzle
        self.g = g  # Cost from start
        self.h = h  # Heuristic to goal
        self.f = g + h  # Total estimated cost
        self.parent = parent
        self.forgotten_f = None  # Best f-value of forgotten descendants
    
    def __lt__(self, other):
        # For heap ordering: prefer lower f, then higher g (deeper in tree)
        if self.f != other.f:
            return self.f < other.f
        return self.g > other.g


def sma_star(puzzle: Puzzle, depth_limit: int, max_nodes: int = 10000, order: str = "UDLR", heuristic=None, logger: logging.Logger = None) -> Tuple[Optional[Puzzle], int, int]:
    """SMA* (Simplified Memory-bounded A*) algorithm.
    
    Memory-efficient variant of A* that limits the number of nodes in memory.
    When memory is full, removes the worst (highest f-value) leaf nodes.
    Stores the best forgotten f-value to allow regeneration if needed.
    
    Args:
        puzzle: Initial puzzle state
        depth_limit: Maximum depth to search
        max_nodes: Maximum number of nodes to keep in memory
        order: Order of move exploration (default "UDLR")
        heuristic: Heuristic function to use (default manhattan_distance)
        logger: Optional logger for debugging
    """
    if heuristic is None:
        heuristic = manhattan_distance
    
    # Initialize with root node
    h = heuristic(puzzle)
    root = SMAStarNode(puzzle, g=0, h=h)
    
    # Priority queue for open nodes (to be expanded)
    # Format: (node)
    open_heap = [root]
    
    # Track all nodes in memory (both open and closed)
    nodes_in_memory = {puzzle.__repr__(): root}
    
    # Visited states (for quick lookup)
    visited = set()
    
    iteration = 0
    max_frontier_size = 1

    while open_heap:
        iteration += 1
        max_frontier_size = max(max_frontier_size, len(open_heap))
        
        # Get the most promising node
        current_node = heapq.heappop(open_heap)
        current_puzzle = current_node.puzzle
        
        if logger:
            logger.info(f"Iter {iteration}: depth={len(current_puzzle.history)}, queue={len(open_heap)}, visited={len(visited)}, f={current_node.f}")
        
        # Goal test
        if current_puzzle.is_solved():
            if logger:
                logger.info(f"Solution found! Iterations: {iteration}, Moves: {len(current_puzzle.history)}, Max frontier: {max_frontier_size}")
            return (current_puzzle, iteration, max_frontier_size)
        
        # Mark as visited
        state = current_puzzle.__repr__()
        visited.add(state)
        
        # Check depth limit
        if len(current_puzzle.history) >= depth_limit:
            continue
        
        # Define move operations
        move_operations = {
            "U": (current_puzzle.can_move("U") and current_puzzle.previous_move() != "D", lambda p: p.up()),
            "D": (current_puzzle.can_move("D") and current_puzzle.previous_move() != "U", lambda p: p.down()),
            "L": (current_puzzle.can_move("L") and current_puzzle.previous_move() != "R", lambda p: p.left()),
            "R": (current_puzzle.can_move("R") and current_puzzle.previous_move() != "L", lambda p: p.right())
        }
        
        # Generate successors
        successors = []
        for move in order:
            if move in move_operations:
                can_move, operation = move_operations[move]
                if can_move:
                    new_puzzle = current_puzzle.copy()
                    operation(new_puzzle)
                    new_state = new_puzzle.__repr__()
                    
                    # Skip if already visited
                    if new_state in visited:
                        continue
                    
                    new_g = len(new_puzzle.history)
                    new_h = heuristic(new_puzzle)
                    new_node = SMAStarNode(new_puzzle, new_g, new_h, parent=current_node)
                    successors.append((new_state, new_node))
        
        # Add successors to open heap and track in memory
        for state, node in successors:
            # Memory management: if at capacity, remove worst leaf node
            if len(nodes_in_memory) >= max_nodes:
                # Find the worst (highest f-value) leaf node in open heap
                if open_heap:
                    # Remove the worst node (last in sorted order)
                    worst_node = max(open_heap, key=lambda n: (n.f, -n.g))
                    open_heap.remove(worst_node)
                    heapq.heapify(open_heap)
                    
                    # Remove from memory tracking
                    worst_state = worst_node.puzzle.__repr__()
                    if worst_state in nodes_in_memory:
                        del nodes_in_memory[worst_state]
                    
                    # Store forgotten f-value in parent
                    if worst_node.parent:
                        if worst_node.parent.forgotten_f is None:
                            worst_node.parent.forgotten_f = worst_node.f
                        else:
                            worst_node.parent.forgotten_f = min(worst_node.parent.forgotten_f, worst_node.f)
            
            # Add new node
            heapq.heappush(open_heap, node)
            nodes_in_memory[state] = node
    
    if logger:
        logger.info(f"No solution found. Iterations: {iteration}, Depth limit: {depth_limit}, Max frontier: {max_frontier_size}")
    return (None, iteration, max_frontier_size)
    return (None, iteration)
