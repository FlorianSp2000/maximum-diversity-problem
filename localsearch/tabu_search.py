
from structure import solution

def tabu_search(sol, iterations=100, tabu_tenure=10):
    tabu_list = set()
    instance = sol['instance']

    for it in range(iterations):
        sel, ofVarSel, unsel, ofVarUnsel = selectInterchange(sol, tabu_list)
        if sel != -1 and unsel != -1 and ofVarSel < ofVarUnsel:
            solution.removeFromSolution(sol, sel, ofVarSel)
            solution.addToSolution(sol, unsel, ofVarUnsel)
            tabu_list.add((sel, unsel))
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop()

def selectInterchange(sol, tabu_list):
    n = sol['instance']['n']
    sel = -1
    bestSel = 0x3f3f3f
    unsel = -1
    bestUnsel = 0

    for v in sol['sol']:
        d = solution.distanceToSol(sol, v)
        if d < bestSel:
            bestSel = d
            sel = v

    for v in range(n):
        if not solution.contains(sol, v):
            d = solution.distanceToSol(sol, v, without=sel)
            if d > bestUnsel and (sel, v) not in tabu_list:
                bestUnsel = d
                unsel = v

    return sel, round(bestSel, 2), unsel, round(bestUnsel, 2)
