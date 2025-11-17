# Observations

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
