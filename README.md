# Heuristic Approach towards the Maximum Diversity Problem

This project implements a **Greedy Randomized Adaptive Search Procedure (GRASP)** in combination with Metaheuristics such as Path Relinking and Tabu Search for solving a combinatorial optimization problem. The framework is designed to allow experimentation with different configurations, parameter tuning strategies, and enhancements to improve algorithmic performance.

## Problem Definition
The Maximum Diversity Problem (MDP) can be formulated as follows:

Given a set N = {1, ..., n} of elements and distances d(i,j) between each pair of elements i,j ∈ N, select a subset S ⊆ N of size m that maximizes the sum of distances between all pairs of selected elements:

maximize   ∑(i,j)∈S d(i,j)  
subject to:  
|S| = m  
S ⊆ N

## Features
- **Constructive Phase**: Generates initial feasible solutions based on a greedy randomized approach.
- **Local Search Phase**: Refines solutions iteratively to improve their objective values.
- **Parameter Tuning**: Includes functionality to calibrate the `alpha` parameter using random sampling for better performance.
- **Execution Profiling**: Captures and reports execution times for performance analysis.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/grasp-optimization.git
    ```

## Usage
#### Running the Main Program
To execute the GRASP implementation on a problem instance:

```bash
python main.py
```
The program will output details for each iteration, including:

- Constructive phase (C) objective value.
- Local search (LS) objective value.
- Best solution found and its objective value.

#### Parameter Tuning
You can tune the alpha parameter using random sampling:
```
# In main.py
num_samples = 1000  # Number of random alpha values to test
iters = 10          # Number of iterations per alpha value
optimal_alpha = tune_alpha_random(inst, iters, num_samples)
print(f"Optimal Alpha Found: {optimal_alpha}")
```

The tuning function evaluates multiple random values of alpha in the range [0, 1] and identifies the one achieving the best average objective value.
##### Output Example
```
Iter 1: C -> 6529.76, LS -> 7551.41
Iter 2: C -> 7127.59, LS -> 7634.70
...
BEST SOLUTION:
Solution: [385, 3, 7, 8, 263, ...]
Objective Value: 7634.70
```

