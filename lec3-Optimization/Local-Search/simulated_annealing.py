import math
import random
from .problem import LocalSearchProblem

def simulated_annealing(problem: LocalSearchProblem, max_steps = 10000, initial_temperature = 100.0,
                        cooling_rate = 0.995, initial_state = None):

    if initial_state is None:
        current = problem.initial_state()
    else:
        current = initial_state

    for t in range(max_steps):
        # 1. 当前温度 Tt = T0 * alpha^t
        temperature = (initial_temperature * cooling_rate ** t)
        if temperature < 1e-12:
            break

        # 2. 随机选择一个邻居
        neighbor = problem.random_neighbor(current)
        if neighbor is None:
            break

        # 3. 计算 cost
        current_cost = problem.cost(current)
        neighbor_cost = problem.cost(neighbor)

        # 4. neighbor 比 current 好多少
        #
        # 这是最小化问题：
        # neighbor cost 更低 -> delta > 0
        delta = current_cost - neighbor_cost

        # 5. 更好：一定接受
        if delta > 0:
            current = neighbor

        # 6. 不更好：按概率接受
        else:
            probability = math.exp(delta / temperature)
            if random.random() < probability:
                current = neighbor

    return current
