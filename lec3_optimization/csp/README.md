# 约束满足问题（Constraint Satisfaction Problem）

`binary_CSP.py` 实现有限值域二元 CSP 求解器，组合 Backtracking、AC-3、MRV、Degree、
LCV 与 MAC；`australia_map.py` 用澳大利亚地图着色验证求解流程。

## 问题表示

一个 CSP 包含：

- 变量集合 $X_1,\ldots,X_n$；
- 每个变量的值域 $D(X_i)$；
- 判断变量取值组合是否合法的约束。

当前 `CSP` 类接收一个统一的二元约束函数：

```python
constraint(X, x, Y, y) -> bool
```

并通过 `neighbors[X]` 指定与变量 $X$ 存在约束的其他变量。求解结果是完整的
`{variable: value}` 字典，无解时返回 `None`。

## Backtracking Search

回溯搜索逐步构造部分赋值。对当前变量尝试一个值，如果它与已赋值邻居一致，就递归
处理下一个变量；当前分支无法完成时撤销赋值并尝试下一个值。

`backtrack_naive` 按输入顺序选择变量和值，只进行一致性检查。`backtrack` 额外加入
启发式与约束传播，通常能更早发现不可能完成的分支。

## Arc Consistency 与 AC-3

有向弧 $(X,Y)$ 是 arc-consistent 的，当且仅当 $D(X)$ 中每个值 $x$ 都能在 $D(Y)$
中找到至少一个满足约束的支持值：

$$\forall x\in D(X),\ \exists y\in D(Y):C(X=x,Y=y)$$

`revise(X, Y, domains)` 删除所有没有支持的 $x$。一旦 $D(X)$ 改变，所有依赖 $X$
的相邻弧都需要重新检查。`ac3` 使用队列重复这个过程；任何值域变为空都说明当前
分支无解。

Arc consistency 能删去不可能值，但不能保证剩余域一定组成全局解，所以通常仍需要
回溯搜索。

## 变量选择：MRV 与 Degree

`select_unassigned_variable` 首先使用 Minimum Remaining Values：

$$X^*=\operatorname*{argmin}_{X\notin assignment}|D(X)|$$

值域越小的变量越可能尽早暴露失败。若多个变量的剩余值数量相同，再使用 Degree
Heuristic，优先选择未赋值邻居最多的变量，让当前选择尽可能多地约束后续搜索。

## 值排序：LCV

Least Constraining Value 优先尝试排除邻居候选值最少的取值。当前实现对每个候选
$x$ 统计它与未赋值邻居值不兼容的次数，并按计数升序排列。LCV 的目标是给后续变量
保留更多选择。

## Maintaining Arc Consistency

`backtrack` 尝试 `var = value` 后会复制当前值域，把 $D(var)$ 收缩为单元素集合，再从
所有 `neighbor -> var` 的弧开始运行 AC-3。这种在每次搜索赋值后维持弧一致性的方式
称为 MAC。

完整流程为：

```text
全局 AC-3
  -> MRV + Degree 选择变量
  -> LCV 排列候选值
  -> 检查与已赋值邻居的一致性
  -> 收缩当前变量的域
  -> MAC 传播
  -> 递归或回溯
```

每个分支复制一份 domains，因此失败分支的约束传播不会污染兄弟分支。

## 澳大利亚地图着色

`australia_map.py` 把 `WA`、`NT`、`SA`、`Q`、`NSW`、`V` 和 `T` 作为变量，把红、
绿、蓝作为每个变量的值域。相邻州之间使用同一个约束：

$$color(X)\ne color(Y)$$

`T` 没有邻居，因此可以选择任意颜色。集合的迭代顺序不保证固定，所以不同运行得到
的具体合法配色可能不同。

## 运行示例

该示例只依赖 Python 标准库。在当前目录执行：

```bash
cd lec3_optimization/csp
python australia_map.py
```

当前求解器面向有限值域和二元约束。全局约束、软约束、最优解目标以及大型实例的
专用数据结构尚未实现。
