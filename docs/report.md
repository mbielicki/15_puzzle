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

## 3. Informed Search Algorithms

Informed search algorithms, also known as heuristic search algorithms, use domain-specific knowledge to guide the search toward the goal. Unlike uninformed search, these algorithms evaluate states using a heuristic function that estimates the distance or cost to reach the goal, allowing them to prioritize more promising paths.

### 3.1 Best-First Search

**Algorithm Description:**

Best-First Search is a greedy search algorithm that uses a priority queue to explore states, always selecting the state that appears closest to the goal according to the heuristic function. It prioritizes states solely by their heuristic value h(n), without considering the cost to reach them.

**Key Characteristics:**

- **Completeness**: Complete if the state space is finite and a visited set is used
- **Optimality**: Not guaranteed - being greedy, it may find suboptimal solutions
- **Time Complexity**: O(b^d) in the worst case, but typically much better with good heuristics
- **Space Complexity**: O(b^d) - stores frontier and visited states
- **Greedy Nature**: Focuses exclusively on minimizing estimated distance to goal

**Implementation Details:**

The algorithm uses a priority queue (min-heap) where states are ordered by their heuristic value h(n). States with lower heuristic values (estimated to be closer to the goal) are explored first. A counter ensures FIFO ordering for states with identical heuristic values.

**Performance:**

Best-First Search can be very efficient with good heuristics but may get stuck in local minima. From our test results:
- Best-First with Manhattan distance: 11 iterations
- Best-First with Hamming distance: 20 iterations
- Best-First with no heuristic (h=0): 4,848 iterations (equivalent to BFS)

The dramatic reduction in iterations (from 4,848 to 11) demonstrates the power of effective heuristics.

### 3.2 A* Search

**Algorithm Description:**

A* (pronounced "A-star") is an optimal search algorithm that combines the actual cost from the start with a heuristic estimate to the goal. It uses an evaluation function f(n) = g(n) + h(n), where:
- **g(n)**: actual cost from the start state to state n (path length so far)
- **h(n)**: heuristic estimate from state n to the goal
- **f(n)**: estimated total cost of the solution through state n

**Key Characteristics:**

- **Completeness**: Complete if a solution exists
- **Optimality**: Guaranteed optimal if the heuristic is admissible (never overestimates)
- **Time Complexity**: O(b^d) in the worst case, but typically much better with good heuristics
- **Space Complexity**: O(b^d) - must maintain frontier and visited states
- **Admissible Heuristics**: Requires h(n) ≤ true cost to goal for optimality guarantee

**Why A* is Optimal:**

A* is optimal when the heuristic is admissible (never overestimates the true cost). The algorithm maintains the following invariant: if there exists a path of cost C to the goal, A* will find it before exploring any path with f(n) > C. This ensures that the first solution found is optimal.

**Implementation Details:**

States are prioritized by f(n) = g(n) + h(n). The algorithm tracks the actual path cost g(n) for each state and combines it with the heuristic estimate h(n). A visited set prevents re-exploration of states.

**Performance:**

A* with good heuristics dramatically outperforms uninformed search:
- A* with Manhattan distance: 14 iterations, max frontier 18
- A* with Hamming distance: 24 iterations, max frontier 31
- A* with no heuristic (h=0): 4,848 iterations, max frontier 5,061 (equivalent to BFS)

The Manhattan distance heuristic reduces iterations by 99.7% compared to uninformed search (14 vs 4,848).

### 3.3 Simplified Memory-Bounded A* (SMA*)

**Algorithm Description:**

SMA* is a memory-limited variant of A* designed for scenarios where memory constraints prevent storing all frontier nodes. When the number of nodes in memory reaches a specified limit, SMA* removes the worst (highest f-value) leaf nodes. It stores the best forgotten f-value in the parent node, allowing regeneration of pruned subtrees if needed.

**Key Characteristics:**

