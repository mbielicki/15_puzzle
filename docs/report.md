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

## 4. Experimental Results

### 4.1 Test Methodology

To comprehensively evaluate the search algorithms, we conducted experiments on four puzzles of varying difficulty levels. Each experiment used different puzzle configurations to test algorithm performance under different conditions.

**Experiment 1: Easy Puzzle (10 moves)**

The first test puzzle is a 4×4 configuration solvable in 10 moves, shown in Figure 1.

```
Figure 1: Initial state of 10-move puzzle
┌────┬────┬────┬────┐
│  1 │  2 │  3 │  4 │
├────┼────┼────┼────┤
│  6 │  9 │  7 │  8 │
├────┼────┼────┼────┤
│ 13 │  5 │ 10 │ 11 │
├────┼────┼────┼────┤
│ 14 │    │ 15 │ 12 │
└────┴────┴────┴────┘
```

- Purpose: Baseline comparison of all algorithms on a simple puzzle
- Algorithms tested: All 6 algorithms with various configurations (23 total tests)
- Depth limit: 15 moves
- Optimal solution: 10 moves

**Experiment 2: Medium Puzzle (20 moves, 4×4)**

The second test puzzle requires 20 moves for the optimal solution (Figure 2).

```
Figure 2: Initial state of 20-move puzzle (4×4)
┌────┬────┬────┬────┐
│  1 │  2 │  3 │  4 │
├────┼────┼────┼────┤
│  5 │ 11 │  8 │  6 │
├────┼────┼────┼────┤
│    │ 10 │ 14 │  7 │
├────┼────┼────┼────┤
│  9 │ 13 │ 15 │ 12 │
└────┴────┴────┴────┘
```

- Purpose: Test informed search performance on moderate difficulty
- Algorithms tested: Best-First, A*, SMA* with different heuristics
- Depth limit: 30 moves
- Optimal solution: 20 moves

**Experiment 3: Large State Space (20 moves, 5×5)**

The third puzzle uses a larger 5×5 grid to evaluate scalability (Figure 3).

```
Figure 3: Initial state of 20-move puzzle (5×5)
┌────┬────┬────┬────┬────┐
│  6 │  1 │  3 │  9 │  4 │
├────┼────┼────┼────┼────┤
│  2 │ 12 │  7 │  8 │  5 │
├────┼────┼────┼────┼────┤
│ 16 │ 11 │ 13 │ 14 │ 10 │
├────┼────┼────┼────┼────┤
│ 21 │ 17 │ 19 │    │ 15 │
├────┼────┼────┼────┼────┤
│ 22 │ 23 │ 18 │ 24 │ 20 │
└────┴────┴────┴────┴────┘
```

- Purpose: Evaluate scalability to larger state spaces
- Algorithms tested: Best-First, A*, SMA* with Manhattan and Hamming heuristics
- Depth limit: 60 moves
- Optimal solution: 20 moves

**Experiment 4: Hard Puzzle (28 moves, 4×4)**

The final test puzzle is the most challenging, requiring 28 moves (Figure 4).

```
Figure 4: Initial state of 28-move puzzle
┌────┬────┬────┬────┐
│    │  1 │  2 │  3 │
├────┼────┼────┼────┤
│  5 │  7 │  4 │ 15 │
├────┼────┼────┼────┤
│  9 │ 10 │  8 │ 11 │
├────┼────┼────┼────┤
│ 13 │ 14 │  6 │ 12 │
└────┴────┴────┴────┘
```

- Purpose: Test memory constraints and heuristic effectiveness on difficult puzzles
- Algorithms tested: Best-First, A*, SMA* with different heuristics
- Depth limit: 60 moves
- Optimal solution: 28 moves
- Key objective: Demonstrate SMA* memory limits and optimality trade-offs

**Testing Environment:**

- Platform: Windows with PowerShell
- Python Version: 3.13
- Memory limit for SMA*: 10,000 nodes
- Iteration counting: Total states examined during search
- Frontier tracking: Maximum number of states held in memory simultaneously

