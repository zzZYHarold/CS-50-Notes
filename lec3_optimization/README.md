# 优化（Optimization）

优化问题要求从候选状态中找到目标函数尽可能好的状态。本目录从两条路线展开：
`local_search/` 在邻域中迭代改进当前解，`csp/` 把问题表示为变量、值域和约束，
通过约束传播与回溯寻找可行赋值。

## Local Search

局部搜索通常只维护一个或少量当前状态，不关心从起点到当前状态的完整动作路径。
这里实现爬山法、随机重启与模拟退火，并提供医院选址和 Traveling Salesman Problem
两种问题表示。

爬山法只接受更优邻居，收敛快但可能停在局部最优；模拟退火在高温阶段允许以一定
概率接受较差解，随后逐渐降低这种概率。详见
[`local_search/README.md`](local_search/README.md)。

## Constraint Satisfaction Problem

CSP 由变量集合 $X$、各变量的值域 $D(X)$ 和约束集合组成。这里的通用求解器支持
二元约束，并把以下技术组合起来：

- AC-3 弧一致性；
- Backtracking Search；
- MRV 与 Degree 变量选择；
- LCV 值排序；
- MAC（Maintaining Arc Consistency）。

澳大利亚地图着色用一个相邻地区颜色不同的约束展示完整求解流程。详见
[`csp/README.md`](csp/README.md)。

## 两类方法的区别

| 维度 | Local Search | CSP |
| --- | --- | --- |
| 目标 | 改善数值代价 | 找到满足全部约束的赋值 |
| 状态 | 通常是完整候选解 | 通常是部分赋值与剩余值域 |
| 搜索轨迹 | 常主动丢弃历史 | 失败时回溯到分支点 |
| 完备性 | 当前实现不保证全局最优 | 有限值域回溯可系统枚举 |
| 典型用途 | 选址、路线、连续或巨大空间 | 排程、着色、逻辑配置 |

这两种表示并非互斥：约束可以转化为惩罚项交给局部搜索，优化目标也可以附加到
CSP 形成 Constraint Optimization Problem。当前代码分别保留两条最清晰的教学实现。
