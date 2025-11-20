# 15-Puzzle Solver: Algorithm Comparison Report

## 1. Introduction
### 1.1 Problem Overview
*Brief description of the 15-puzzle, goal state, and computational complexity*

### 1.2 Algorithms Implemented
*List of all 6 algorithms tested: BFS, DFS, IDDFS, Best-First, A\*, SMA\**

### 1.3 Usage
*Explain how to use main.py: command-line interface, algorithm selection (-b/-a/-s flags), move ordering options, input format (pipe puzzle from file or stdin), example commands*

## 2. Uninformed Search Algorithms
### 2.1 Breadth-First Search (BFS)
*Algorithm description, queue-based approach, optimality guarantee, visited set usage*

### 2.2 Depth-First Search (DFS)
*Algorithm description, stack-based approach, depth limit necessity*
*Include note from docs/notes.md about visited set and depth limit problem*

### 2.3 Iterative Deepening DFS (IDDFS)
*Algorithm description, combines DFS and BFS benefits*
*Include explanation from docs/notes.md about why IDDFS does more iterations than BFS*

### 2.4 Move Ordering Strategies
#### 2.4.1 Standard Orders (LRUD, RDUL, UDLR, DURL)
*Explain how move order affects search path and iteration count*

#### 2.4.2 Random Order (RAND)
*Explain per-node randomization and non-deterministic behavior*

## 3. Informed Search Algorithms
### 3.1 Best-First Search
*Algorithm description, priority queue with heuristic only (greedy), not optimal*

### 3.2 A* Search
*Algorithm description, f(n) = g(n) + h(n), optimality with admissible heuristics*

### 3.3 Simplified Memory-Bounded A* (SMA*)
*Algorithm description, memory-limited variant of A\*, node pruning strategy*

### 3.4 Heuristic Functions
#### 3.4.1 Manhattan Distance
*Definition, admissibility, effectiveness for sliding puzzles*

#### 3.4.2 Hamming Distance (Misplaced Tiles)
*Definition, admissibility, comparison with Manhattan distance*

## 4. Experimental Results
### 4.1 Test Methodology
*Test configurations: Multiple puzzles of varying difficulty*
- *Experiment 1: 4x4 puzzle with 10 moves (experiment_10.txt)*
- *Experiment 2: 4x4 puzzle with 20 moves (experiment_20.txt)*
- *Experiment 3: 5x5 puzzle with 20 moves (experiment_20_5x5.txt)*
- *Experiment 4: 4x4 puzzle with 28 moves (experiment_28.txt)*
*Hardware/software environment, iteration counting approach, max frontier size tracking*

### 4.2 Performance Metrics Explained
*Metrics tracked:*
- *Moves: Solution path length (lower is better; optimal varies by puzzle)*
- *Iterations: Total states examined (indicates computational work)*
- *Max Frontier: Maximum states held in memory simultaneously (space complexity)*
- *Time (s): Execution time in seconds*
- *Status: Search outcome (SUCCESS, NO SOLUTION, INTERRUPTED, EXCEPTION)*

### 4.3 Experiment 1: Easy Puzzle (10 Moves)
#### 4.3.1 Uninformed Search Results
*Present BFS, DFS, IDDFS results from experiment_10.txt*
- *BFS: 2,618-5,061 max frontier (O(b^d) space), all find optimal 10-move solution*
- *DFS: Constant 15 max frontier (O(d) space), 10-12 moves, highly variable iterations (7,642-203,465)*
- *IDDFS: 10 max frontier, optimal 10 moves, 6,890-9,814 iterations*
- *Move order impact: RDUL most efficient for BFS (2,618 iterations), LRUD for IDDFS (6,890 iterations)*

#### 4.3.2 Informed Search Results
*Present Best-First, A\*, SMA\* results from experiment_10.txt*
- *A\* Manhattan: 14 iterations, 18 max frontier - 99.7% reduction vs BFS*
- *A\* Hamming: 24 iterations, 31 max frontier - less informed but still optimal*
- *Best-First: Slightly better iteration counts (11-20) but optimal on easy puzzle*
- *SMA\*: Nearly identical to A\* when memory sufficient (h=0 shows small variance)*
- *A\* h=0: Behaves identically to BFS (4,848 iterations, 5,061 frontier)*

