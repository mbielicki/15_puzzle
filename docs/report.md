# 15-Puzzle Solver: Algorithm Comparison Report

## 1. Introduction

### 1.1 Problem Overview

The 15-puzzle is a sliding puzzle consisting of a 4×4 grid with 15 numbered tiles and one empty space. The objective is to rearrange the tiles from a scrambled initial configuration to reach the goal state. In the goal state, tiles are ordered sequentially (1-15) with the empty space in the bottom-right corner.

The computational complexity of the 15-puzzle stems from its vast state space. With 16 positions and 16 tiles (including the empty space), there are 16! possible configurations. Mathematical constraints restrict reachability: only half of these configurations are reachable from any given starting position. This yields approximately 10.4 trillion solvable states. This combinatorial explosion renders exhaustive search computationally infeasible for complex puzzle instances.

The 15-puzzle provides an ideal benchmark for comparing search algorithms. Performance can be precisely measured through multiple metrics: solution length, node expansions, execution time, and memory consumption.

### 1.2 Algorithms Implemented

This project implements and compares six search algorithms: three uninformed (BFS, DFS, IDDFS) and three informed (Best-First, A\*, SMA\*). Uninformed algorithms explore the state space without domain-specific knowledge. Informed algorithms utilize heuristic functions to guide the search process. BFS and A\* guarantee optimal solutions. IDDFS achieves optimality with reduced memory requirements. SMA\* operates within strict memory bounds and maintains near-optimal performance under favorable conditions.

### 1.3 Usage

The solver is invoked using `python main.py -<algorithm> <parameter>`. For uninformed algorithms (BFS, DFS, IDDFS), the move order must be specified: LRUD, RDUL, UDLR, DURL, or RAND. For informed algorithms (Best-First, A\*, SMA\*), a heuristic function is selected. Options are 0 (none), 1 (Manhattan distance), or 2 (Hamming distance). The program outputs the solution path, the number of explored states, and execution time.

## 2. Search Algorithms

### 2.1 Breadth-First Search (BFS)

BFS explores the state space level by level using a queue data structure (first-in, first-out). The algorithm guarantees optimal solutions. However, it requires storing all unexplored states in memory. This results in exponential space complexity. The memory requirement renders BFS impractical for complex puzzle instances despite its optimality guarantee.

### 2.2 Depth-First Search (DFS)

DFS explores the state space depth-first using a stack data structure (last-in, first-out). The algorithm exhibits linear space complexity but does not guarantee optimal solutions. A depth limit is required to prevent infinite loops in cyclic state spaces. The implementation does not maintain a visited set. This allows the discovery of alternative solution paths.

### 2.3 Iterative Deepening DFS (IDDFS)

IDDFS combines the space efficiency of DFS with the optimality guarantee of BFS through iterative deepening. The algorithm performs repeated depth-limited searches with progressively increasing depth bounds. This approach expands approximately twice as many nodes as BFS. However, it achieves linear space complexity. IDDFS represents the only algorithm that guarantees optimal solutions while maintaining minimal memory requirements.

### 2.4 Best-First Search

Best-First Search expands nodes based solely on heuristic evaluation. It selects the state with the minimum estimated distance to the goal while disregarding path cost. The algorithm exhibits rapid convergence with effective heuristics but does not guarantee optimal solutions. Memory complexity remains exponential, comparable to BFS.

### 2.5 A* Search

A\* evaluates nodes using the sum of path cost (g) and heuristic estimate (h). The algorithm guarantees optimal solutions provided the heuristic is admissible. An admissible heuristic never overestimates the true cost to goal. Space complexity remains exponential. However, effective heuristics dramatically reduce node expansions compared to uninformed search.

### 2.6 SMA* (Simplified Memory-Bounded A*)

SMA\* extends A\* with a fixed memory bound (10,000 nodes in these experiments). Upon reaching the memory limit, the algorithm prunes the least promising nodes. It retains their evaluation scores for potential regeneration. Space complexity is bounded by the specified limit. With admissible heuristics and sufficient memory, SMA\* maintains optimality. Under restrictive memory constraints or weak heuristics, solution quality may degrade.

### 2.7 Heuristic Functions

Manhattan distance computes the sum of horizontal and vertical displacements for each tile from its current position to its goal position. This heuristic is admissible and particularly effective for sliding puzzles, as it accurately reflects the constrained movement mechanics of the domain.

Hamming distance counts the number of misplaced tiles. While also admissible, this heuristic provides less informative guidance than Manhattan distance, as it assigns uniform cost to all misplaced tiles regardless of their actual distance from goal positions.

## 3. Experimental Results

All algorithms were evaluated on four puzzle instances of varying difficulty. Performance metrics include four measures: solution length, number of expanded nodes, peak frontier size (memory usage), and execution time.

### 3.1 Easy Puzzle (10 moves, 4×4)



**Uninformed Search Results:**

