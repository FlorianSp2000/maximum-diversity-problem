from structure import instance, solution
from algorithms import grasp, pathrelinking
import random
import os

def executeInstance(instance_path, elite_set_size=10, max_steps=None, diversify=True, solution_size=100):
    # path = "instances/MDG-a_2_n500_m50.txt"
    # "instances/MDG-a_1_100_m10.txt" 
    # instances/MDG-a_2_n500_m50.txt
    # inst = instance.readInstance(path)
    inst = instance.readInstance(instance_path)

    all_solutions = []
    for _ in range(solution_size):
        sol = grasp.execute(inst, 1, -1)
        all_solutions.append(sol)

    all_solutions.sort(key=lambda s: s['of'], reverse=True)
    top_solutions = all_solutions[:elite_set_size]
    
    best_pr_solution = pathrelinking.execute(top_solutions, max_steps=max_steps, diversify=diversify)

    # sol = grasp.execute(inst, 10, -1)
    # optimal_alpha = grasp.tune_alpha_random(inst, 10, 1000)
    # print(f"Optimal Alpha Found: {optimal_alpha}")

    print("\nBEST SOLUTION:")
    solution.printSolution(best_pr_solution)

if __name__ == '__main__':
    random.seed(1)
    instances_dir = "instances"
    instance_paths = [
        os.path.join(instances_dir, file)
        for file in os.listdir(instances_dir)
        if file.endswith(".txt")
    ]
    executeInstance(instance_paths[0], elite_set_size=20, max_steps=None, diversify=True, solution_size=100)

