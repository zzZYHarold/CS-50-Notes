from .game import AdversarialGame


def minimax(game: AdversarialGame, state):
    """
    返回当前玩家在 state 下的最优动作。

    假设：
        - 双人
        - 零和
        - 双方均采用最优策略
    """

    root_player = game.player(state)

    best_action = None
    best_value = float("-inf")

    for action in game.actions(state):
        next_state = game.result(state, action)

        value = minimax_value(game, next_state, root_player)

        if value > best_value:
            best_value = value
            best_action = action

    return best_action


def minimax_value(game, state, root_player):
    """
    返回 state 对 root_player 而言的 Minimax 值。
    """

    # 递归出口：终局
    if game.isTerminal(state):
        return game.utility(state, root_player)

    current_player = game.player(state)

    # 如果现在轮到 root_player：
    # 他希望最大化效用
    if current_player == root_player:
        value = float("-inf")

        for action in game.actions(state):
            next_state = game.result(state, action)

            value = max(value, minimax_value(game, next_state, root_player))

        return value

    # 否则轮到对手：
    # 对手希望让 root_player 的效用最小
    else:
        value = float("inf")

        for action in game.actions(state):
            next_state = game.result(state, action)

            value = min(value, minimax_value(game, next_state, root_player))

        return value