from collections import deque


""" 构建层次:
    Version 0
    Naive Backtracking
    ≈ schedule0.py
    │
    ├── Select variable：按顺序
    ├── Select value：按顺序
    └── Consistency check
              │
              ↓
    Version 1
    Backtracking + Inference
    │
    ├── REVISE
    ├── AC-3
    └── MAC
              │
              ↓
    Version 2
    Backtracking + Inference + Heuristics
    │
    ├── MRV
    ├── Degree
    ├── LCV
    └── MAC / AC-3
              │
              ↓
          Final Solver
"""


class CSP:
    # ---------- CSP definition ----------
    def __init__(self, variables, domains, neighbors, constraint):
        """
        初始化 CSP 问题。

        :param variables: 变量列表（可迭代）
        :param domains: 字典 {变量: 值域（可迭代）}
        :param neighbors: 字典 {变量: 邻居列表（可迭代）}
        :param constraint: 二元约束函数 constraint(X, x, Y, y) -> bool
                          表示变量 X 取 x、变量 Y 取 y 时是否满足约束。
        """

        self.variables = list(variables)
        self.domains = {var: set(domains[var]) for var in variables}
        self.neighbors = {var: set(neighbors[var]) for var in variables}

        # constraint(X, x, Y, y) -> bool
        self.constraint = constraint


    # ---------- Constraint propagation ----------
    def revise(self, X, Y, domains):
        """
        修订 X 的域：删除所有与 Y 的任意取值都不兼容的 x。

        :param X: 待修订的变量
        :param Y: 约束中的另一个变量
        :param domains: 当前域字典（会被原地修改）
        :return: bool 是否删除了至少一个值
        """

        revised = False

        # 注意不能一边遍历原 set，一边删除
        for x in set(domains[X]):
            # 是否存在某个 y ∈ D(Y)，使得 X=x,Y=y 满足约束？
            supported = any(self.constraint(X, x, Y, y) for y in domains[Y])
            if not supported:
                domains[X].remove(x)
                revised = True

        return revised


    def ac3(self, domains, queue=None):
        """ Arc Consistency Algorithm 3 -- 弧一致性算法

        维护所有弧 (X, Y) 的弧一致性，若发现某变量域变为空则返回 False。

        :param domains: 当前域字典（会被原地修改）
        :param queue: 初始弧队列，若为 None 则使用所有弧 (X, Y) for X in variables, Y in neighbors[X]
        :return: bool 是否维持了弧一致性（且所有域非空）
        """

        # 如果没有指定 queue，
        # 就从所有 arc 开始
        if queue is None:
            queue = deque((X, Y) for X in self.variables for Y in self.neighbors[X])
        else:
            queue = deque(queue)

        while queue:
            X, Y = queue.popleft()

            if self.revise(X, Y, domains):
                # X 已经没有任何可能取值, CSP 无解
                if not domains[X]:
                    return False

                # X 改变了, 那么所有依赖 X 的 Z 都要重新检查
                for Z in self.neighbors[X] - {Y}:
                    queue.append((Z, X))

        return True


    # ---------- Backtracking utilities ----------
    def consistent(self, var, value, assignment):
        """
        检查当给变量 var 赋值 value 时，是否与当前已赋值的所有邻居约束相容。

        :param var: 变量
        :param value: 尝试赋的值
        :param assignment: 当前已赋值的字典 {变量: 值}
        :return: bool 是否相容
        """

        for neighbor in self.neighbors[var]:
            # neighbor 还没有赋值，不用管
            if neighbor not in assignment:
                continue

            if not self.constraint(var, value, neighbor, assignment[neighbor]):
                return False

        return True


    def assignment_complete(self, assignment):
        """
        判断赋值是否完整（所有变量均已赋值）。

        :param assignment: 当前赋值字典
        :return: bool
        """

        # 所有变量都有值了
        return len(assignment) == len(self.variables)


    # ---------- Heuristics ----------
    def select_unassigned_variable(self, assignment, domains):
        """
        使用 MRV + Degree 启发式选择下一个待赋值的变量。

        MRV（Minimum Remaining Values）：优先选择当前域最小的变量。
        Degree（度启发式）：若 MRV 相同，优先选择未赋值邻居最多的变量（约束力最强）。

        :param assignment: 当前已赋值字典
        :param domains: 当前域字典
        :return: 选中的变量
        """

        unassigned = [v for v in self.variables if v not in assignment]

        return min(unassigned,
                   key=lambda v: (
                       # 第一优先级：MRV
                       len(domains[v]),

                       # 第二优先级：Degree
                       # Degree 越大越优先，所以取负
                       -sum(1 for n in self.neighbors[v] if n not in assignment)
                   ))


    def order_domain_values(self, var, assignment, domains):
        """
        使用 LCV（Least Constraining Value）启发式排列变量 var 的值域。

        按“该值排除的未赋值邻居的可能取值数量”升序排列，排除越少越优先。

        :param var: 变量
        :param assignment: 当前已赋值字典
        :param domains: 当前域字典
        :return: 排序后的值列表（升序）
        """

        def eliminated_values(value):
            """计算给 var 赋 value 后，其所有未赋值邻居中因此被排除的值的个数。"""

            count = 0

            for neighbor in self.neighbors[var]:
                if neighbor in assignment:
                    continue

                for neighbor_value in domains[neighbor]:
                    if not self.constraint(var, value, neighbor, neighbor_value):
                        count += 1

            return count

        return sorted(domains[var], key=eliminated_values)


    # ---------- Search ----------
    def backtrack_naive(self, assignment, domains):
        """
        纯回溯搜索（无启发式，无传播），仅作为版本 0 的演示。
        按变量顺序赋值，值也按原顺序尝试。

        :param assignment: 当前已赋值字典
        :param domains: 当前域字典（注意：该函数不会修改域）
        :return: 完整赋值字典或 None（无解）
        """

        if self.assignment_complete(assignment):
            return assignment.copy()

        var = next(v for v in self.variables if v not in assignment)

        # 随便找一个还没赋值的变量
        for value in domains[var]:
            if self.consistent(var, value, assignment):
                assignment[var] = value

                result = self.backtrack_naive(assignment, domains)
                if result is not None:
                    return result
                # 如果 result 返回 None 就回溯
                del assignment[var]

        return None


    def backtrack(self, assignment, domains):
        """
        完整回溯搜索，集成 MRV、Degree、LCV 和 MAC（Maintaining Arc Consistency）。

        搜索流程：
          1. 若赋值完整，返回副本。
          2. 用 MRV+Degree 选择变量 var。
          3. 用 LCV 排序 var 的值域。
          4. 尝试每个值，若与已赋值变量一致则临时赋值。
          5. 复制域，将 var 的域收缩为 {value}。
          6. 建立队列（所有邻居 → var）并执行 AC-3。
          7. 若传播成功，递归调用 backtrack；若成功则返回解。
          8. 否则回溯（删除 var 的赋值）并尝试下一个值。

        :param assignment: 当前已赋值字典
        :param domains: 当前域字典（该函数会复制，不影响调用者的域）
        :return: 完整赋值字典或 None
        """

        # 所有变量都已赋值
        if self.assignment_complete(assignment):
            return assignment.copy()

        # MRV + Degree
        var = self.select_unassigned_variable(assignment, domains)

        # LCV
        for value in self.order_domain_values(var, assignment, domains):
            # 与已经赋值的变量是否冲突
            if not self.consistent(var, value, assignment):
                continue

            # 尝试赋值
            assignment[var] = value

            # 为当前分支复制 domains（因为AC3会真正修改 domains，分支若失败则在 backtrack 后必须恢复 domains）
            new_domains = {v: set(values) for v, values in domains.items()}

            # var 已经被确定
            new_domains[var] = {value}

            # MAC(Maintaining Arc Consistency):
            # var 改变以后，需要检查 neighbor → var
            queue = [(neighbor, var) for neighbor in self.neighbors[var] if neighbor not in assignment]

            if self.ac3(new_domains, queue):
                result = self.backtrack(assignment, new_domains)
                if result is not None:
                    return result

            # 如果 result 返回 None 就回溯
            del assignment[var]

        return None


    def solve(self):
        """
        求解 CSP 问题的主入口。

        流程：
          1. 复制初始域。
          2. 运行全局 AC-3 进行约束传播。
          3. 若 AC-3 失败（某域为空），则直接返回 None（无解）。
          4. 否则调用 backtrack 进行完整搜索。

        :return: 完整赋值字典（若找到解）或 None
        """

        domains = {var: set(values) for var, values in self.domains.items()}

        # 先做一次全局 constraint propagation
        if not self.ac3(domains):
            return None

        return self.backtrack({}, domains)