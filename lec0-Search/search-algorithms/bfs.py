from collections import deque
from .problem import SearchProblem

def breadthFirstSearch(problem: SearchProblem):
    """广度优先搜索 BFS。"""

    start_state = problem.getStartState()
    frontier = deque([(start_state, [])])
    visited = {start_state}

    while frontier:
        # popleft() 从最左侧取出最早加入的元素：FIFO
        state, actions = frontier.popleft()

        if problem.isGoalState(state):
            return actions

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)

            new_actions = actions + [action]
            frontier.append((successor, new_actions))

    return None

bfs = breadthFirstSearch