| Algorithm | Order | Moves | Iterations | Max Frontier | Time (s) |
|-----------|-------|-------|-----------|--------------|----------|
| BFS       | UDLR  | 10    | 4,848     | 5,061        | 0.96     |
| BFS       | DULR  | 10    | 4,817     | 5,036        | 1.01     |
| BFS       | LRUD  | 10    | 3,470     | 3,710        | 0.74     |
| BFS       | RDUL  | 10    | 2,618     | 2,824        | 0.59     |
| BFS       | RAND  | 10    | 4,512     | 4,716        | 0.97     |
| DFS       | UDLR  | 12    | 201,089   | 15           | 23.44    |
| DFS       | DULR  | 12    | 203,465   | 15           | 23.14    |
| DFS       | LRUD  | 10    | 95,493    | 15           | 10.89    |
| DFS       | RDUL  | 12    | 7,642     | 15           | 0.85     |
| DFS       | RAND  | 12    | 130,727   | 15           | 14.86    |
| IDDFS     | UDLR  | 10    | 9,814     | 10           | 1.10     |
| IDDFS     | DULR  | 10    | 9,704     | 10           | 1.09     |
| IDDFS     | LRUD  | 10    | 6,890     | 10           | 0.75     |
| IDDFS     | RAND  | 10    | 7,142     | 10           | 0.83     |

BFS consistently discovered the optimal 10-move solution. Node expansions varied by 85% (2,618-4,848) depending on move ordering. DFS exhibited greater variability (27-fold difference) and occasionally produced suboptimal solutions. IDDFS achieved the same 10-move optimal solution as BFS. It expanded twice as many nodes but utilized 500 times less memory.

**Informed Search Results:**

| Algorithm  | Heuristic  | Moves | Iterations | Max Frontier | Time (s) |
|------------|------------|-------|-----------|--------------|----------|
| A*         | h=0        | 10    | 4,848     | 5,061        | 0.90     |
| A*         | Manhattan  | 10    | 14        | 18           | 0.01     |
| A*         | Hamming    | 10    | 24        | 31           | 0.01     |
| Best-First | h=0        | 10    | 4,848     | 5,061        | 0.87     |
| Best-First | Manhattan  | 10    | 11        | 15           | 0.01     |
| Best-First | Hamming    | 10    | 20        | 26           | 0.01     |
| SMA*       | h=0        | 10    | 4,821     | 5,143        | 1.07     |
| SMA*       | Manhattan  | 10    | 11        | 15           | 0.01     |
| SMA*       | Hamming    | 10    | 19        | 24           | 0.01     |

Without a heuristic (h=0), A\* exhibits identical behavior to BFS (4,848 node expansions). Manhattan distance demonstrated superior performance compared to Hamming distance (11-14 versus 19-24 node expansions). SMA\* achieved identical performance to A\*. The memory bound was not reached.

### 3.2 Medium Puzzle (20 moves, 4×4)

| Algorithm  | Heuristic  | Moves | Iterations | Max Frontier | Time (s) |
|------------|------------|-------|-----------|--------------|----------|
| Best-First | Manhattan  | 26    | 108       | 132          | 0.08     |
| Best-First | Hamming    | 30    | 465       | 361          | 0.15     |
| A*         | h=0        | 20    | 2,583,816 | 2,393,992    | 425.63   |
| A*         | Manhattan  | 20    | 828       | 861          | 0.29     |
| A*         | Hamming    | 20    | 6,867     | 7,119        | 1.11     |
| SMA*       | Manhattan  | 20    | 828       | 861          | 0.33     |
| SMA*       | Hamming    | 20    | 6,867     | 7,119        | 1.35     |

Best-First Search achieved rapid execution but produced suboptimal solutions (26-30 moves versus the optimal 20). A\* without a heuristic expanded 2.5 million nodes. This demonstrates the critical importance of effective heuristic guidance. Manhattan distance expanded 8 times fewer nodes than Hamming distance.

### 3.3 Large State Space (20 moves, 5×5)

| Algorithm  | Heuristic | Moves | Iterations | Max Frontier | Time (s) |
|------------|-----------|-------|-----------|--------------|----------|
| Best-First | Manhattan | 26    | 148       | 205          | 0.08     |
| Best-First | Hamming   | 26    | 2,425     | 1,986        | 0.41     |
| A*         | Manhattan | 20    | 29        | 34           | 0.02     |
| A*         | Hamming   | 20    | 39        | 41           | 0.01     |
| SMA*       | Manhattan | 20    | 29        | 34           | 0.02     |
| SMA*       | Hamming   | 20    | 39        | 41           | 0.01     |

This instance had a significantly larger state space (10^24 versus 10^13). Despite this, it required substantially fewer node expansions (29 versus 828 with Manhattan distance). This observation indicates that initial state configuration exerts greater influence on search complexity than state space size.

### 3.4 Hard Puzzle (28 moves, 4×4)

