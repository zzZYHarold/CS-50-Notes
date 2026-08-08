# search_algorithms/greedy.py

from heapq import heappush, heappop
from itertools import count

from .problem import SearchProblem


def greedyBestFirstSearch(problem: SearchProblem, heuristic):
    """
    贪婪最佳优先搜索 Greedy Best-First Search。

    参数：
        problem:
            搜索问题

        heuristic(state, problem):
            启发式函数，用于估计 state 到目标的剩余代价

    返回：
        找到目标：动作列表
        无解：None
    """

    start_state = problem.getStartState()

    # 当两个节点的启发式值相同时，
    # 用递增编号避免 heapq 比较 state。
    insertion_order = count()

    # 优先队列中的元素：
    #
    # (
    #     heuristic_value,
    #     insertion_number,
    #     state,
    #     actions
    # )
    frontier = []
    heappush(frontier, (heuristic(start_state, problem), next(insertion_order), start_state, []))

    # 已经发现过的状态
    visited = {start_state}

    while frontier:
        _, _, state, actions = heappop(frontier)

        if problem.isGoalState(state):
            return actions

        for successor, action, _ in problem.getSuccessors(state):
            if successor in visited:
                continue

            visited.add(successor)
            heappush(frontier, (heuristic(successor, problem), next(insertion_order), successor, actions + [action]))

    return None


gbfs = greedyBestFirstSearch