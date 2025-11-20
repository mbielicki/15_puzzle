# 15-Puzzle Solver: Algorithm Comparison Report

## 1. Introduction

### 1.1 Problem Overview

The 15-puzzle is a sliding puzzle consisting of a 4×4 grid with 15 numbered tiles and one empty space. The goal is to rearrange the tiles from a scrambled initial configuration to reach the goal state where tiles are ordered sequentially (1-15) with the empty space in the bottom-right corner.

The 15-puzzle is computationally challenging due to its large state space. With 16 positions and 16 different tiles (including the empty space), there are 16! possible configurations, though only half of these are reachable from any given starting position due to parity constraints. This results in approximately 10.4 trillion solvable states, making exhaustive search impractical for deep solutions.

The puzzle serves as an excellent benchmark for comparing different search algorithms, as it provides a well-defined problem with measurable metrics including solution optimality, iteration count, execution time, and memory usage.

### 1.2 Algorithms Implemented

This project implements and compares six different search algorithms:

**Uninformed Search Algorithms:**
- **Breadth-First Search (BFS)**: Explores states level by level, guaranteeing optimal solutions
- **Depth-First Search (DFS)**: Explores deeply before backtracking, requires depth limiting
- **Iterative Deepening DFS (IDDFS)**: Combines BFS optimality with DFS memory efficiency

**Informed Search Algorithms:**
- **Best-First Search**: Greedy search using heuristic function only
- **A\* Search**: Optimal search using f(n) = g(n) + h(n) with admissible heuristics
- **Simplified Memory-Bounded A\* (SMA\*)**: Memory-limited variant of A\*

All algorithms were tested with various configurations including different move orderings and heuristic functions to provide comprehensive performance comparisons.

### 1.3 Usage

The puzzle solver is executed through `main.py`, which provides a command-line interface for algorithm selection and configuration.

**Basic Command Structure:**
```bash
python main.py -<algorithm> <parameter>
```

**Algorithm Selection and Parameters:**

The parameter depends on the algorithm selected:

*Uninformed Search Algorithms (BFS, DFS, IDDFS):*
- `-b` or `--bfs ORDER`: Breadth-First Search
- `-d` or `--dfs ORDER`: Depth-First Search
- `-i` or `--idfs`: Iterative Deepening DFS
- **Parameter (ORDER)**: Move ordering strategy
  - `LRUD`: Left, Right, Up, Down
  - `RDUL`: Right, Down, Up, Left
  - `UDLR`: Up, Down, Left, Right
  - `DURL`: Down, Up, Right, Left
  - `RAND`: Random ordering at each node (non-deterministic)

*Informed Search Algorithms (Best-First, A\*, SMA\*):*
- `-f` or `--bf HEURISTIC`: Best-First Search
- `-a` or `--astar HEURISTIC`: A\* Search
- `-s` or `--sma HEURISTIC`: SMA\* Search
- **Parameter (HEURISTIC)**: Heuristic function identifier
  - `0`: No heuristic (equivalent to uninformed search)
  - `1`: Manhattan distance
  - `2`: Hamming distance (misplaced tiles)

**Input Format:**

The puzzle is provided via standard input, either piped from a file or entered directly. The input format requires:

1. First line: Puzzle dimensions as `rows cols` (e.g., `4 4` for a 4×4 puzzle)
2. Following lines: Grid configuration where each number represents a tile and `0` represents the empty space

Example input for a 4×4 puzzle:
```
4 4
1 2 3 4
5 6 7 8
9 10 0 11
13 14 15 12
```

**Example Commands:**

```bash
# BFS with LRUD move ordering
Get-Content inputs/puzzle_4x4_10moves.txt | python main.py -b LRUD

# A* with Manhattan distance heuristic
Get-Content inputs/puzzle_4x4_10moves.txt | python main.py -a 1

# IDDFS with random move ordering
Get-Content inputs/puzzle_4x4_10moves.txt | python main.py -i RAND

# Best-First with Hamming distance heuristic
Get-Content inputs/puzzle_4x4_10moves.txt | python main.py -f 2
```

**Output:**

The program outputs the solution path (sequence of moves), number of iterations performed, and execution time. Detailed logs are written to timestamped files in the `logs/` directory for further analysis.

## 2. Uninformed Search Algorithms

Uninformed search algorithms, also known as blind search algorithms, explore the state space without using any domain-specific knowledge or heuristics. They rely solely on the problem definition and systematically traverse the search tree until a solution is found or the search space is exhausted.

### 2.1 Breadth-First Search (BFS)

**Algorithm Description:**

Breadth-First Search explores the state space level by level, examining all states at depth *d* before moving to states at depth *d+1*. It uses a queue (FIFO - First In, First Out) data structure to maintain the frontier of unexplored states.

**Key Characteristics:**

- **Completeness**: BFS is complete - it will find a solution if one exists
- **Optimality**: BFS guarantees finding the shortest solution path (optimal for unit-cost paths)
- **Visited Set**: Uses a visited set to avoid re-exploring states, ensuring each state is processed only once
- **Time Complexity**: O(b^d) where *b* is the branching factor and *d* is the solution depth
- **Space Complexity**: O(b^d) - can be memory-intensive for deep solutions as it stores all frontier nodes

**Implementation Details:**

The BFS implementation maintains a queue of puzzle states and a visited set. At each iteration, it:
1. Removes the next state from the front of the queue
2. Checks if it's the goal state
3. Marks it as visited
4. Generates all valid successor states (respecting depth limits and avoiding reverse moves)
5. Adds unvisited successors to the back of the queue

The algorithm respects a depth limit to prevent excessive exploration and avoids immediate move reversals (e.g., moving Up after Down) to reduce redundant states.

### 2.2 Depth-First Search (DFS)