| Algorithm  | Heuristic | Moves | Iterations | Max Frontier | Time (s) |
|------------|-----------|-------|-----------|--------------|----------|
| Best-First | Manhattan | 52    | 1,839     | 1,414        | 0.59     |
| Best-First | Hamming   | 52    | 10,500    | 8,282        | 1.64     |
| A*         | Manhattan | 28    | 15,045    | 14,089       | 5.06     |
| A*         | Hamming   | 28    | 492,185   | 460,553      | 83.12    |
| SMA*       | Manhattan | 28    | 15,045    | 10,000*      | 29.31    |
| SMA*       | Hamming   | 32    | 130,956   | 10,000*      | 692.39   |

*SMA\* capped at 10,000-node limit*

Best-First Search achieved rapid execution (0.59s) at the cost of solution quality (52 moves versus the optimal 28). Manhattan distance enabled optimal solution discovery 33 times faster than Hamming distance. A critical finding emerged: SMA\* with Manhattan distance maintained optimality despite memory constraints. It required 5.8 times longer execution. In contrast, SMA\* with Hamming distance produced a suboptimal solution (32 versus 28 moves).

## 4. Analysis

### 4.1 Algorithm Comparison

| Algorithm  | Optimal     | Space      | Best Iterations | Worst Iterations | Key Strength           | Key Weakness         |
|------------|-------------|------------|-----------------|------------------|------------------------|----------------------|
| BFS        | Yes         | O(b^d)     | 2,618           | 2.5M             | Guaranteed optimal     | Explosive memory     |
| DFS        | No          | O(d)       | 7,642           | 203,465          | Minimal memory         | Suboptimal, variable |
| IDDFS      | Yes         | O(d)       | 6,890           | 9,814            | Optimal + efficient    | 2× iterations       |
| Best-First | No          | O(b^d)     | 11              | 562              | Very fast              | Suboptimal           |
| A*         | Yes         | O(b^d)     | 14              | 15,045           | Optimal + efficient    | High memory          |
| SMA*       | Conditional | O(limit)   | 11              | 130,956          | Bounded memory         | May lose optimality  |

A\* with Manhattan distance reduces node expansions by 99.7% compared to BFS (14 versus 4,848). IDDFS expands twice as many nodes as BFS. However, it reduces memory consumption by a factor of 500. Best-First Search achieves 86% faster execution than A\*. This comes at the cost of producing solutions 86% longer on difficult instances.

### 4.2 Heuristic Effectiveness

| Puzzle      | Manhattan Iters | Hamming Iters | Efficiency Gain |
|-------------|-----------------|---------------|------------------|
| 10-move 4×4 | 14              | 24            | 42%              |
| 20-move 4×4 | 828             | 6,867         | 88%              |
| 20-move 5×5 | 29              | 39            | 26%              |
| 28-move 4×4 | 15,045          | 492,185       | 97%              |

Manhattan distance's superiority increases with problem difficulty (from 42% to 97% efficiency gain). As complexity increases, Hamming distance exhibits exponential degradation (20,000-fold increase in node expansions). Manhattan distance demonstrates more graceful scaling (1,000-fold increase). Under memory constraints, SMA\* with Manhattan distance maintains optimality. In contrast, SMA\* with Hamming distance produces suboptimal solutions.

### 4.3 Key Insights

Memory consumption represents a fundamental algorithmic trade-off. Doubling puzzle difficulty increases BFS memory requirements by a factor of 473 (from 5,000 to 2.4 million stored states). IDDFS offers an explicit space-time trade-off. It doubles node expansions while reducing memory consumption by a factor of 500 compared to BFS. SMA\* demonstrates that admissible heuristics can maintain optimality even under strict memory bounds.

Initial state configuration often dominates state space size in determining search complexity. The 5×5 puzzle instance had a state space 10^11 times larger than the 4×4 instance. Despite this, it required 28 times fewer node expansions due to favorable heuristic alignment. Move ordering significantly impacts uninformed search performance (BFS variance of 85%, DFS variance of 27-fold). In contrast, informed search with effective heuristics exhibits minimal sensitivity to move ordering.

## 5. Conclusions

Heuristic quality represents the dominant factor in search performance. Manhattan distance achieves 97% greater efficiency than Hamming distance on difficult instances. This advantage increases as problem complexity grows. Memory trade-offs are fundamental: BFS and A\* exhibit exponential space complexity. IDDFS doubles node expansions to reduce memory by a factor of 500. SMA\* bounds memory at the potential cost of optimality. Initial state configuration often exerts greater influence than state space size. The 5×5 instance proved 28 times more tractable than the 4×4 instance despite having a state space 10^11 times larger. Under memory constraints, heuristic quality becomes critical. With a 10,000-node limit, SMA\* with Manhattan distance maintained optimality. SMA\* with Hamming distance produced suboptimal solutions.

Algorithm selection recommendations: A\* with Manhattan distance is optimal when memory resources are abundant. IDDFS is preferred under severe memory constraints. SMA\* with Manhattan distance provides near-optimal solutions with bounded memory. Best-First Search with Manhattan distance enables rapid approximate solutions when optimality is not required. Manhattan distance is essential for instances requiring more than 15 moves. SMA\* solution quality degradation indicates insufficient memory allocation or inadequate heuristic function. Uninformed search remains viable only for trivial instances requiring fewer than 10 moves.
