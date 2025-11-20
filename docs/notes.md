# Observations

## Why IDDFS Does More Iterations Than BFS

IDDFS (Iterative Deepening Depth-First Search) performs significantly more iterations than BFS to find the same solution, even though both algorithms are optimal and find the shortest path.

**Example from test results:**
- BFS LRUD: 2,618 iterations → 10-move solution
- IDDFS LRUD: 6,890 iterations → 10-move solution

**Reason: Redundant Work**

IDDFS repeatedly visits the same states across multiple depth iterations:

1. **Depth 0**: Explores root node (1 iteration)
2. **Depth 1**: Explores root + depth-1 nodes (multiple iterations)
3. **Depth 2**: Explores root + depth-1 + depth-2 nodes (even more iterations)
4. ...continues until solution depth...

Each iteration restarts from the root and re-explores all shallower levels. States near the root are visited many times (once per depth level).

**BFS visits each state exactly once** using a queue and visited set, so it never re-explores states.

**Why use IDDFS then?**
- Memory efficiency: BFS stores all frontier nodes in memory (can be huge), while IDDFS only stores the current path (O(d) vs O(b^d) space)
- For deep solutions or large branching factors, the memory savings outweigh the redundant iterations

**Trade-off:**
- IDDFS: More iterations, less memory
- BFS: Fewer iterations, more memory

## Visited set and depth limit

The Problem:

When using depth-limited DFS with a visited set, you can miss solutions because you skip states that were visited via a longer path, even though a shorter path to that same state would lead to a solution within the depth limit.

Example:

Suppose the depth limit is D.

- First, you reach state X via a long path of length L steps
- You mark X as visited
- This path is too long - you only have (D - L) steps remaining, which isn't enough to reach the solution from X
- Later, you discover a shorter path to X of length S steps (where S < L)
- But X is already marked as visited, so you skip it
- However, from X you need M more steps to reach the solution
- S + M would be less than D (within the limit), but you never try because X was already visited

The key issue: The visited set prevents revisiting X, even though reaching X via the shorter S-step path (instead of the L-step path) would have left enough remaining depth (D - S) to find the solution in M more steps.
