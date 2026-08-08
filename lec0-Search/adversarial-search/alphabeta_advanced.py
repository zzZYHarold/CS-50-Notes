from .game import AdversarialGame


def alphaBetaSearch(game: AdversarialGame, state):
    """
    使用 Alpha-Beta 剪枝的 Minimax。

    返回当前玩家的最优动作。
    """
    root_player = game.player(state)

    alpha = float("-inf")
    beta = float("inf")

    best_action = None
    best_value = float("-inf")

    for action in game.actions(state):
        next_state = game.result(state, action)

        value = alphaBetaValue(game, next_state, root_player, alpha, beta)

        if value > best_value:
            best_value = value
            best_action = action

        alpha = max(alpha, best_value)

    return best_action


def alphaBetaValue(game, state, root_player, alpha, beta):
    """
    返回 state 的 Minimax 值，同时进行 Alpha-Beta 剪枝。
    """
    # 终局
    if game.isTerminal(state):
        return game.utility(state, root_player)

    current_player = game.player(state)

    # ---------- MAX ----------
    if current_player == root_player:
        value = float("-inf")

        for action in game.actions(state):
            next_state = game.result(state, action)

            value = max(value, alphaBetaValue(game, next_state, root_player, alpha, beta))

            # MAX 当前能够保证的最好结果
            alpha = max(alpha, value)

            # 剪枝
            if alpha >= beta:
                break

        return value

    # ---------- MIN ----------
    else:
        value = float("inf")

        for action in game.actions(state):
            next_state = game.result(state, action)

            value = min(value, alphaBetaValue(game, next_state, root_player, alpha, beta))

            # MIN 当前能够保证把 MAX 压到多低
            beta = min(beta, value)

            # 剪枝
            if alpha >= beta:
                break

        return value


alphabeta = alphaBetaSearch