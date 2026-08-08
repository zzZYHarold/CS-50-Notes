from abc import ABC, abstractmethod

class SearchProblem(ABC):
    """
    搜索问题的抽象接口。

    状态需要是可哈希的，因为搜索算法会把状态放入：
    set 或 dict。
    """

    @abstractmethod
    def getStartState(self):
        """返回初始状态。"""
        pass

    @abstractmethod
    def isGoalState(self, state):
        """判断 state 是否为目标状态。"""
        pass

    @abstractmethod
    def getSuccessors(self, state):
        """
        返回当前状态的所有后继。

        每个后继的格式为：
            (successor, action, step_cost)
        """
        pass