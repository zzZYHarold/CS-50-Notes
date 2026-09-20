try:
    from .game import AdversarialGame
except ImportError:  # Allow loading this file directly from its directory.
    from game import AdversarialGame


def minimax(game: AdversarialGame, state):
    root_player = game.player(state)
    best_action = None
    best_value = float("-inf")

    for action in game.actions(state):
        next_state = game.result(state, action)

        # 根节点是 MAX，
        # MAX 做完一步后自然进入 MIN 层
        value = minValue(game, next_state, root_player)

        if value > best_value:
            best_value = value
            best_action = action

    return best_action


def maxValue(game: AdversarialGame, state, root_player):
    if game.isTerminal(state):
        return game.utility(state, root_player)

    value = float("-inf")

    for action in game.actions(state):
        next_state = game.result(state, action)
        value = max(value, minValue(game, next_state, root_player))

    return value


def minValue(game: AdversarialGame, state, root_player):
    if game.isTerminal(state):
        return game.utility(state, root_player)

    value = float("inf")

    for action in game.actions(state):
        next_state = game.result(state, action)
        value = min(value, maxValue(game, next_state, root_player))

    return value