### 4.2 Performance Metrics Explained

Each experiment tracked five key metrics to evaluate algorithm performance:

**Moves:** Solution path length measured as the number of tile moves from initial state to goal state. Lower is better. The optimal solution length varies by puzzle difficulty (10, 20, or 28 moves in our experiments). This metric indicates solution quality.

**Iterations:** Total number of states examined during the search process. Each iteration involves popping a state from the frontier, checking if it's the goal, and generating successor states. This metric indicates computational work and algorithmic efficiency.

**Max Frontier:** Maximum number of states held in memory simultaneously during the search. This represents peak space complexity and validates theoretical O(b^d) vs O(d) predictions. Critical for comparing memory efficiency across algorithms.

**Time (s):** Execution time in seconds from search start to solution discovery. Influenced by iterations, data structure operations, and heuristic computation cost. Useful for practical performance comparison.

**Status:** Search outcome indicating SUCCESS (solution found), NO SOLUTION (search exhausted), INTERRUPTED (user cancelled), or EXCEPTION (error occurred). All experiments in this report show SUCCESS status.

### 4.3 Experiment 1: Easy Puzzle (10 Moves)

The first experiment used the 4×4 puzzle shown in Figure 1, testing all 23 algorithm configurations to establish baseline performance characteristics.

#### 4.3.1 Uninformed Search Results

Table 1 presents the performance of uninformed search algorithms on the 10-move puzzle.

**Table 1: Uninformed Search Performance on 10-Move Puzzle**

| Algorithm    | Order | Moves | Iterations | Max Frontier | Time (s) | Status  |
|--------------|-------|-------|-----------|--------------|----------|---------|
| BFS          | UDLR  | 10    | 4,848     | 5,061        | 0.96     | SUCCESS |
| BFS          | DULR  | 10    | 4,817     | 5,036        | 1.01     | SUCCESS |
| BFS          | LRUD  | 10    | 3,470     | 3,710        | 0.74     | SUCCESS |
| BFS          | RDUL  | 10    | 2,618     | 2,824        | 0.59     | SUCCESS |
| BFS          | RAND  | 10    | 4,512     | 4,716        | 0.97     | SUCCESS |
| DFS          | UDLR  | 12    | 201,089   | 15           | 23.44    | SUCCESS |
| DFS          | DULR  | 12    | 203,465   | 15           | 23.14    | SUCCESS |
| DFS          | LRUD  | 10    | 95,493    | 15           | 10.89    | SUCCESS |
| DFS          | RDUL  | 12    | 7,642     | 15           | 0.85     | SUCCESS |
| DFS          | RAND  | 12    | 130,727   | 15           | 14.86    | SUCCESS |
| IDDFS        | UDLR  | 10    | 9,814     | 10           | 1.10     | SUCCESS |
| IDDFS        | DULR  | 10    | 9,704     | 10           | 1.09     | SUCCESS |
| IDDFS        | LRUD  | 10    | 6,890     | 10           | 0.75     | SUCCESS |
| IDDFS        | RAND  | 10    | 7,142     | 10           | 0.83     | SUCCESS |

**Observations from Table 1:**

- **BFS**: All move orderings found the optimal 10-move solution. Iterations ranged from 2,618 (RDUL) to 4,848 (UDLR), showing 85% variation. Max frontier ranged from 2,824 to 5,061 states, confirming O(b^d) space complexity.
- **DFS**: Solution lengths varied from 10-12 moves (occasionally suboptimal). Iterations extremely variable: 7,642 (RDUL) to 203,465 (DULR), demonstrating 27× variance. Max frontier constant at 15 states (depth limit), validating O(d) space complexity.
- **IDDFS**: All orderings found optimal 10-move solution. Iterations ranged from 6,890 (LRUD) to 9,814 (UDLR). Max frontier constant at 10 states (solution depth), confirming O(d) space complexity. IDDFS performed 2× more iterations than BFS due to re-exploration (6,890 vs 3,470 for LRUD) but used 500× less memory.

