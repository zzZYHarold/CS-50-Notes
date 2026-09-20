from abc import ABC, abstractmethod

class AdversarialGame(ABC):
    """
    双人零和对抗博弈的抽象接口。
    """

    @abstractmethod
    def player(self, state):
        """
        返回当前 state 下轮到哪个玩家行动。
        """
        pass

    @abstractmethod
    def actions(self, state):
        """
        返回当前状态下所有合法动作。
        """
        pass

    @abstractmethod
    def result(self, state, action):
        """
        返回执行 action 后的新状态。
        """
        pass

    @abstractmethod
    def isTerminal(self, state):
        """
        判断当前状态是否为终局。
        """
        pass

    @abstractmethod
    def utility(self, state, player):
        """
        返回终局 state 对 player 的效用。

        例如：
            赢：  1
            平：  0
            输： -1
        """
        pass