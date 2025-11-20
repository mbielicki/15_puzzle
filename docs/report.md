# 15-Puzzle Solver: Algorithm Comparison Report

## 1. Introduction

### 1.1 Problem Overview

The 15-puzzle is a sliding puzzle consisting of a 4×4 grid with 15 numbered tiles and one empty space. The goal is to rearrange the tiles from a scrambled initial configuration to reach the goal state where tiles are ordered sequentially (1-15) with the empty space in the bottom-right corner.

The 15-puzzle is computationally challenging due to its large state space. With 16 positions and 16 different tiles (including the empty space), there are 16! possible configurations, though only half of these are reachable from any given starting position due to parity constraints. This results in approximately 10.4 trillion solvable states, making exhaustive search impractical for deep solutions.

The puzzle serves as an excellent benchmark for comparing different search algorithms, as it provides a well-defined problem with measurable metrics including solution optimality, iteration count, execution time, and memory usage.

### 1.2 Algorithms Implemented

This project compares six search algorithms: three uninformed (BFS, DFS, IDDFS) and three informed (Best-First, A\*, SMA\*). Uninformed algorithms explore systematically without domain knowledge, while informed algorithms use heuristic functions to guide exploration. BFS and A\* guarantee optimal solutions, IDDFS optimizes memory usage while maintaining optimality, and SMA\* provides memory-bounded search with conditional optimality.

### 1.3 Usage

The solver is invoked via `python main.py -<algorithm> <parameter>`. Uninformed algorithms (BFS, DFS, IDDFS) take a move ordering parameter (LRUD, RDUL, UDLR, DURL, or RAND). Informed algorithms (Best-First, A\*, SMA\*) take a heuristic identifier: 0 (none), 1 (Manhattan distance), or 2 (Hamming distance). The program outputs the solution path, iteration count, and execution time.

## 2. Search Algorithms

### 2.1 Breadth-First Search (BFS)

BFS explores states level-by-level using a FIFO queue. It guarantees optimal solutions and completeness but requires O(b^d) space, storing all frontier nodes in memory. This makes it impractical for deep solutions despite its optimality guarantee.

### 2.2 Depth-First Search (DFS)

DFS follows paths deeply before backtracking using a LIFO stack. It achieves O(d) space complexity (much better than BFS) but doesn't guarantee optimal solutions. Requires depth limiting to ensure termination. Our implementation avoids visited sets to prevent missing solutions reachable via shorter paths.

### 2.3 Iterative Deepening DFS (IDDFS)

IDDFS combines DFS's O(d) space efficiency with BFS's optimality guarantee by performing depth-limited searches with increasing depth limits. It performs about 2× more iterations than BFS due to re-exploring shallow states, but this redundancy is worthwhile for memory-constrained scenarios. IDDFS is the only algorithm offering both optimality and linear space complexity.

### 2.4 Best-First Search

Best-First Search greedily selects states with lowest heuristic value h(n), ignoring path cost. It's fast with good heuristics but doesn't guarantee optimal solutions. Space complexity is O(b^d).

### 2.5 A* Search

A\* uses evaluation function f(n) = g(n) + h(n), combining actual path cost g(n) with heuristic estimate h(n). It guarantees optimal solutions when the heuristic is admissible (never overestimates). Space complexity is O(b^d). With good heuristics, A\* dramatically outperforms uninformed search.

### 2.6 SMA* (Simplified Memory-Bounded A*)

SMA\* is A\* with bounded memory (10,000 nodes in our tests). When the frontier reaches the limit, it prunes the worst (highest f-value) leaf nodes, storing f-values in parents for potential regeneration. Space complexity is O(memory limit). Maintains optimality with strong heuristics but may yield suboptimal solutions with weak heuristics under memory pressure.

### 2.7 Heuristic Functions

**Manhattan Distance:** Sum of horizontal and vertical distances each tile must travel to reach its goal position. Admissible (never overestimates) and highly effective for sliding puzzles.

**Hamming Distance:** Count of misplaced tiles. Admissible but less informed than Manhattan—treats all misplaced tiles equally regardless of how far they are from their goal positions.

## 3. Experimental Results

We tested all algorithms on four puzzles of varying difficulty. Metrics tracked: solution length (moves), states examined (iterations), peak memory (max frontier), and execution time.

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

