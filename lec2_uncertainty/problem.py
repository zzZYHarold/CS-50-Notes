from abc import ABC, abstractmethod
from typing import Hashable


class HMMProblem(ABC):
    """
    Hidden Markov Model 问题的抽象基类。

    一个具体 HMM 问题需要提供：
    1. 所有可能的隐藏状态 states
    2. 已经观察到的 observation sequence
    3. 初始概率 P(X_1)
    4. 转移概率 P(X_t | X_{t-1})
    5. 发射概率 P(E_t | X_t)
    """

    @property
    @abstractmethod
    def states(self) -> list[Hashable]:
        """所有可能的隐藏状态。"""
        pass

    @property
    @abstractmethod
    def observations(self) -> list[Hashable]:
        """实际观察到的 observation sequence。"""
        pass

    @abstractmethod
    def initial_probability(self, state: Hashable) -> float:
        """
        P(X_1 = state)
        第一时刻处于 state 的概率。
        """
        pass

    @abstractmethod
    def transition_probability(self, previous_state: Hashable, current_state: Hashable) -> float:
        """P(X_t = current_state | X_{t-1} = previous_state)"""
        pass

    @abstractmethod
    def emission_probability(self, state: Hashable, observation: Hashable) -> float:
        """P(E_t = observation | X_t = state)"""
        pass