#### 4.3.2 Informed Search Results

Table 2 shows the performance of informed search algorithms with different heuristics.

**Table 2: Informed Search Performance on 10-Move Puzzle**

| Algorithm    | Heuristic        | Moves | Iterations | Max Frontier | Time (s) | Status  |
|--------------|------------------|-------|-----------|--------------|----------|---------|
| A*           | h=0 (None)       | 10    | 4,848     | 5,061        | 0.90     | SUCCESS |
| A*           | Manhattan        | 10    | 14        | 18           | 0.01     | SUCCESS |
| A*           | Hamming          | 10    | 24        | 31           | 0.01     | SUCCESS |
| Best-First   | h=0 (None)       | 10    | 4,848     | 5,061        | 0.87     | SUCCESS |
| Best-First   | Manhattan        | 10    | 11        | 15           | 0.01     | SUCCESS |
| Best-First   | Hamming          | 10    | 20        | 26           | 0.01     | SUCCESS |
| SMA*         | h=0 (None)       | 10    | 4,821     | 5,143        | 1.07     | SUCCESS |
| SMA*         | Manhattan        | 10    | 11        | 15           | 0.01     | SUCCESS |
| SMA*         | Hamming          | 10    | 19        | 24           | 0.01     | SUCCESS |

**Observations from Table 2:**

- **A* with Manhattan**: 14 iterations, 18 max frontier (99.7% reduction vs BFS, 99.6% reduction in memory)
- **A* with Hamming**: 24 iterations, 31 max frontier (71% more iterations than Manhattan, still 99.5% better than uninformed BFS)
- **A* with h=0**: 4,848 iterations, identical to BFS, validating that A* reduces to BFS when h=0
- **Best-First**: Manhattan variant achieved optimal solution (10 moves) with only 11 iterations, fewer than A* due to greedy nature
- **SMA***: Performance nearly identical to A* (memory limit of 10,000 nodes never triggered on this easy puzzle)
- **Heuristic comparison**: Manhattan distance provides superior guidance (14 iterations vs 24 for Hamming, a 42% reduction)

### 4.4 Experiment 2: Medium Puzzle (20 Moves, 4×4)

This experiment tested informed search algorithms on the puzzle shown in Figure 2, focusing on heuristic effectiveness and the comparison between optimal and greedy approaches.

**Table 3: Informed Search Performance on 20-Move Puzzle (4×4)**

| Algorithm    | Heuristic        | Moves | Iterations | Max Frontier | Time (s) | Status  |
|--------------|------------------|-------|-----------|--------------|----------|---------|  
| Best-First   | Manhattan        | 26    | 108       | 132          | 0.08     | SUCCESS |
| Best-First   | Hamming          | 30    | 465       | 361          | 0.15     | SUCCESS |
| A*           | h=0 (None)       | 20    | 2,583,816 | 2,393,992    | 425.63   | SUCCESS |
| A*           | Manhattan        | 20    | 828       | 861          | 0.29     | SUCCESS |
| A*           | Hamming          | 20    | 6,867     | 7,119        | 1.11     | SUCCESS |
| SMA*         | Manhattan        | 20    | 828       | 861          | 0.33     | SUCCESS |
| SMA*         | Hamming          | 20    | 6,867     | 7,119        | 1.35     | SUCCESS |

**Observations from Table 3:**

