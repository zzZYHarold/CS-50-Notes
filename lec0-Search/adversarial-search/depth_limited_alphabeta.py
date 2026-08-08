from .game import AdversarialGame


def alphaBetaSearch(game: AdversarialGame, state, depth_limit, evaluation):
    if game.isTerminal(state):
        return None

    alpha = float("-inf")
    beta = float("inf")

    best_action = None
    best_value = float("-inf")

    for action in game.actions(state):
        next_state = game.result(state, action)

        value = minValue(game, next_state, depth_limit - 1, alpha, beta, evaluation)

        if value > best_value:
            best_value = value
            best_action = action

        alpha = max(alpha, best_value)

    return best_action


def maxValue(game: AdversarialGame, state, depth, alpha, beta, evaluation):
    if game.isTerminal(state):
        return game.utility(state)

    if depth == 0:
        return evaluation(state)

    value = float("-inf")

    for action in game.actions(state):
        next_state = game.result(state, action)
        value = max(value, minValue(game, next_state, depth - 1, alpha, beta, evaluation))

        if value >= beta:
            return value

        alpha = max(alpha, value)

    return value


def minValue(game: AdversarialGame, state, depth, alpha, beta, evaluation):
    if game.isTerminal(state):
        return game.utility(state)

    if depth == 0:
        return evaluation(state)

    value = float("inf")

    for action in game.actions(state):
        next_state = game.result(state, action)

        value = min(value, minValue(game, next_state, depth - 1, alpha, beta, evaluation))

        if value <= alpha:
            return value

        beta = min(beta, value)

    return value