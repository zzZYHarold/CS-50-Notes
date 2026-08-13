# mcts.py
#Selection -> Expansion -> Simulation -> Backpropagation
"""
Selection
    ↓
while fully_expanded:
    UCT 选择孩子


Expansion
    ↓
从 untried_actions
挑一个动作
生成 MCTSNode


Simulation
    ↓
从新节点开始
随机行动直到 terminal


Backpropagation
    ↓
沿 parent 回去
visits += 1
value_sum += reward
"""

import math
import random

from .game import AdversarialGame


class MCTSNode:
    """
    MCTS 搜索树中的节点。
    """
    def __init__(self, game: AdversarialGame, state, parent=None, action=None):
        self.state = state
        self.parent = parent

        # parent 通过什么动作来到当前节点
        self.action = action

        # 已经扩展出来的孩子
        self.children = []

        # 尚未扩展的动作
        if game.isTerminal(state):
            self.untried_actions = []
        else:
            self.untried_actions = list(game.actions(state))

        # 当前节点被访问多少次
        self.visits = 0

        # 从根节点玩家视角累计得到多少 reward
        self.value_sum = 0.0


    @property
    def mean_value(self):
        """
        当前节点的平均价值 Q。
        """
        if self.visits == 0:
            return 0.0

        return self.value_sum / self.visits


    def fully_expanded(self):
        """
        是否所有合法动作都已经扩展。
        """
        return len(self.untried_actions) == 0


def uctSelectChild(game, node, root_player, exploration=math.sqrt(2)):
    """
    使用 UCT 从 node 的 children 中选择一个孩子。
    """
    current_player = game.player(node.state)

    # 当前是根玩家行动：
    #     希望 root reward 越大越好
    #
    # 当前是对手行动：
    #     希望 root reward 越小越好
    if current_player == root_player:
        sign = 1
    else:
        sign = -1

    log_parent_visits = math.log(node.visits)

    def uct_value(child):
        # 理论上 Expansion + Backprop 后，
        # 已生成的孩子都会至少访问过一次。
        # 这里还是做一下保护。
        if child.visits == 0:
            return float("inf")

        # exploitation
        exploitation = sign * child.mean_value

        # exploration
        exploration_bonus = exploration * math.sqrt(log_parent_visits / child.visits)

        return exploitation + exploration_bonus

    return max(node.children, key=uct_value)


def monteCarloTreeSearch(game: AdversarialGame, state, iterations=1000, exploration=math.sqrt(2), seed=None):
    """
    蒙特卡罗树搜索 MCTS。

    参数：
        game:
            双人零和博弈

        state:
            当前状态

        iterations:
            执行多少轮 MCTS

        exploration:
            UCT 的探索系数 C

        seed:
            随机种子

    返回：
        推荐的 action
    """
    if game.isTerminal(state):
        return None

    rng = random.Random(seed)

    # 当前真正需要做决策的玩家
    root_player = game.player(state)
    root = MCTSNode(game=game, state=state)

    for _ in range(iterations):
        node = root

        # ==========================================
        # 1. Selection
        # ==========================================
        while not game.isTerminal(node.state) and node.fully_expanded() and node.children:
            node = uctSelectChild(game, node, root_player, exploration)

        # ==========================================
        # 2. Expansion
        # ==========================================
        if not game.isTerminal(node.state) and node.untried_actions:
            action = rng.choice(node.untried_actions)
            node.untried_actions.remove(action)

            next_state = game.result(node.state, action)
            child = MCTSNode(game=game, state=next_state, parent=node, action=action)
            node.children.append(child)

            # 后续 simulation 从新节点开始
            node = child

        # ==========================================
        # 3. Simulation / Rollout
        # ==========================================
        rollout_state = node.state

        while not game.isTerminal(rollout_state):
            possible_actions = list(game.actions(rollout_state))
            action = rng.choice(possible_actions)

            rollout_state = game.result(rollout_state, action)

        # 从根节点玩家的角度评价最终结果
        reward = game.utility(rollout_state, root_player)

        # ==========================================
        # 4. Backpropagation
        # ==========================================
        while node is not None:
            node.visits += 1
            node.value_sum += reward
            node = node.parent

    # ==============================================
    # 最终选择
    # ==============================================

    # 最终决策不再使用 UCB 的 exploration bonus。
    #
    # 常见策略：
    # 选择访问次数最多的根节点孩子。
    best_child = max(root.children, key=lambda child: (child.visits, child.mean_value))
    return best_child.action


mcts = monteCarloTreeSearch