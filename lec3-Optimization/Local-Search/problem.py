import math
import random
from abc import ABC, abstractmethod


class LocalSearchProblem(ABC):
    """
    爬山问题的抽象接口。
    状态需要是可哈希的（因为部分爬山变种可能会用到 set 去重）。
    """

    @abstractmethod
    def initial_state(self):
        """
        生成一个（随机的）初始状态
        """
        pass

    @abstractmethod
    def neighbors(self, state):
        """
        生成 state 的所有邻居
        """
        pass

    @abstractmethod
    def cost(self, state):
        """
        返回 state 的代价
        越小越好
        """
        pass

    def random_neighbor(self, state):
        """
        随机选择一个邻居。

        默认实现：先生成所有邻居，再随机选一个。
        某些问题可以重写这个方法，提高效率。
        """
        candidates = list(self.neighbors(state))

        if not candidates:
            return None

        return random.choice(candidates)


class HospitalsProblem(LocalSearchProblem):
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
    
    
class TravelingSalesmanProblem(LocalSearchProblem):

    def __init__(self, cities):
        """
        cities:

        {
            "A": (x1, y1),
            "B": (x2, y2),
            ...
        }
        """

        if len(cities) < 2:
            raise ValueError("TSP needs at least two cities")

        self.cities = dict(cities)

    def initial_state(self):
        """
        随机生成一条城市访问顺序
        """

        route = list(self.cities.keys())
        random.shuffle(route)

        return tuple(route)

    def neighbors(self, state):
        """
        枚举所有：
        交换任意两个城市后得到的路线
        """

        n = len(state)

        for i in range(n - 1):
            for j in range(i + 1, n):
                route = list(state)
                route[i], route[j] = (route[j], route[i])
                yield tuple(route)

    def random_neighbor(self, state):
        """
        模拟退火只需要随机一个邻居，
        没必要先生成 O(n^2) 个邻居。
        """

        i, j = random.sample(range(len(state)), 2)
        route = list(state)
        route[i], route[j] = (route[j], route[i])

        return tuple(route)

    def cost(self, state):
        """
        计算整条旅行路线长度，
        包括最后一个城市返回第一个城市。
        """

        total = 0.0
        n = len(state)
        for i in range(n):
            city_a = state[i]

            # 最后一个自动连回 state[0]
            city_b = state[(i + 1) % n]

            x1, y1 = self.cities[city_a]
            x2, y2 = self.cities[city_b]

            distance = math.hypot(x2 - x1, y2 - y1)
            total += distance

        return total