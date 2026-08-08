# search_algorithms/astar.py

from heapq import heappush, heappop
from itertools import count

from .problem import SearchProblem


def nullHeuristic(state, problem=None):
    """
    恒为 0 的启发式函数。

    当 A* 使用 nullHeuristic 时：
        f(n) = g(n) + 0 = g(n)

    因此 A* 会退化成 UCS。
    """
    return 0

def manhattanHeuristic(state, problem):
    row, column = state
    goal_row, goal_column = problem.goal

    return abs(row - goal_row) + abs(column - goal_column)

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    A* 搜索。

    参数：
        problem:
            搜索问题

        heuristic(state, problem):
            从 state 到目标的剩余代价估计

    返回：
        找到目标：动作列表
        无解：None
    """

    start_state = problem.getStartState()
    insertion_order = count()

    # 优先队列中的元素：
    #
    # (
    #     f,
    #     insertion_number,
    #     g,
    #     state,
    #     actions
    # )
    frontier = []

    start_g = 0
    start_h = heuristic(start_state, problem)
    start_f = start_g + start_h

    heappush(frontier, (start_f, next(insertion_order), start_g, start_state, []))

    # best_cost[state]：
    # 当前已知从起点到 state 的最低实际代价 g。
    best_cost = {start_state: 0}
    infinity = float("inf")

    while frontier:
        f, _, g, state, actions = heappop(frontier)

        # 如果后来已经发现了一条更便宜的路径到达 state，
        # 当前堆元素就是过期记录。
        if g > best_cost.get(state, infinity):
            continue

        # 目标必须在弹出时检查，而不是生成时检查。
        if problem.isGoalState(state):
            return actions

        for successor, action, step_cost in problem.getSuccessors(state):
            if step_cost < 0:
                raise ValueError("A* 不支持负动作代价")

            new_g = g + step_cost

            # 只有发现更便宜的路径时才更新
            if new_g < best_cost.get(successor, infinity):
                best_cost[successor] = new_g

                new_h = heuristic(successor, problem)
                new_f = new_g + new_h

                heappush(frontier, (new_f, next(insertion_order), new_g, successor, actions + [action]))

    return None


astar = aStarSearch