- **Best-First Search**: Fast but suboptimal. Manhattan variant found 26-move solution (30% longer than optimal) in only 0.08s. Hamming variant found 30-move solution (50% longer) with 4.3× more iterations than Manhattan.
- **A* with Manhattan**: Optimal 20-move solution with 828 iterations and 861 max frontier. Highly efficient with strong heuristic.
- **A* with Hamming**: Still optimal (20 moves) but required 8.3× more iterations than Manhattan (6,867 vs 828). Weaker heuristic necessitates more exploration.
- **A* with h=0**: Optimal but extremely expensive - 2,583,816 iterations taking 425.63s (equivalent to BFS). Demonstrates absolute necessity of heuristics, performing 3,119× more iterations than A* Manhattan.
- **SMA* performance**: Identical to A* for both heuristics (memory limit of 10,000 nodes not reached as both used ~7,000 states).
- **Heuristic quality dominance**: Manhattan 8.3× better than Hamming, 3,119× better than h=0

### 4.5 Experiment 3: Large State Space (20 Moves, 5×5)

This experiment evaluated algorithm scalability using the 5×5 puzzle shown in Figure 3, revealing a counter-intuitive finding about state space size and search difficulty.

**Table 4: Informed Search Performance on 20-Move Puzzle (5×5)**

| Algorithm    | Heuristic        | Moves | Iterations | Max Frontier | Time (s) | Status  |
|--------------|------------------|-------|-----------|--------------|----------|---------|  
| Best-First   | Manhattan        | 26    | 148       | 205          | 0.08     | SUCCESS |
| Best-First   | Hamming          | 26    | 2,425     | 1,986        | 0.41     | SUCCESS |
| A*           | Manhattan        | 20    | 29        | 34           | 0.02     | SUCCESS |
| A*           | Hamming          | 20    | 39        | 41           | 0.01     | SUCCESS |
| SMA*         | Manhattan        | 20    | 29        | 34           | 0.02     | SUCCESS |
| SMA*         | Hamming          | 20    | 39        | 41           | 0.01     | SUCCESS |

**Observations from Table 4:**

**Counter-Intuitive Discovery:** Despite having a much larger state space (25!/2 vs 16!/2 possible configurations), the 5×5 puzzle was dramatically easier for informed search than the 4×4 20-move puzzle (Table 3).

- **A* with Manhattan**: Only 29 iterations compared to 828 for the 4×4 puzzle (96.5% reduction). Extremely efficient despite larger state space.
- **A* with Hamming**: Only 39 iterations compared to 6,867 for the 4×4 puzzle (99.4% reduction). Even the weaker Hamming heuristic becomes highly effective.
- **Best-First**: Suboptimal solutions (26 moves vs optimal 20) consistent with 4×4 results. Hamming variant required 16× more iterations than Manhattan (2,425 vs 148).
- **SMA* performance**: Perfect match with A* for both heuristics (memory not constrained, frontiers of 34 and 41 well below 10,000 limit).
- **Puzzle configuration significance**: The 5×5 puzzle proved easier because tile positions aligned favorably with Manhattan distance, creating a clearer gradient toward the goal. This demonstrates that with effective heuristics, the quality of guidance matters far more than the size of the search space.

### 4.6 Experiment 4: Hard Puzzle (28 Moves, 4×4)

The final experiment used the challenging puzzle shown in Figure 4, specifically designed to stress-test memory limits and demonstrate the optimality-memory trade-off in SMA*.

**Table 5: Informed Search Performance on 28-Move Puzzle**

| Algorithm    | Heuristic  | Moves | Iterations | Max Frontier | Time (s) | Status  |
|--------------|------------|-------|-----------|--------------|----------|---------|  
| Best-First   | Manhattan  | 52    | 1,839     | 1,414        | 0.59     | SUCCESS |
| Best-First   | Hamming    | 52    | 10,500    | 8,282        | 1.64     | SUCCESS |
| A*           | Manhattan  | 28    | 15,045    | 14,089       | 5.06     | SUCCESS |
| A*           | Hamming    | 28    | 492,185   | 460,553      | 83.12    | SUCCESS |
| SMA*         | Manhattan  | 28    | 15,045    | 10,000*      | 29.31    | SUCCESS |
| SMA*         | Hamming    | 32    | 130,956   | 10,000*      | 692.39   | SUCCESS |

