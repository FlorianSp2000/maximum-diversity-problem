from structure import solution
import copy
import time
from concurrent.futures import ThreadPoolExecutor


def execute(solutions, max_steps=None, diversify=True):
    start_time = time.time()
    best = max(solutions, key=lambda s: s['of'])
    n_solutions = len(solutions)

    def process_pair(i, j):
        initial = solutions[i]
        guiding = solutions[j]
        return path_relink(initial, guiding, max_steps=max_steps, diversify=diversify)

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_pair, i, j)
            for i in range(n_solutions)
            for j in range(i + 1, n_solutions)
        ]
        for future in futures:
            candidate = future.result()
            if candidate['of'] > best['of']:
                best = candidate

    print(f"Path Relinking Completed in {round(time.time() - start_time, 2)} seconds.")
    return best


def path_relink(initial, guiding, max_steps=None, diversify=True):
    if diversify:
        similarity = len(initial['sol'] & guiding['sol']) / len(initial['sol'] | guiding['sol'])
        if similarity > 0.5:
            return initial

    current = copy.deepcopy(initial)
    guiding_set = guiding['sol']
    steps = 0
    best = copy.deepcopy(initial)

    to_add = guiding_set - current['sol']
    to_remove = current['sol'] - guiding_set

    while to_add and to_remove and (max_steps is None or steps < max_steps):
        add = max(to_add, key=lambda x: solution.distanceToSol(current, x))  # Greedy addition
        remove = min(to_remove, key=lambda x: solution.distanceToSol(current, x))  # Greedy removal

        solution.removeFromSolution(current, remove)
        solution.addToSolution(current, add)

        if current['of'] > best['of']:
            best = copy.deepcopy(current)

        to_add.remove(add)
        to_remove.remove(remove)
        steps += 1

    return best
