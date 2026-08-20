# 这一版不考虑“多个最优 neighbor 随机选一个”，同时做了更深层的抽象
from .problem import LocalSearchProblem


def hill_climb(problem: LocalSearchProblem, initial_state):
    current = initial_state

    while True:
        neighbors = list(problem.neighbors(current))

        if not neighbors:
            return current

        neighbor = min(neighbors, key=problem.cost)

        if problem.cost(neighbor) >= problem.cost(current):
            return current

        current = neighbor


def random_restart(problem: LocalSearchProblem, restarts):
    best_state = None

    for _ in range(restarts):
        initial_state = problem.initial_state()

        state = hill_climb(problem, initial_state)

        if (best_state is None or problem.cost(state) < problem.cost(best_state)):
            best_state = state

    return best_state