**Algorithm Description:**

Depth-First Search explores the state space by following a single path as deeply as possible before backtracking. It uses a stack (LIFO - Last In, First Out) data structure, which can be implemented explicitly (iterative) or implicitly through recursion.

**Key Characteristics:**

- **Completeness**: DFS is complete only with a depth limit - without one, it may explore infinitely deep paths
- **Optimality**: DFS does not guarantee optimal solutions - it finds the first solution encountered, which may not be shortest
- **Time Complexity**: O(b^d) in the worst case, where all paths up to depth *d* are explored
- **Space Complexity**: O(d) where *d* is the search depth - much more memory-efficient than BFS
- **Depth Limit Necessity**: A depth limit is essential to prevent infinite exploration and ensure termination

**The Visited Set Problem:**

A critical implementation consideration for depth-limited DFS is whether to use a visited set. When using depth-limited DFS with a visited set, you can miss solutions because you skip states that were visited via a longer path, even though a shorter path to that same state would lead to a solution within the depth limit.

For example, suppose the depth limit is *D*:
- You first reach state *X* via a long path of length *L* steps and mark it visited
- This path leaves only *D - L* remaining steps, insufficient to reach the solution
- Later, you discover a shorter path to *X* of length *S* steps (where *S < L*)
- But *X* is already marked visited, so you skip it
- However, the shorter path would have left *D - S* steps remaining, which might be enough to find the solution

**Trade-off**: Our implementation does not use a visited set for DFS, allowing it to find solutions even when states are revisited via shorter paths, at the cost of potentially exploring the same state multiple times.

### 2.3 Iterative Deepening DFS (IDDFS)

**Algorithm Description:**

Iterative Deepening Depth-First Search combines the space efficiency of DFS with the optimality guarantee of BFS. It performs a series of depth-limited DFS searches with increasing depth limits: first depth 0, then depth 1, then depth 2, and so on until a solution is found.

**Key Characteristics:**

- **Completeness**: IDDFS is complete like BFS
- **Optimality**: IDDFS guarantees optimal solutions like BFS
- **Time Complexity**: O(b^d) - performs more iterations than BFS due to repeated exploration of shallow states
- **Space Complexity**: O(d) like DFS - only stores the current search path

**Why IDDFS Does More Iterations Than BFS:**

IDDFS performs significantly more iterations than BFS to find the same solution, even though both algorithms are optimal. From our test results:
- BFS LRUD: 3,470 iterations → 10-move solution
- IDDFS LRUD: 6,890 iterations → 10-move solution

**Reason: Redundant Work**

IDDFS repeatedly visits the same states across multiple depth iterations:
1. Depth 0: Explores root node (1 iteration)
2. Depth 1: Explores root + depth-1 nodes (multiple iterations)
3. Depth 2: Explores root + depth-1 + depth-2 nodes (even more iterations)
4. ...continues until solution depth...

Each iteration restarts from the root and re-explores all shallower levels. States near the root are visited many times (once per depth level from 0 to the solution depth).

In contrast, **BFS visits each state exactly once** using a queue and visited set, so it never re-explores states.

**Why Use IDDFS?**

Despite the redundant work, IDDFS offers crucial advantages:
- **Memory Efficiency**: BFS stores all frontier nodes in memory (can be enormous), while IDDFS only stores the current path (O(d) vs O(b^d) space)
- **Scalability**: For deep solutions or large branching factors, the memory savings outweigh the redundant iterations
- **Optimal + Space-Efficient**: The only algorithm combining BFS's optimality with DFS's memory efficiency

**Trade-off Summary:**
- IDDFS: More iterations, less memory, optimal
- BFS: Fewer iterations, more memory, optimal
- DFS: Fewer iterations, less memory, not optimal

### 2.4 Move Ordering Strategies

The order in which possible moves are explored can significantly impact the search performance, especially for uninformed algorithms that lack heuristic guidance.

#### 2.4.1 Standard Orders (LRUD, RDUL, UDLR, DURL)

Move ordering determines the sequence in which the algorithm considers valid moves from any given state. The user can specify any arbitrary ordering of the four moves (U, D, L, R). Common orderings include:

- **LRUD** (Left, Right, Up, Down): Prioritizes horizontal moves before vertical
- **RDUL** (Right, Down, Up, Left): Reverse-priority ordering
- **UDLR** (Up, Down, Left, Right): Prioritizes vertical moves before horizontal
- **DURL** (Down, Up, Right, Left): Alternative vertical-first ordering

**Impact on Search:**

Different move orders can dramatically affect the number of iterations required to find a solution:
- The order determines which branches of the search tree are explored first
- A fortunate ordering may find the solution quickly; an unfortunate one explores many wrong paths
- For BFS, different orderings produce the same solution length (optimal) but different iteration counts
- For DFS, different orderings can produce both different solution lengths and different iteration counts

From our test results, BFS performance varied significantly by move order:
- BFS LRUD: 3,470 iterations
- BFS RDUL: 2,618 iterations (best)
- BFS UDLR: 4,848 iterations (worst)

This variance demonstrates how critical move ordering is for uninformed search efficiency.

#### 2.4.2 Random Order (RAND)

The RAND ordering introduces non-deterministic behavior by randomly shuffling the move order at each node expansion.

**Implementation:**

Unlike standard orderings that use a fixed sequence throughout the search, RAND creates a fresh random permutation of [U, D, L, R] at every node. This means:
- Each state expansion uses a different random ordering
- The same puzzle may take different paths across multiple runs
- Iteration counts and execution times vary between runs

**Characteristics:**

- **Non-Deterministic**: Different results on each execution
- **Exploration Diversity**: Avoids systematic bias of fixed orderings
- **Variable Performance**: May find solutions quickly or slowly depending on random choices
