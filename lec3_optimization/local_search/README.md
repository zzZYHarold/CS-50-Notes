# 局部搜索（Local Search）

这一目录实现 Hill Climbing、Random-Restart Hill Climbing 和 Simulated Annealing，
并通过统一的 `LocalSearchProblem` 接口表示医院选址与 Traveling Salesman Problem
（TSP）。所有算法都按“代价越小越好”的约定工作。

## 问题接口

`problem.py` 定义三个必要操作：

| 方法 | 含义 |
| --- | --- |
| `initial_state()` | 生成一个初始候选解 |
| `neighbors(state)` | 枚举一步可达的邻居 |
| `cost(state)` | 返回需要最小化的代价 |

默认 `random_neighbor` 会先生成全部邻居再随机选择一个；如果邻域很大，具体问题可以
重写它，直接采样一个邻居。

## Hill Climbing

`hill_climbing.py` 每轮计算所有邻居的代价，找出代价最低的一组，并在并列最优邻居中
随机选择一个。如果最佳邻居也不能严格改善当前代价，算法立即停止：

$$f(s')\ge f(s)\Rightarrow stop$$

这种策略只接受下坡移动，因此收敛直接，但可能停在局部最优、平台或山脊。每一步的
计算量与邻居数量成正比。

`hill_climbing_Another_Version.py` 展示另一个接口版本：调用方显式传入初始状态，并在
并列时直接取 `min` 返回的第一个邻居。它保留作抽象方式的对照。

## Random Restart

随机重启从多个随机初始状态独立运行爬山法，再返回代价最低的结果：

$$s^*=\operatorname*{argmin}_{s\in\{s_1,\ldots,s_R\}}f(s)$$

只要 `initial_state()` 确实有随机性，增加重启次数就提高探索多个吸引域的机会，但计算
成本也近似按重启次数线性增长。

## Simulated Annealing

`simulated_annealing.py` 每一步只采样一个随机邻居。更优解一定接受；较差解仍以一定
概率接受。代码令：

$$\Delta=f(current)-f(neighbor)$$

当 $\Delta\le0$ 时，接受概率为：

$$P(accept)=\exp\left(\frac{\Delta}{T_t}\right)$$

温度按指数方式下降：

$$T_t=T_0\alpha^t$$

高温时更容易跳出局部最优，低温时逐渐接近贪心搜索。`initial_temperature`、
`cooling_rate` 和 `max_steps` 共同控制探索范围与运行成本。

## Hospitals Problem

`HospitalsProblem` 的状态是医院坐标组成的 `frozenset`。邻域操作每次把一家医院向上、
下、左或右移动一格，同时拒绝越界、建在房屋上或与其他医院重叠的状态。

目标函数是每座房屋到最近医院的曼哈顿距离之和：

$$f(H)=\sum_{house\in houses}\min_{hospital\in H}
\left(|r_{house}-r_{hospital}|+|c_{house}-c_{hospital}|\right)$$

使用不可变 `frozenset` 可以让状态安全地保存和比较。

## Traveling Salesman Problem

`TravelingSalesmanProblem` 把城市访问顺序表示为 tuple。`neighbors` 枚举交换任意两个
城市得到的 $O(n^2)$ 个邻居；为模拟退火实现的 `random_neighbor` 则直接随机选择两个
位置交换，避免先构造整个邻域。

路线代价是相邻城市欧氏距离之和，并包含最后一个城市返回第一个城市的闭环边：

$$f(route)=\sum_{i=1}^{n}\lVert p_i-p_{(i\bmod n)+1}\rVert_2$$

## 使用方式与边界

当前文件提供算法和问题类，没有命令行入口。调用流程是构造具体 problem，再把它传给
`hill_climb`、`random_restart` 或 `simulated_annealing`。例如：

```python
from cs50_ai import TravelingSalesmanProblem, simulated_annealing
```

这些实现是随机化教学算法，不保证找到全局最优。需要可复现实验时，应在调用前设置
Python `random` 模块的种子。模拟退火会保留搜索期间见过的最低代价状态，避免最后几步
接受较差邻居后丢失已经找到的最佳解。
