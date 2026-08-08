# search_algorithms/ucs.py

from heapq import heappush, heappop
from itertools import count

from .problem import SearchProblem


def uniformCostSearch(problem: SearchProblem):
    """一致代价搜索 UCS。"""

    start_state = problem.getStartState()

    insertion_order = count()
    frontier = []

    # 元素格式：
    # (累计代价, 入队编号, 当前状态, 动作序列)
    heappush(frontier, (0, next(insertion_order), start_state, []))

    best_cost = {start_state: 0}
    infinity = float("inf")

    while frontier:
        cost, _, state, actions = heappop(frontier)

        # 已经有更便宜的路径到达该状态
        if cost > best_cost.get(state, infinity):
            continue

        if problem.isGoalState(state):
            return actions

        for successor, action, step_cost in problem.getSuccessors(state):
            if step_cost < 0:
                raise ValueError("UCS 不支持负动作代价")

            new_cost = cost + step_cost

            if new_cost < best_cost.get(successor, infinity):
                best_cost[successor] = new_cost

                heappush(frontier, (new_cost, next(insertion_order), successor, actions + [action]))
    return None


ucs = uniformCostSearch