BFS achieved optimal solutions with 85% iteration variance (2,618-4,848) based on move ordering. DFS showed extreme variance (27×) with occasional suboptimal solutions. IDDFS matched BFS optimality with 2× more iterations but 500× less memory.

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

With h=0, A\* behaves identically to BFS (4,848 iterations). Manhattan dramatically outperformed Hamming (11-14 vs 19-24 iterations). SMA\* matched A\* performance as memory limit wasn't reached.

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

Best-First was fast but suboptimal (26-30 vs 20 moves). A\* with h=0 required 2.5M iterations, demonstrating heuristic importance. Manhattan used 8× fewer iterations than Hamming.

### 3.3 Large State Space (20 moves, 5×5)

| Algorithm  | Heuristic | Moves | Iterations | Max Frontier | Time (s) |
|------------|-----------|-------|-----------|--------------|----------|
| Best-First | Manhattan | 26    | 148       | 205          | 0.08     |
| Best-First | Hamming   | 26    | 2,425     | 1,986        | 0.41     |
| A*         | Manhattan | 20    | 29        | 34           | 0.02     |
| A*         | Hamming   | 20    | 39        | 41           | 0.01     |
| SMA*       | Manhattan | 20    | 29        | 34           | 0.02     |
| SMA*       | Hamming   | 20    | 39        | 41           | 0.01     |

Despite vastly larger state space (10^24 vs 10^13), this puzzle required far fewer iterations (29 vs 828 with Manhattan). Puzzle configuration matters more than state space size.

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

Best-First was fast (0.59s) but highly suboptimal (52 vs 28 moves). Manhattan achieved optimality 33× faster than Hamming. **Key finding:** SMA\* with Manhattan maintained optimality despite memory limits (5.8× slower), while Hamming yielded suboptimal solution (32 vs 28 moves).

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

Manhattan-guided A\* achieves 99.7% reduction over BFS (14 vs 4,848 iterations). IDDFS trades 2× iterations for 500× memory reduction. Best-First runs 86% faster than A\* but produces 86% worse solutions on hard puzzles.

### 4.2 Heuristic Effectiveness

| Puzzle      | Manhattan Iters | Hamming Iters | Efficiency Gain |
|-------------|-----------------|---------------|------------------|
| 10-move 4×4 | 14              | 24            | 42%              |
| 20-move 4×4 | 828             | 6,867         | 88%              |
| 20-move 5×5 | 29              | 39            | 26%              |
| 28-move 4×4 | 15,045          | 492,185       | 97%              |

Manhattan's advantage scales with difficulty (42% to 97%). Hamming degrades exponentially (20,000× growth) vs Manhattan's 1,000× growth. Under memory constraints, SMA\* with Manhattan maintained optimality while Hamming yielded suboptimal solutions.

### 4.3 Key Insights

**Memory Trade-offs:** BFS requires 473× more memory when depth doubles (5K→2.4M frontier). IDDFS achieves 500× reduction vs BFS with 2× iteration cost. SMA\* maintains optimality with strong heuristics despite memory limits.

**Configuration Matters:** 5×5 puzzle (10^24 states) proved 28× easier than 4×4 (10^13 states) due to favorable heuristic alignment. Move ordering causes 85% variance for BFS, 27× for DFS. Informed search eliminates this sensitivity.

## 5. Conclusions

Heuristic quality dominates all other factors. Manhattan distance achieves 97% efficiency gains over Hamming on hard puzzles, and this gap widens with difficulty. Memory-optimality trade-offs are fundamental: BFS/A\* demand exponential memory, IDDFS accepts 2× iterations for 500× memory reduction, SMA\* offers bounded memory with conditional optimality. Puzzle configuration trumps state space size—the 5×5 puzzle proved 28× easier than 4×4 despite being 10^11 times larger. Memory pressure amplifies heuristic importance: under 10K-node limits, SMA\* with Manhattan maintained optimality while Hamming yielded suboptimal solutions.

**Algorithm Selection:** Use A\*+Manhattan for optimal solutions with ample memory, IDDFS for severe memory constraints, SMA\*+Manhattan for bounded memory with near-optimal solutions, Best-First+Manhattan for fast approximations. Always use Manhattan for puzzles >15 moves. Monitor SMA\* solution quality as degradation signals insufficient memory or weak heuristics. Uninformed search is viable only for puzzles <10 moves.
