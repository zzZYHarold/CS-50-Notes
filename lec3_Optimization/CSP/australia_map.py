# 用于测试CSP solver
from binary_CSP import CSP  # 导入刚才写的类


if __name__ == "__main__":
    # 1. 变量
    variables = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]

    # 2. 颜色
    colors = {"red", "green", "blue"}

    # 3. 值域
    domains = {var: set(colors) for var in variables}

    # 4. 邻接关系
    neighbors = {
        "WA": {"NT", "SA"},
        "NT": {"WA", "SA", "Q"},
        "SA": {"WA", "NT", "Q", "NSW", "V"},
        "Q": {"NT", "SA", "NSW"},
        "NSW": {"Q", "SA", "V"},
        "V": {"SA", "NSW"},
        "T": set()
    }

    # 5. 约束
    def different_color(X, x, Y, y):
        return x != y

    # 6. 求解
    csp = CSP(variables, domains, neighbors, different_color)
    solution = csp.solve()

    # 7. 输出
    if solution:
        print("找到着色方案：")
        for state, color in solution.items():
            print(f"  {state}: {color}")
    else:
        print("无解")

"""
找到着色方案：
  SA: red
  NT: green
  NSW: green
  WA: blue
  Q: blue
  V: blue
  T: red
"""