*Note: SMA* max frontier capped at memory limit of 10,000 nodes*

**Observations from Table 5:**

#### 4.6.1 Performance at Memory Limits

- **Best-First Search**: Highly suboptimal - found 52-move solutions (86% longer than optimal 28 moves). Manhattan variant fastest (0.59s) but demonstrates greedy failure. Hamming required 5.7× more iterations than Manhattan.

- **A* with Manhattan**: Optimal 28-move solution with 15,045 iterations. Frontier of 14,089 stayed just below SMA* memory limit.

- **A* with Hamming**: Still optimal but massively more expensive - 33× more iterations (492,185 vs 15,045) and 32× larger frontier (460,553 vs 14,089) compared to Manhattan. Frontier far exceeds SMA* memory limit.

- **SMA* with Manhattan**: Found optimal 28-move solution with same iteration count as A* (15,045). Memory limit reached (capped at 10,000), but optimal path preserved. However, 5.8× slower than A* (29.31s vs 5.06s) due to memory management overhead.

- **SMA* with Hamming**: **SUBOPTIMAL** - found 32-move solution instead of optimal 28 (14% longer). Memory constraint forced pruning of the optimal path. Demonstrated 73% reduction in iterations vs A* (130,956 vs 492,185) and 98% reduction in memory (10,000 vs 460,553), but sacrificed optimality.

#### 4.6.2 Memory vs Optimality Trade-off

This experiment provides clear evidence of SMA*'s fundamental trade-off between memory and optimality:

**When Memory is Sufficient (Manhattan heuristic):**

- SMA* finds optimal solution like A*
- Same iteration count (15,045)
- Slower due to memory management overhead (5.8× slower)
- Memory limit reached but optimal path preserved

**When Memory is Insufficient (Hamming heuristic):**

- SMA* sacrifices optimality to maintain memory bounds
- Suboptimal solution: 32 moves vs optimal 28 (14% longer)
- Pruned the optimal path due to weaker heuristic guidance
- Demonstrates graceful degradation under memory pressure

**Heuristic Quality Critical for SMA*:**

- Strong heuristic (Manhattan): Keeps frontier compact, enables optimality within memory limit
- Weak heuristic (Hamming): Frontier explodes, forces suboptimal pruning
- Manhattan 33× more efficient than Hamming for this puzzle

### 4.7 Heuristic Function Comparison Across All Experiments

Analyzing heuristic performance across all difficulty levels reveals consistent patterns:

**Manhattan Distance Superiority:**

| Puzzle Difficulty | Manhattan Iterations | Hamming Iterations | Reduction |
|-------------------|---------------------|-------------------|-----------|
| 10-move (4×4)     | 14                  | 24                | 42%       |
| 20-move (4×4)     | 828                 | 6,867             | 88%       |
| 20-move (5×5)     | 29                  | 39                | 26%       |
| 28-move (4×4)     | 15,045              | 492,185           | 97%       |

**Key Observations:**

1. **Manhattan advantage grows with difficulty:** 42% reduction on easy puzzles → 97% on hard puzzles
2. **Hamming degrades exponentially:** From 24 iterations (easy) to 492,185 (hard) - a 20,000× increase
3. **Manhattan scales linearly:** From 14 iterations (easy) to 15,045 (hard) - a 1,000× increase
4. **5×5 anomaly:** Both heuristics extremely effective due to favorable configuration

**Why Manhattan Outperforms Hamming:**

- **Manhattan:** Captures distance information (how far each tile must move)
- **Hamming:** Binary information only (tile right or wrong)
- **Sliding puzzles favor Manhattan:** Distance matters more than mere displacement
- **Hamming misses guidance:** Two tiles out of place by 1 vs 5 positions appear identical

**Practical Implications:**

- Always use Manhattan distance for sliding puzzles when possible
- Hamming acceptable for easy puzzles but catastrophic for hard ones
- On 28-move puzzle: Manhattan takes 5 seconds, Hamming takes 83 seconds (16× slower)
- SMA* with Hamming loses optimality; with Manhattan stays optimal

