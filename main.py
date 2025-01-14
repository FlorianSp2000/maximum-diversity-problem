from structure import instance, solution
from algorithms import grasp, pathrelinking
import random
import os
import csv
import time
from datetime import datetime
import argparse

def executeInstance(instance_path, elite_set_size=10, max_steps=None, diversify=True, solution_size=100, algorithm='grasp', alpha=-1):
    # path = "instances/MDG-a_2_n500_m50.txt"
    # "instances/MDG-a_1_100_m10.txt" 
    # instances/MDG-a_2_n500_m50.txt
    # inst = instance.readInstance(path)
    start_time = time.time()
    inst = instance.readInstance(instance_path)

    all_solutions = []
    for _ in range(solution_size):
        # print(f"alpha is {alpha}")
        sol = grasp.execute(inst, 10, alpha, algorithm)
        all_solutions.append(sol)

    all_solutions.sort(key=lambda s: s['of'], reverse=True)
    if algorithm == 'grasp':
        best_solution = all_solutions[0]
    elif algorithm == 'pr' or algorithm == 'tabu':
        top_solutions = all_solutions[:elite_set_size]
    
        best_solution = pathrelinking.execute(top_solutions, max_steps=max_steps, diversify=diversify)

    runtime = round(time.time() - start_time, 2)

    metrics = {
        "instance_name": os.path.basename(instance_path),
        "objective_value": round(best_solution['of'], 2),
        "runtime": runtime,
        "best_solution": " ".join(map(str, best_solution['sol'])),
    }
    # sol = grasp.execute(inst, 10, -1)
    # optimal_alpha = grasp.tune_alpha_random(inst, 10, 1000)
    # print(f"Optimal Alpha Found: {optimal_alpha}")

    print("\nBEST SOLUTION:")
    solution.printSolution(best_solution)
    return metrics

def empiricalAnalysis(instances_dir, csv_output_path, elite_set_size=10, max_steps=5, diversify=True, algorithm='grasp'):
    """
    Perform empirical analysis over multiple instances and save results to a CSV file.

    Parameters:
    - instances_dir: Directory containing the instance files.
    - csv_output_path: Path to save the CSV results.
    - elite_set_size: Number of top solutions used for Path Relinking.
    - max_steps: Maximum steps to explore during Path Relinking.
    - diversify: Ensure diversity between solutions.
    """
    # Dynamically find all .txt files in the instances directory
    instance_paths = [
        os.path.join(instances_dir, file)
        for file in os.listdir(instances_dir)
        if file.endswith(".txt")
    ]

    if not instance_paths:
        print(f"No instance files found in directory: {instances_dir}")
        return

    results = []

    for instance_path in instance_paths:
        #extract last number, either 50 out of m50 or 10 out of m10
        instance = instance_path[-6:-4]
        alpha = -1
        if instance == '10':
            alpha = 0.743
        elif instance == '50':
            alpha = 0.114
        
        metrics = executeInstance(instance_path, elite_set_size, max_steps, diversify, algorithm=algorithm, alpha=alpha)
        results.append(metrics)

    # Write results to CSV
    with open(csv_output_path, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["instance_name",  "objective_value", "runtime", "best_solution",])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nEmpirical analysis completed. Results saved to {csv_output_path}")


if __name__ == '__main__':
    # add a argument with argparse that indicates the algorithm grasp verus grasp with path relinking
    parser = argparse.ArgumentParser(description='Empirical Analysis of GRASP with Path Relinking')
    parser.add_argument('--algorithm', type=str, default='grasp', help='Algorithm to use: grasp or pr', choices=['grasp', 'pr', 'tabu'], )
    args = parser.parse_args()
    random.seed(1)
    timestamp = datetime.now().strftime("%M_%H_%d_%m_%Y")

    # Define the instances directory
    instances_dir = "instances"

    # Output CSV file path
    csv_output_path = f"results/empirical_results_{args.algorithm}_{timestamp}.csv"

    # Perform empirical analysis
    empiricalAnalysis(instances_dir, csv_output_path, elite_set_size=20, max_steps=5, diversify=True, algorithm=args.algorithm)


