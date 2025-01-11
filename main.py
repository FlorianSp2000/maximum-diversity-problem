from structure import instance, solution
from algorithms import grasp
import random

def executeInstance():
    path = "instances/MDG-a_2_n500_m50.txt"
    # "instances/MDG-a_1_100_m10.txt" 
    # instances/MDG-a_2_n500_m50.txt
    inst = instance.readInstance(path)
    # sol = grasp.execute(inst, 10, -1)
    optimal_alpha = grasp.tune_alpha_random(inst, 10, 1000)
    print(f"Optimal Alpha Found: {optimal_alpha}")

    # print("\nBEST SOLUTION:")
    # solution.printSolution(sol)

if __name__ == '__main__':
    random.seed(1)
    executeInstance()