## 5. Analysis and Discussion

### 5.1 Algorithm Performance Summary

Table 6 summarizes the key characteristics of all six algorithms across optimality, efficiency, and memory usage dimensions.

**Table 6: Algorithm Comparison Summary**

| Algorithm | Optimal | Space Complexity | Best Case Iterations | Worst Case Iterations | Memory Efficient | Strengths | Weaknesses |
|-----------|---------|------------------|---------------------|----------------------|------------------|-----------|------------|
| BFS | Yes | O(b^d) | 2,618 (10-move) | 2.5M (20-move) | No | Guaranteed optimal, simple | Explosive memory |
| DFS | No | O(d) | 7,642 (10-move) | 203,465 (10-move) | Yes | Minimal memory | Suboptimal, highly variable |
| IDDFS | Yes | O(d) | 6,890 (10-move) | 9,814 (10-move) | Yes | Optimal + memory efficient | Redundant re-exploration |
| Best-First | No | O(b^d) | 11 (10-move) | 562 (28-move) | No | Very fast | Suboptimal, greedy mistakes |
| A* | Yes | O(b^d) | 14 (10-move) | 15,045 (28-move) | No | Optimal + efficient | High memory |
| SMA* | Conditional | O(memory limit) | 11 (10-move) | 130,956 (28-move suboptimal) | Yes | Bounded memory | May lose optimality |

**Performance Patterns:**

- **Uninformed vs Informed:** Manhattan-guided A* achieves 99.7% reduction in iterations compared to BFS (14 vs 4,848)
- **Memory vs Optimality Trade-off:** IDDFS sacrifices time (2× more iterations than BFS) for 500× memory reduction while maintaining optimality
- **SMA* Adaptability:** Matches A* when memory sufficient, degrades gracefully when constrained
- **Best-First Risk:** 86% faster than A* on 28-move puzzle (0.59s vs 5.06s) but 86% worse solution quality (52 vs 28 moves)

### 5.2 Heuristic Effectiveness

The choice of heuristic function profoundly impacts informed search performance, with effects that amplify as puzzle difficulty increases.

**Manhattan Distance Characteristics:**

Manhattan distance proved consistently superior across all experiments. It provides fine-grained guidance by measuring the exact minimum distance each tile must travel. For the 15-puzzle, this captures the essential structure of the problem: tiles must slide specific distances along orthogonal paths.

The efficiency gains were dramatic:
- Easy puzzles (10 moves): 42% fewer iterations than Hamming
- Medium puzzles (20 moves): 88% fewer iterations than Hamming  
- Hard puzzles (28 moves): 97% fewer iterations than Hamming

This escalating advantage occurs because Manhattan distance provides increasingly valuable guidance as the search tree deepens. On the 28-move puzzle, Manhattan examined 15,045 states while Hamming examined 492,185 states - a 33-fold difference.

**Hamming Distance Limitations:**

Hamming distance counts misplaced tiles without measuring displacement magnitude. A tile one position away contributes identically to a tile five positions away, making the heuristic less informative for sliding puzzles.

The consequences grow severe with difficulty:
- 10-move puzzle: 24 iterations (acceptable)
- 20-move puzzle: 6,867 iterations (8× worse than Manhattan)
- 28-move puzzle: 492,185 iterations (33× worse than Manhattan)

**Impact on SMA*:**

Heuristic quality becomes critical when memory is constrained. On the 28-move puzzle:
- **SMA* with Manhattan:** Optimal 28-move solution within 10,000-node memory limit
- **SMA* with Hamming:** Suboptimal 32-move solution, forced to prune optimal path

This demonstrates that weak heuristics can cause SMA* to sacrifice solution quality, even when a strong heuristic would maintain optimality within the same memory bounds.

### 5.3 Memory-Space Trade-offs

