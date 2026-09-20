# 状态空间搜索（State-Space Search）

这一目录用统一的 `SearchProblem` 接口实现 DFS、BFS、UCS、Greedy Best-First
Search、A* 和 IDDFS。各算法都返回从初始状态到目标状态的动作列表；frontier 耗尽且
没有找到目标时返回 `None`。

## 搜索问题接口

`problem.py` 要求具体问题实现三个方法：

| 方法 | 含义 |
| --- | --- |
| `getStartState()` | 返回初始状态 |
| `isGoalState(state)` | 判断状态是否满足目标 |
| `getSuccessors(state)` | 返回 `(successor, action, step_cost)` 列表 |

状态会作为 `set` 或 `dict` 的键，因此必须可哈希。每个 frontier 元素还保存到达当前
状态的动作序列，找到目标后可以直接返回路径。

## 通用搜索框架

`template` 给出所有图搜索算法共有的骨架：

```text
把初始节点加入 frontier
while frontier 非空:
    按算法规则取出一个节点
    如果它是目标，返回动作序列
    展开尚未处理的后继并加入 frontier
frontier 耗尽后返回 None
```

算法的主要区别是 frontier 数据结构、节点优先级和重复状态处理方式。

## Depth-First Search

`dfs.py` 使用 list 作为 LIFO 栈，总是先展开最后加入的节点。若搜索树的最大深度为
$m$、最大分支因子为 $b$，树搜索形式的最坏时间复杂度为 $O(b^m)$，空间复杂度约为
$O(bm)$。

DFS 可能很快到达深层解，但找到的路径不一定最短；在无限深状态空间中也可能一直
沿错误分支前进。图搜索必须正确过滤重复状态，才能避免在环中反复展开。

## Breadth-First Search

`bfs.py` 使用 `collections.deque` 作为 FIFO 队列，按深度逐层展开。设最浅目标深度为
$d$，最坏时间和空间复杂度都为 $O(b^d)$。

当所有动作代价相同，BFS 找到的是动作数最少的路径；动作代价不同时，“步数最少”
不等于“总代价最低”，此时应使用 UCS。

## Uniform-Cost Search

`ucs.py` 使用最小堆，每次展开累计路径代价最小的节点：

$$g(n)=\sum_{a\in path(n)}c(a)$$

`best_cost[state]` 保存目前到达某状态的最低代价。堆中较贵的旧记录不会被立即删除，
而是在弹出时识别为过期记录并跳过。只要动作代价非负，UCS 在弹出目标时得到最低
总代价路径；代码会拒绝负动作代价。

## Greedy Best-First Search

`gbfs.py` 只按启发式估计排序：

$$priority(n)=h(n)$$

$h(n)$ 估计当前状态到目标的剩余代价。GBFS 往往比无信息搜索更直接地朝目标推进，
但忽略已经付出的路径代价，因此通常不保证最优。启发式很差时也可能走大量弯路。

## A* Search

`astar.py` 同时考虑已付代价和剩余估计：

$$f(n)=g(n)+h(n)$$

`nullHeuristic` 恒为 $0$，因此 A* 会退化为 UCS。`manhattanHeuristic` 对二维网格状态
计算曼哈顿距离：

$$h((r,c))=|r-r_g|+|c-c_g|$$

对图搜索而言，若启发式是一致的（consistent），即对每条代价为 $c(n,n')$ 的边满足：

$$h(n)\le c(n,n')+h(n')$$

则当前实现按最低 $f$ 弹出目标时可得到最优路径。代码同样要求动作代价非负，并用
`best_cost` 支持发现更便宜路径后的重新入堆。

## Iterative Deepening DFS

`iddfs.py` 依次使用深度限制 $0,1,2,\ldots$ 运行 Depth-Limited Search。内部哨兵
`_CUTOFF` 区分“本轮因深度限制停止”和“状态空间内确实无解”，从而决定是否继续增加
深度。

IDDFS 会重复访问浅层节点，但在分支因子较大时，节点总数通常由最深一层主导。它在
单位步长问题中具有 BFS 的最浅解性质，同时保留接近 DFS 的空间需求。

## 算法对比

| 算法 | frontier | 使用代价 | 使用启发式 | 一般是否最优 |
| --- | --- | ---: | ---: | --- |
| DFS | 栈 | 否 | 否 | 否 |
| BFS | 队列 | 只隐含单位代价 | 否 | 单位代价时是 |
| UCS | 最小堆 | $g(n)$ | 否 | 非负代价时是 |
| GBFS | 最小堆 | 否 | $h(n)$ | 否 |
| A* | 最小堆 | $g(n)$ | $h(n)$ | 一致启发式下是 |
| IDDFS | 深度受限栈 | 只隐含深度 | 否 | 单位代价时是 |

## 使用方式

这些文件是算法模块，没有绑定某个具体问题。实现 `SearchProblem` 后，可以通过仓库
根目录的合法模块名导入：

```python
from cs50_ai import SearchProblem, breadth_first_search
```

所有源码目录均使用合法的 snake_case 包名，可以直接通过普通 Python 导入。根目录的
`cs50_ai.py` 额外提供更简洁、命名一致的公共入口；各模块也保留从所在目录直接加载时
的导入兼容性。

BFS 和 DFS 都在状态第一次进入 frontier 时标记为已访问，后续遇到同一状态不会重复
入队，因此可安全处理含环的有限图。
