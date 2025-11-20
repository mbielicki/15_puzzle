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
*Test configuration: 10-move puzzle, depth limit 15, 23 algorithm configurations*
*Hardware/software environment, iteration counting approach*

### 4.2 Performance Metrics
*Metrics tracked: iterations, execution time, solution length, success/failure*

### 4.3 Uninformed Search Comparison
*Present results from docs/experiment_10.txt for BFS, DFS, IDDFS*
*Compare different move orders, highlight RAND variability*

### 4.4 Informed Search Comparison
*Present results from docs/experiment_10.txt for Best-First, A\*, SMA\**
*Show dramatic efficiency gains over uninformed search*

### 4.5 Heuristic Function Comparison
*Compare Manhattan vs Hamming distance performance*
*Show iteration counts and time differences from docs/experiment_10.txt*

### 4.6 Move Order Impact Analysis
*Analyze how LRUD, RDUL, UDLR, DURL affect uninformed algorithms*
*Show RAND order variation across runs*

## 5. Analysis and Discussion
### 5.1 Optimality vs Efficiency Trade-offs
*Which algorithms guarantee optimal solutions, which sacrifice optimality for speed*

### 5.2 Memory Usage Considerations
*BFS vs IDDFS memory trade-offs, SMA\* memory bounds*
*Reference O(d) vs O(b^d) space complexity from docs/notes.md*

### 5.3 Iteration Count Analysis
*Why A\* Manhattan is most efficient (14 iterations)*
*Why IDDFS does more work than BFS (6,890 vs 2,618 iterations)*
*Reference explanation from docs/notes.md*

### 5.4 Execution Time Patterns
*Correlation between iterations and time, outliers (DFS with deep searches)*

## 6. Conclusions
### 6.1 Algorithm Recommendations
*Best algorithm for different scenarios: optimal solution needed, memory constrained, etc.*

### 6.2 Lessons Learned
*Key insights about search algorithms, heuristics, implementation challenges*
