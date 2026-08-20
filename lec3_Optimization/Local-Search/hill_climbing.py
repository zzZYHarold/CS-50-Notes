import random
from .problem import LocalSearchProblem


def hill_climb(problem: LocalSearchProblem):
    """
    随机爬山算法（Random Hill Climbing）。
    在当前状态的邻居中，选择代价最小的一个作为下一步，若多个邻居并列最优则随机选取。
    当邻居代价均不低于当前状态时（即陷入局部最优或平坦区域），算法终止。

    该算法不保证找到全局最优，且对初始状态敏感。

    Args:
       initial_state: 任意可哈希或不可哈希的对象，表示搜索的起始状态。
       neighbors (callable): 接收一个状态，返回该状态的所有邻居状态的可迭代对象
                             （例如 list、tuple 或生成器）。
       cost (callable): 接收一个状态，返回一个数值（int 或 float），
                        代表该状态的代价，**越小越好**。

    Returns:
       找到的局部最优状态（代价无法通过单步邻居改善）。

    Note:
       - 若当前状态没有任何邻居（`neighbors(current)` 为空），则直接返回当前状态。
       - 当存在多个代价相同且为最小的邻居时，通过 `random.choice` 随机选择一个，
         这使得算法具有随机性，多次运行可能得到不同结果。
       - 时间复杂度为 O(N) 每步，其中 N 为邻居数量（由 `neighbors` 返回的个数决定）。
    """
    current = problem.initial_state()

    while True:
        neighbors = list(problem.neighbors(current))

        if not neighbors:
            return current

        # 计算每个邻居的 cost
        costs = [(problem.cost(state), state) for state in neighbors]

        # 最优邻居的 cost
        best_cost = min(cost for cost, _ in costs)

        # 可能有多个同样好的邻居
        best_neighbors = [state for cost, state in costs if cost == best_cost]

        # 找不到更好的邻居：到达局部最优
        if best_cost >= problem.cost(current):
            return current

        # 移动到随机一个最优邻居
        current = random.choice(best_neighbors)


def random_restart(problem: LocalSearchProblem, restarts):
    """
    随机重启爬山算法（Random Restart Hill Climbing）。
    多次从随机初始状态运行基础爬山算法，记录所有运行结果中代价最小的状态，
    以降低陷入局部最优的风险。

    该函数会执行 `restarts` 次独立的爬山搜索，每次搜索的起始状态由 `problem.initial_state()`
    提供（通常该函数内部包含随机性），最终返回所有搜索结果中的最优状态。

    Args:
        problem: 一个对象，必须包含以下方法或属性：
                 - initial_state(): 返回一个起始状态（通常随机生成）
                 - neighbors(state): 返回状态的所有邻居
                 - cost(state): 返回状态的代价（越小越好）
                 该对象也可以是一个元组 (initial_state, neighbors, cost)，
                 但更推荐使用统一接口的对象（如 LocalSearchProblem 的子类）。
        restarts (int): 重启次数（即运行基础爬山算法的总次数）。
                        必须为正整数，否则函数可能无法产生有效结果。

    Returns:
        最优状态（即所有运行中找到的代价最小的状态对象）。
        如果 `restarts` 为 0，则返回 `None`（因为从未运行任何搜索）。

    Note:
        - 时间复杂度约为 O(restarts * 单次爬山时间)。
        - 由于每次爬山都从不同的随机初始点开始，结果通常优于单次爬山。
        - 该函数假设 `problem.cost` 返回的代价越低越好，这与 `hill_climb` 函数的设计一致。
        - 初始状态生成务必包含随机性，否则多次重启将毫无意义。
    """
    best_state = None
    best_cost = float("inf")

    for _ in range(restarts):
        state = hill_climb(problem)
        cost = problem.cost(state)

        if cost < best_cost:
            best_state = state
            best_cost = cost

    return best_state

