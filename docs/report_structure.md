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
### 5.1 Optimality vs Efficiency Trade-offs
*Optimal algorithms: BFS, IDDFS, A\* (with admissible heuristics), SMA\* (when memory sufficient)*
*Suboptimal algorithms:*
- *DFS: Depth-limited, finds any solution (10-12 moves for 10-move puzzle)*
- *Best-First: Greedy, sacrifices optimality for speed (26-52 moves vs optimal 20-28)*
- *SMA\*: Can become suboptimal under memory pressure (32 vs 28 moves with Hamming)*

### 5.2 Memory Usage Considerations
*Space complexity validation from experiments:*
- *BFS: O(b^d) confirmed - 2,824 to 5,061 max frontier (10-move puzzle)*
- *DFS: O(d) confirmed - constant 15 max frontier (depth limit)*
- *IDDFS: O(d) confirmed - max frontier of 10 (solution depth)*
- *A\* Manhattan: Dramatic reduction - 18 to 861 max frontier vs BFS's thousands*
- *SMA\*: Enforced 10,000 node limit demonstrated in 28-move puzzle*

### 5.3 Critical Findings
#### 5.3.1 Heuristic Quality Dominates Difficulty
*Manhattan distance 33x more efficient than Hamming on hard puzzles*
*Strong heuristic overcomes large state spaces: 5x5 puzzle easier than 4x4 for A\* Manhattan*
*Uninformed A\* (h=0) performs identically to BFS - validates heuristic necessity*

#### 5.3.2 SMA\* Memory-Optimality Trade-off
*When memory sufficient: SMA\* identical to A\* (verified in 10-move and 20-move puzzles)*
*When memory constrained: SMA\* sacrifices optimality (32 vs 28 moves, Hamming heuristic)*
*Memory management overhead: 6x slower despite same iterations (29.31s vs 5.06s, Manhattan)*

#### 5.3.3 Best-First Performance Paradox
*Fewest iterations on hard puzzles (1,839 vs A\*'s 15,045) but suboptimal (52 vs 28 moves)*
*Fastest execution time (0.59s) but sacrifices solution quality*
*Greedy nature: explores most promising paths first but misses optimal solution*

#### 5.3.4 IDDFS Iteration Overhead
*IDDFS does more work than BFS (6,890 vs 2,618 iterations) due to repeated exploration*
*Trade-off justified: O(d) space vs BFS's O(b^d) space*
*Reference explanation from docs/notes.md about re-exploration cost*

### 5.4 Iteration Count Patterns
*A\* Manhattan: Most efficient informed search (14 to 15,045 iterations by difficulty)*
*DFS variability: 7,642 to 203,465 iterations depending on move order*
*Best-First: Consistently low iterations but poor solution quality*
*Hamming heuristic: Degrades rapidly with puzzle difficulty (24 to 492,185 iterations)*

### 5.5 Execution Time Analysis
*Strong correlation between iterations and time, but exceptions:*
- *SMA\* memory management: 6x slower than A\* with same iteration count*
- *DFS outliers: 23 seconds for 203,465 iterations vs A\* Hamming 83 seconds for 492,185*
- *Best-First speed advantage: 0.59s for suboptimal solution vs 5-83s for optimal*

## 6. Conclusions
### 6.1 Algorithm Recommendations by Scenario
#### 6.1.1 Optimal Solution Required, Memory Available
*A\* with Manhattan distance: Consistently best performance (14-15,045 iterations)*
*Provides optimality guarantee with minimal computational work*

#### 6.1.2 Memory Constrained Environment
*SMA\* with Manhattan distance: Optimal when memory sufficient, graceful degradation when constrained*
*IDDFS: Guaranteed O(d) space, always optimal, but high iteration count*
*Trade-off: SMA\* faster but may sacrifice optimality; IDDFS slower but always optimal*

#### 6.1.3 Quick Approximate Solution Acceptable
*Best-First with Manhattan distance: Fastest execution (0.08-0.59s)*
*Solution quality varies (optimal on easy puzzles, 2x suboptimal on hard puzzles)*

#### 6.1.4 No Heuristic Available
*BFS: Optimal and reliable, but O(b^d) memory*
*IDDFS: Optimal with O(d) memory, iteration overhead acceptable for memory-constrained systems*
*Avoid DFS: Highly variable, suboptimal, deep searches expensive*

### 6.2 Key Insights
#### 6.2.1 Heuristic Quality is Critical
*Manhattan distance 97% more efficient than Hamming on hard puzzles*
*Uninformed A\* (h=0) identical to BFS - heuristic necessity validated*
*Strong heuristic overcomes state space size: 5x5 easier than 4x4*

#### 6.2.2 Memory-Optimality Trade-off
*SMA\* demonstrates practical implementation of memory-bounded search*
*Can sacrifice optimality to maintain memory bounds (32 vs 28 moves)*
*Memory management overhead significant: 6x slower despite same iteration count*

#### 6.2.3 Move Order Impact on Uninformed Search
*BFS: RDUL most efficient (2,618 iterations), UDLR least efficient (4,848 iterations)*
*DFS: Extreme variability (7,642 to 203,465 iterations) - move order critical*
*Informed search: Move order irrelevant (heuristic dominates exploration)*

#### 6.2.4 Space Complexity Validation
*Empirical results confirm theoretical predictions:*
- *BFS: O(b^d) - thousands of states in frontier*
- *DFS/IDDFS: O(d) - frontier limited to depth (10-15 states)*
- *A\* Manhattan: Dramatically reduced frontier (18-861 vs BFS's thousands)*

### 6.3 Future Work
*Test on larger puzzles (5x5 harder configurations) to further stress SMA\* memory limits*
*Explore advanced heuristics: pattern databases, disjoint pattern databases*
*Investigate adaptive memory limits for SMA\* based on available system memory*
*Benchmark additional move ordering strategies for uninformed search optimization*
