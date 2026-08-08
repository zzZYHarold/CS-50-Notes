from .problem import SearchProblem

def depthFirstSearch(problem: SearchProblem):
    """深度优先搜索 DFS。"""

    start_state = problem.getStartState()
    frontier = [(start_state, [])]
    visited = {start_state}

    while frontier:
        # list.pop() 从末尾取出元素，因此是栈：LIFO
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)

            new_actions = actions + [action]
            frontier.append((successor, new_actions))

    return None

dfs = depthFirstSearch






