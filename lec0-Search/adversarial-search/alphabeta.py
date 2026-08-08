from .game import AdversarialGame

#alpha: 沿当前搜索路径，MAX 已经找到的、能够保证得到的最好值。-> 它是 MAX 的下界
#-> MAX 已经有多好的备选方案
#beta:  沿当前搜索路径，MIN 已经找到的、能够保证压到的最好值。
#-> MIN 已经能把 MAX 压得多低


def alphaBetaSearch(game, state):
    """
    当前 state 是 MAX 节点。
    返回 MAX 应该选择的最优动作。
    """
    alpha = float("-inf")
    beta = float("inf")

    best_value = float("-inf")
    best_action = None

    for action in game.actions(state):
        next_state = game.result(state, action)

        # MAX 走完一步，下一层轮到 MIN
        value = minValue(game, next_state, alpha, beta)

        if value > best_value:
            best_value = value
            best_action = action

        alpha = max(alpha, best_value)

    return best_action


def maxValue(game: AdversarialGame, state, alpha, beta):
    """
    当前 state 是 MAX 节点。
    返回这个状态的 Minimax 值。
    """
    if game.isTerminal(state):
        return game.utility(state)

    value = float("-inf")

    for action in game.actions(state):
        next_state = game.result(state, action)
        value = max(value, minValue(game, next_state, alpha, beta))

        # beta cutoff
        if value >= beta:
            return value

        alpha = max(alpha, value)

    return value

def minValue(game, state, alpha, beta):
    """
    当前 state 是 MIN 节点。
    返回这个状态的 Minimax 值。
    """
    if game.isTerminal(state):
        return game.utility(state)

    value = float("inf")

    for action in game.actions(state):
        next_state = game.result(action, state)
        value = min(value, maxValue(game, next_state, alpha, beta))

        # alpha cutoff
        if value <= alpha:
            return value

        beta = min(beta, value)

    return value