The experimental results validate theoretical space complexity predictions and reveal practical trade-offs between memory usage and search efficiency.

**BFS Memory Explosion:**

BFS exhibits O(b^d) space complexity as predicted. The 10-move puzzle required a maximum frontier of 5,061 states, while the 20-move puzzle (with h=0) ballooned to 2,393,992 states - a 473-fold increase for only doubling the solution depth. This exponential growth makes BFS impractical for deep solutions despite its optimality guarantee.

**IDDFS Memory Efficiency:**

IDDFS achieves O(d) space complexity by storing only the current search path. On the 10-move puzzle, IDDFS maintained a maximum frontier of just 10 states compared to BFS's 5,061 - a 500-fold reduction. The cost is computational redundancy: IDDFS performed 6,890 iterations versus BFS's 3,470 (2× more work), but this is a favorable trade-off when memory is constrained.

**SMA* Behavior Under Memory Pressure:**

SMA* demonstrates two distinct operating regimes:

*When memory is sufficient:* SMA* behaves identically to A*. On the 20-move puzzle with Manhattan distance, both algorithms performed exactly 828 iterations with an 861-node frontier - well below the 10,000-node limit. However, SMA* incurred 14% overhead (0.33s vs 0.29s) due to memory management bookkeeping.

*When memory is constrained:* SMA* begins pruning nodes when the frontier reaches its limit. On the 28-move puzzle with Hamming distance, A* required 460,553 frontier nodes while SMA* was capped at 10,000. This forced SMA* to prune aggressively, ultimately yielding a suboptimal 32-move solution instead of the optimal 28 moves.

Interestingly, on the 28-move puzzle with Manhattan distance, SMA* achieved optimality despite reaching the 10,000-node limit, taking 29.31 seconds compared to A*'s 5.06 seconds - a 5.8× slowdown caused by repeated node regeneration. This demonstrates that SMA* can maintain optimality even under memory pressure if the heuristic is strong enough to keep the frontier compact.

### 5.4 Puzzle Configuration Impact

Counter-intuitively, state space size does not directly correlate with puzzle difficulty when informed search is used.

**The 5×5 Puzzle Anomaly:**

The 5×5 puzzle has a vastly larger state space than the 4×4 puzzle (approximately 10^24 vs 10^13 reachable states). Despite this, the 5×5 20-move puzzle proved dramatically easier than the 4×4 20-move puzzle:

- 4×4 puzzle: 828 iterations with Manhattan distance
- 5×5 puzzle: 29 iterations with Manhattan distance (96.5% reduction)

This 28-fold improvement occurred because the 5×5 puzzle configuration aligned favorably with the Manhattan distance heuristic. The initial state had tiles closer to their goal positions on average, allowing the heuristic to provide exceptionally strong guidance toward the solution.

**Move Order Significance:**

For uninformed search, move ordering profoundly affects performance. On the 10-move puzzle:
- BFS RDUL: 2,618 iterations (best)
- BFS UDLR: 4,848 iterations (worst)
- Variance: 85% between best and worst

DFS showed even greater sensitivity, with iteration counts varying 27-fold (7,642 to 203,465) based solely on move order.

In contrast, informed search with good heuristics exhibits minimal sensitivity to move ordering. A* with Manhattan distance consistently found solutions efficiently regardless of the move exploration sequence, as the heuristic-driven priority queue naturally guides the search toward optimal paths.

**Implications:**

- State space size matters far less than puzzle configuration and heuristic alignment
- Uninformed search requires careful move ordering tuning for each puzzle
- Informed search with strong heuristics eliminates move ordering concerns
- Puzzle difficulty for informed search depends on how well the heuristic captures the problem structure

## 6. Conclusions

This comprehensive experimental evaluation of six search algorithms on the 15-puzzle demonstrates fundamental trade-offs between optimality, memory efficiency, and computational work.

**Summary of Key Findings:**

The experiments revealed that algorithm selection depends critically on the problem constraints:

