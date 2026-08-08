from hashlib import new

from .problem import SearchProblem

_CUTOFF = object()

def depthLimitedSearch(problem: SearchProblem, limit: int):
    """
    深度受限搜索 DLS（Depth-Limited Search）。

    只搜索深度不超过 limit 的节点。

    返回：
        找到目标：动作列表
        因深度限制而停止：_CUTOFF
        状态空间内确实无解：None
    """

    if limit < 0:
        raise ValueError("limit 不能小于 0")

    start_state = problem.getStartState()
    frontier = [(start_state, [], 0)]

    # 记录当前已知到达每个状态的最小深度
    best_depth = {start_state: 0}

    cutoff_occurred = False
    infinity = float("inf")

    while frontier:
        state, actions, depth = frontier.pop()

        # 这个状态后来已经通过更浅的路径到达过，
        # 当前记录已经过时，直接跳过。
        if depth > best_depth.get(state, infinity):
            continue

        if problem.isGoalState(state):
            return actions

        successors = problem.getSuccessors(state)

        # 已经到达本轮允许的最大深度，不能继续展开。
        if depth == limit:
            # 如果下面还有尚未以更浅深度到达的节点，
            # 说明增大深度限制后仍有继续搜索的必要。
            for successor, action, cost in successors:
                next_depth = depth + 1

                if next_depth < best_depth.get(successor, infinity):
                    cutoff_occurred = True
                    break

            continue

        # 没到达最大深度，正常展开子代
        for successor, action, cost in successors:
            next_depth = depth + 1

            if next_depth < best_depth.get(successor, infinity):
                best_depth[successor] = next_depth

                frontier.append((successor, actions + [action], next_depth))

    if cutoff_occurred:
        return _CUTOFF
    return None

def iterativeDeepeningSearch(problem, max_depth=None):
    """
    迭代加深深度优先搜索 IDDFS。

    按照深度限制：
        0, 1, 2, 3, ...

    反复执行深度受限搜索。

    参数：
        problem：
            搜索问题

        max_depth：
            可选的最大搜索深度；
            None 表示不主动设置上限。

    返回：
        找到目标：动作列表
        确认无解或超过 max_depth：None
    """

    limit = 0

    while max_depth is None or limit <= max_depth:
        result = depthLimitedSearch(problem, limit)

        if result is _CUTOFF:
            limit += 1
            continue

        return result

    return None

iddfs = iterativeDeepeningSearch