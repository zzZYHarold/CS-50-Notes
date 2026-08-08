from .game import AdversarialGame


def minimax(game: AdversarialGame, state):
    best_action = None
    best_value = float("-inf")

    for action in game.actions(state):
        next_state = game.result(state, action)

        # 根节点是 MAX，
        # MAX 做完一步后自然进入 MIN 层
        value = minValue(game, next_state)

        if value > best_value:
            best_value = value
            best_action = action

    return best_action


def maxValue(game: AdversarialGame, state):
    if game.isTerminal(state):
        return game.utility(state)

    value = float("-inf")

    for action in game.actions(state):
        next_state = game.result(state, action)
        value = max(value, minValue(game, next_state))

    return value


def minValue(game: AdversarialGame, state):
    if game.isTerminal(state):
        return game.utility(state)

    value = float("inf")

    for action in game.actions(state):
        next_state = game.result(state, action)
        value = min(value, maxValue(game, next_state))

    return value