- **Completeness**: Complete if enough memory exists to store the solution path
- **Optimality**: Optimal like A* if the heuristic is admissible and memory is sufficient
- **Time Complexity**: O(b^d) but may re-explore pruned subtrees
- **Space Complexity**: O(memory limit) - bounded by user-specified constraint
- **Memory Management**: Prunes worst leaf nodes when memory is full

**How It Works:**

1. Maintains a node limit (default 10,000 nodes in our implementation)
2. When memory is full, identifies the worst (highest f-value) leaf node
3. Removes the worst leaf and stores its f-value in the parent's `forgotten_f` field
4. If exploration later suggests a forgotten subtree might contain the solution, it can be regenerated

**Node Pruning Strategy:**

When choosing which node to prune, SMA* selects the leaf node with:
- Highest f-value (least promising)
- Among ties, prefers shallower nodes (lower g-value)

**Performance:**

For puzzles solvable within the memory limit, SMA* performs identically to A*:
- SMA* with Manhattan distance: 11 iterations, max frontier 15
- SMA* with Hamming distance: 19 iterations, max frontier 24

For problems exceeding the memory limit, SMA* trades time for space by re-exploring pruned subtrees.

### 3.4 Heuristic Functions

Heuristic functions are the key to informed search performance. A good heuristic guides the search efficiently toward the goal, while a poor heuristic provides little advantage over uninformed search.

#### 3.4.1 Manhattan Distance

**Definition:**

Manhattan distance (also called taxicab distance or L1 norm) is the sum of the horizontal and vertical distances each tile must travel to reach its goal position. For a tile at position (x₁, y₁) that belongs at position (x₂, y₂), its Manhattan distance is |x₁ - x₂| + |y₁ - y₂|.

**Calculation:**

For the entire puzzle, the Manhattan distance is the sum of individual Manhattan distances for all non-empty tiles:

```
h(n) = Σ (|current_x - goal_x| + |current_y - goal_y|)
```

**Admissibility:**

Manhattan distance is admissible for the 15-puzzle. Each tile must move at least its Manhattan distance to reach the goal position, so the heuristic never overestimates the true cost. This makes it suitable for A* to guarantee optimal solutions.

**Effectiveness:**

Manhattan distance is highly effective for sliding puzzles because:
- It accurately captures the minimum work needed (each tile's minimum moves)
- It provides strong guidance without being too expensive to compute
- It's significantly more informed than simpler heuristics like Hamming distance

**Performance:**

From our test results, Manhattan distance achieves exceptional efficiency:
- A* Manhattan: 14 iterations (99.7% reduction vs uninformed)
- Best-First Manhattan: 11 iterations
- Maximum frontier size: only 15-18 states

#### 3.4.2 Hamming Distance (Misplaced Tiles)

**Definition:**

Hamming distance counts the number of tiles that are not in their correct position (excluding the empty tile). It measures how many tiles need to move, but not how far they need to travel.

**Calculation:**

```
h(n) = count of tiles in wrong positions
```

**Admissibility:**

Hamming distance is admissible because each misplaced tile requires at least one move to reach its goal position. Since we count only the number of misplaced tiles (not the distance they must travel), the heuristic never overestimates.

**Comparison with Manhattan Distance:**

Hamming distance is less informed than Manhattan distance:
- **Hamming**: Counts tiles that need to move (binary: wrong or right)
- **Manhattan**: Measures how far each tile needs to move (quantitative distance)

For example, if a tile is 5 positions away:
- Hamming distance: contributes 1 (just "wrong position")
- Manhattan distance: contributes 5 (actual distance)

**Performance:**

Test results show Hamming distance is less efficient than Manhattan:
- A* Hamming: 24 iterations vs Manhattan's 14 (71% more)
- Best-First Hamming: 20 iterations vs Manhattan's 11 (82% more)
- Maximum frontier: 26-31 states vs Manhattan's 15-18

While still dramatically better than uninformed search, Hamming distance provides weaker guidance than Manhattan distance for sliding puzzles.
