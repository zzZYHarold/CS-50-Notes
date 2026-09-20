# 对抗搜索（Adversarial Search）

这一目录实现双人零和、确定性、完全信息博弈中的 Minimax、Alpha-Beta 剪枝、深度
受限 Alpha-Beta 和 Monte Carlo Tree Search（MCTS）。`game.py` 定义通用博弈接口，
其他文件负责选择当前状态下的动作。

## 博弈接口

具体游戏需要继承 `AdversarialGame` 并实现：

| 方法 | 含义 |
| --- | --- |
| `player(state)` | 当前轮到哪个玩家 |
| `actions(state)` | 当前状态的合法动作 |
| `result(state, action)` | 执行动作后的新状态 |
| `isTerminal(state)` | 是否为终局 |
| `utility(state, player)` | 终局对指定玩家的效用 |

效用通常使用胜、平、负分别对应 $1,0,-1$，但算法只要求数值越大对根玩家越有利。

## Minimax

Minimax 假设双方都采用最优策略。以根玩家视角，轮到根玩家时选择最大值，轮到对手
时选择最小值：

$$V(s)=\begin{cases}
U(s),&s\text{ is terminal}\\
\max_{a\in A(s)}V(Result(s,a)),&Player(s)=root\\
\min_{a\in A(s)}V(Result(s,a)),&Player(s)\ne root
\end{cases}$$

`minimax_advanced.py` 先记录 `root_player`，因此可以从任意一方行动的状态开始，并始终
用根玩家视角解释终局效用。若分支因子为 $b$、终局深度为 $m$，完整搜索时间复杂度为
$O(b^m)$。

## Alpha-Beta Pruning

Alpha-Beta 与 Minimax 返回相同决策，但维护两个界：

- $\alpha$：MAX 目前至少能够保证的值；
- $\beta$：MIN 目前至多允许的值。

当 $\alpha\ge\beta$ 时，当前分支不可能影响祖先决策，可以停止继续展开。剪枝不会改变
最终 Minimax 值，但效率高度依赖动作顺序；理想排序下，时间复杂度可接近
$O(b^{m/2})$。

`alphabeta_advanced.py` 根据 `game.player(state)` 判断当前层是 MAX 还是 MIN，并统一从
根玩家视角调用 `utility`，是当前接口下更完整的版本。

## 深度受限搜索与评估函数

当博弈树无法搜索到终局，可以只展开到深度 $d$，然后使用评估函数近似局面价值：

$$V_d(s)=evaluation(s)$$

评估函数应从固定玩家视角返回可比较的数值，并尽量让更有利的局面得到更高分。
深度限制控制计算量，但也会产生 horizon effect：重要结果恰好发生在搜索边界之外时，
算法可能做出误判。

## Monte Carlo Tree Search

`mcts.py` 重复执行四个阶段：

1. Selection：沿已经扩展的树使用 UCT 选择子节点；
2. Expansion：从尚未尝试的动作中随机扩展一个孩子；
3. Simulation：随机行动直到终局；
4. Backpropagation：把根玩家视角的 reward 累加回路径上的所有节点。

对已经访问的孩子，UCT 分数为：

$$UCT_i=s\bar{X}_i+C\sqrt{\frac{\ln N}{n_i}}$$

其中 $\bar{X}_i$ 是孩子的平均 reward，$n_i$ 是孩子访问次数，$N$ 是父节点访问次数，
$C$ 控制探索强度。轮到根玩家时 $s=1$，轮到对手时 $s=-1$。搜索结束后，代码选择
访问次数最多的根节点孩子，而不是继续加入探索奖励。

MCTS 不需要评估函数，也不必完整展开博弈树；结果是采样近似，`iterations` 越大通常
越稳定。`seed` 可以固定 rollout 的随机性。

## 文件定位

| 文件 | 定位 |
| --- | --- |
| `game.py` | 双人零和博弈抽象接口 |
| `minimax.py` | 显式拆分 MAX/MIN 递归的基础版本 |
| `minimax_advanced.py` | 依据当前玩家判断层次的通用版本 |
| `alphabeta.py` | 显式拆分 MAX/MIN 递归的基础版本 |
| `alphabeta_advanced.py` | 与当前 `AdversarialGame` 接口一致的通用版本 |
| `depth_limited_alphabeta.py` | 加入深度限制和评估函数的版本 |
| `mcts.py` | 完整的 Selection/Expansion/Simulation/Backpropagation 流程 |

## 使用方式

基础版保留显式的 `maxValue` / `minValue`，advanced 版根据 `game.player(state)` 决定
当前节点角色；两组实现都使用根玩家视角调用 `utility(state, root_player)`。深度受限
版本要求 `depth_limit >= 1`，并在 MAX 与 MIN 之间正确交替。

可以通过仓库根目录的稳定接口导入推荐版本：

```python
from cs50_ai import (
    AdversarialGame,
    minimax,
    alpha_beta_search,
    depth_limited_alpha_beta_search,
    monte_carlo_tree_search,
)
```

MCTS 要求 `iterations` 为正数，并要求每个非终局状态至少有一个合法动作。当前目录没有
绑定具体游戏；增加游戏时，建议先用结果可手算的小型博弈树验证 Minimax 与
Alpha-Beta 返回相同动作。
