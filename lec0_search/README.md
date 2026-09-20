# 搜索（Search）

这一讲把智能体的决策建模为在状态空间中寻找动作序列。`search_algorithms/`
处理单智能体路径搜索，`adversarial_search/` 处理两个理性玩家之间的零和博弈。

## 状态空间搜索

搜索问题由初始状态、目标测试和后继函数组成。后继函数返回：

```text
(successor, action, step_cost)
```

不同算法共享这套问题接口，主要区别在于 frontier 的取出顺序以及是否使用路径代价
$g(n)$ 和启发式估计 $h(n)$。

| 算法 | 节点优先级 | 主要性质 |
| --- | --- | --- |
| DFS | 最深、最后加入 | 内存较少，不保证最短路径 |
| BFS | 最浅、最早加入 | 单位代价下得到最少步数解 |
| UCS | 最小 $g(n)$ | 非负代价下得到最低代价解 |
| GBFS | 最小 $h(n)$ | 依赖启发式，通常更快但不保证最优 |
| A* | 最小 $g(n)+h(n)$ | 合适启发式下兼顾效率与最优性 |
| IDDFS | 逐步增加深度限制 | 结合 DFS 的空间优势与 BFS 的层次性 |

具体接口、公式和代码差异见 [`search_algorithms/README.md`](search_algorithms/README.md)。

## 对抗搜索

对抗搜索不再只问“怎样到达目标”，而是要在对手也会选择行动的前提下寻找策略。
这里包含 Minimax、Alpha-Beta 剪枝、深度受限搜索和 Monte Carlo Tree Search。

Minimax 与 Alpha-Beta 适合可以系统展开的确定性博弈树；MCTS 用重复采样近似评估
动作，更适合分支很多、完整搜索代价过高的场景。具体实现见
[`adversarial_search/README.md`](adversarial_search/README.md)。

## 目录结构

```text
lec0_search/
├── README.md
├── search_algorithms/
│   ├── README.md
│   ├── problem.py
│   ├── dfs.py / bfs.py / ucs.py
│   ├── gbfs.py / astar.py / iddfs.py
│   └── template
└── adversarial_search/
    ├── README.md
    ├── game.py
    ├── minimax.py / minimax_advanced.py
    ├── alphabeta.py / alphabeta_advanced.py
    ├── depth_limited_alphabeta.py
    └── mcts.py
```

当前目录以算法函数和抽象接口为主，没有统一的命令行入口。使用时需要实现对应的
`SearchProblem` 或 `AdversarialGame`，再把问题实例交给算法。