### 4.4 Experiment 2: Medium Puzzle (20 Moves, 4x4)
*Present results from experiment_20.txt*
- *Best-First Manhattan: Fast (0.08s) but suboptimal (26 moves vs optimal 20)*
- *A\* Manhattan: Optimal 20 moves, 828 iterations, 861 max frontier*
- *A\* Hamming: Optimal 20 moves, 6,867 iterations (8.3x more than Manhattan)*
- *A\* h=0 (Uninformed): 2.5M iterations, 2.4M max frontier, 425s - demonstrates heuristic necessity*
- *SMA\* performance: Identical to A\* (828/6,867 iterations), memory limit not reached*

### 4.5 Experiment 3: Large State Space (20 Moves, 5x5)
*Present results from experiment_20_5x5.txt*
- *Counter-intuitive finding: 5x5 puzzle EASIER than 4x4 for informed search*
- *A\* Manhattan: Only 29 iterations vs 828 for 4x4 (96.5% reduction)*
- *A\* Hamming: Only 39 iterations vs 6,867 for 4x4 (99.4% reduction)*
- *Key insight: State space size matters less than puzzle configuration and heuristic quality*
- *Best-First still suboptimal: 26 moves, but very efficient (148 iterations)*

### 4.6 Experiment 4: Hard Puzzle (28 Moves, 4x4)
*Present results from experiment_28.txt - demonstrates SMA\* memory constraints*
#### 4.6.1 Performance at Memory Limits
- *A\* Manhattan: Optimal 28 moves, 15,045 iterations, 14,089 max frontier*
- *SMA\* Manhattan: Optimal 28 moves, 15,045 iterations, but capped at 10,000 frontier (29.31s vs 5.06s)*
- *A\* Hamming: Optimal 28 moves, 492,185 iterations, 460,553 max frontier (exceeds memory limit)*
- *SMA\* Hamming: SUBOPTIMAL 32 moves, 130,956 iterations, 10,000 frontier (memory constraint forced pruning)*

#### 4.6.2 Memory vs Optimality Trade-off
*SMA\* sacrificed optimality (32 vs 28 moves) to maintain 10,000 node memory limit with Hamming heuristic*
*Manhattan heuristic 33x more efficient than Hamming (15,045 vs 492,185 iterations)*
*Best-First: Fastest (0.59s) but highly suboptimal (52 vs 28 moves)*

### 4.7 Heuristic Function Comparison Across All Experiments
*Manhattan Distance consistently superior:*
- *10-move: 14 vs 24 iterations (42% reduction)*
- *20-move: 828 vs 6,867 iterations (88% reduction)*
- *28-move: 15,045 vs 492,185 iterations (97% reduction)*
*Hamming effectiveness decreases as puzzle difficulty increases*

## 5. Analysis and Discussion

### 5.1 Algorithm Performance Summary
*Comparison of all algorithms across optimality, efficiency, and memory usage*
*Table summarizing key characteristics: optimal/suboptimal, space complexity, iteration patterns*

### 5.2 Heuristic Effectiveness
*Manhattan vs Hamming comparison across all difficulty levels*
*Impact of heuristic quality on search efficiency (42% to 97% improvement)*
*Why Manhattan distance is superior for sliding puzzles*

### 5.3 Memory-Space Trade-offs
*BFS vs IDDFS: O(b^d) vs O(d) empirical validation*
*SMA* behavior: optimal when memory sufficient, degrades gracefully when constrained*
*Memory management overhead in SMA* (6× slower despite same iterations)*

### 5.4 Puzzle Configuration Impact
*Counter-intuitive 5×5 result: larger state space but easier to solve*
*State space size vs puzzle difficulty: heuristic quality dominates*
*Move order significance for uninformed search (85% variance), irrelevant for informed search*

## 6. Conclusions

*Summary of key findings from experiments*
*Algorithm recommendations for different scenarios:*
- *Optimal solution with memory available: A* with Manhattan*
- *Memory-constrained optimal: IDDFS*
- *Memory-constrained near-optimal: SMA* with Manhattan*
- *Quick approximate: Best-First with Manhattan*
*Practical implications: importance of heuristic design, memory-optimality trade-offs*
*Future work: larger puzzles, advanced heuristics (pattern databases), adaptive memory limits*
