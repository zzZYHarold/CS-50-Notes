import random
from abc import ABC, abstractmethod


class HillClimbingProblem(ABC):
    """
    爬山问题的抽象接口。
    状态需要是可哈希的（因为部分爬山变种可能会用到 set 去重）。
    """

    @abstractmethod
    def initial_state(self):
        """
        返回（随机的）初始状态。
        """
        pass

    @abstractmethod
    def neighbors(self, state):
        """
        返回 state 的所有邻居状态。
        """
        pass

    @abstractmethod
    def cost(self, state):
        """
        返回 state 的代价（越小越好）。
        """
        pass


class HospitalsProblem(HillClimbingProblem):
    """
    使用：
    problem = HospitalsProblem(
    height=10,
    width=20,
    houses=houses,
    num_hospitals=3
    )

    solution = hill_climb(problem)

    print(solution)
    print(problem.cost(solution))
    """
    def __init__(self, height, width, houses, num_hospitals):
        self.height = height
        self.width = width
        self.houses = houses
        self.num_hospitals = num_hospitals

    def initial_state(self):
        available = [
            (row, col)
            for row in range(self.height)
            for col in range(self.width)
            if (row, col) not in self.houses
        ]

        # 随机放医院
        return frozenset(random.sample(available, self.num_hospitals))

    def neighbors(self, hospitals):
        result = []

        for hospital in hospitals:
            row, col = hospital

            positions = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1)
            ]

            for position in positions:
                row2, col2 = position

                # 越界
                if not (0 <= row2 < self.height and 0 <= col2 < self.width):
                    continue

                # 不能建在房子上
                if position in self.houses:
                    continue

                # 不能和另一家医院重叠
                if position in hospitals:
                    continue

                neighbor = set(hospitals)

                neighbor.remove(hospital)
                neighbor.add(position)

                result.append(frozenset(neighbor))

        return result

    def cost(self, hospitals):
        total = 0

        for house in self.houses:
            # 曼哈顿距离
            distance = min(abs(house[0] - hospital[0]) + abs(house[1] - hospital[1])
                for hospital in hospitals)

            total += distance

        return total