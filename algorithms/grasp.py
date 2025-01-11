from constructives import cgrasp
from localsearch import lsbestimp
import time
import random

def execute(inst, iters, alpha):
    best = None
    total_time = 0  # Initialize total time

    for i in range(iters):
        start_time = time.time()  # Start the timer
        print("Iter " + str(i + 1) + ": ", end="")
        sol = cgrasp.construct(inst, alpha)
        print("C -> " + str(round(sol['of'], 2)), end=", ")
        lsbestimp.improve(sol)
        print("LS -> " + str(round(sol['of'], 2)))
        iter_time = time.time() - start_time  # Calculate iteration time
        total_time += iter_time  # Accumulate total time

        if best is None or best['of'] < sol['of']:
            best = sol

    avg_time = total_time / iters  # Calculate average time
    print(f"\nAverage Execution Time per Iteration: {avg_time:.4f} seconds")
    return best

def tune_alpha_random(inst, iters, num_samples):
    results = []
    
    for _ in range(num_samples):
        alpha = random.uniform(0, 1)  # Randomly sample alpha in [0, 1]
        print(f"Testing alpha={alpha:.4f}")
        total_of = 0  # Sum of objective values
        total_time = 0  # Sum of execution times

        for i in range(iters):
            start_time = time.time()  # Start timer
            
            sol = cgrasp.construct(inst, alpha)  # Constructive phase
            lsbestimp.improve(sol)  # Local search
            
            iter_time = time.time() - start_time  # Time taken for iteration
            total_time += iter_time
            total_of += sol['of']  # Accumulate objective value

        avg_of = total_of / iters  # Average objective value
        avg_time = total_time / iters  # Average execution time
        results.append((alpha, avg_of, avg_time))

        print(f"Alpha: {alpha:.2f}, Avg Objective Value: {avg_of:.2f}, Avg Time: {avg_time:.4f} seconds\n")

    # Find the best alpha based on the highest average objective value
    best_alpha, best_avg_of, best_avg_time = max(results, key=lambda x: x[1])

    print(f"\nOptimal Alpha: {best_alpha:.2f}")
    print(f"Best Avg Objective Value: {best_avg_of:.2f}")
    print(f"Avg Time per Iteration for Best Alpha: {best_avg_time:.4f} seconds")
    return best_alpha