1. **Heuristic quality dominates performance:** Manhattan distance reduced iterations by 42% to 97% compared to Hamming distance, with the advantage growing as puzzle difficulty increased. On the hardest puzzle tested, Manhattan was 33× more efficient.

2. **Memory-optimality trade-offs are unavoidable:** BFS guarantees optimality but requires exponential memory (5,061 to 2.4 million frontier nodes). IDDFS achieves 500× memory reduction while maintaining optimality by accepting 2× redundant computation. SMA* provides bounded memory with conditional optimality.

3. **State space size misleads:** The 5×5 puzzle with 10^11 times more states proved 28× easier than a 4×4 puzzle when using informed search, demonstrating that heuristic alignment matters more than theoretical state space size.

4. **Memory pressure amplifies heuristic importance:** SMA* with Manhattan distance maintained optimality under 10,000-node memory constraint, while SMA* with Hamming distance produced 14% suboptimal solutions under identical constraints.

**Algorithm Recommendations:**

Based on experimental evidence, we recommend the following algorithm selections for different scenarios:

*Scenario 1 - Optimal solution with ample memory:* Use **A\* with Manhattan distance**. This combination provides optimal solutions with minimal computational work (14 to 15,045 iterations across all test cases). Example: 20-move puzzle solved in 0.29 seconds with 828 iterations.

*Scenario 2 - Optimal solution with severe memory constraints:* Use **IDDFS**. When memory is extremely limited and optimality cannot be sacrificed, IDDFS guarantees optimal solutions with O(d) space complexity. Accept 2× iteration overhead as the cost of memory efficiency. Example: 10-move puzzle using 10 frontier nodes vs BFS's 5,061.

*Scenario 3 - Optimal solution with moderate memory constraints:* Use **SMA\* with Manhattan distance**. When memory is limited but not severely so, SMA* can maintain optimality if given sufficient nodes (typically 10,000+) and paired with a strong heuristic. Monitor solution quality to detect memory-induced degradation. Example: 28-move puzzle optimal in 29.31 seconds with 10,000-node limit.

*Scenario 4 - Quick approximate solution:* Use **Best-First with Manhattan distance**. When optimality is less important than speed, Best-First finds near-optimal solutions extremely quickly. Example: 28-move puzzle solved in 0.59 seconds (86% faster than A*) with a 52-move solution (86% longer than optimal).

**Practical Implications:**

For sliding puzzle applications:
- Always prefer Manhattan distance over Hamming distance unless computation cost is prohibitive
- Monitor SMA* solution quality; degradation indicates insufficient memory or weak heuristic
- For web/mobile applications with memory limits, use SMA* with generous node limits (10,000+)
- For offline solvers with ample memory, A* with Manhattan distance is the clear choice
- Uninformed search (BFS/IDDFS) is viable only for puzzles solvable in ≤15 moves

**Future Work:**

Several directions could extend this research:

1. **Pattern Database Heuristics:** Implement pattern databases that precompute exact solution costs for tile subsets, providing perfect heuristics for those subsets and potentially achieving even greater efficiency than Manhattan distance.

2. **Adaptive Memory Management:** Develop SMA* variants that dynamically adjust memory limits based on available system resources and solution progress, maximizing memory utilization without risking system instability.

3. **Larger Puzzles:** Extend experiments to 5×5 and 6×6 puzzles with deeper solutions (40+ moves) to evaluate algorithm scalability and identify performance breaking points.

4. **Parallel Search:** Investigate parallel implementations of A* and SMA* to leverage multi-core processors, potentially achieving significant speedups for hard puzzles.

5. **Learned Heuristics:** Explore neural network-based heuristics trained on large puzzle datasets to potentially discover heuristics superior to Manhattan distance for specific puzzle classes.

This work establishes a foundation for algorithm selection in sliding puzzle applications and demonstrates the critical importance of heuristic design and memory management in achieving practical search performance.
