# 不确定性（Uncertainty）

这一目录使用 Hidden Markov Model（HMM，隐马尔可夫模型）描述“真实状态不可直接
观察，只能看到带噪声证据”的序列问题，并用 Viterbi Algorithm 求最可能的隐藏
状态序列。

`problem.py` 定义通用 HMM 接口，`weather_problem.py` 给出天气与雨伞的离散示例，
`viterbi.py` 实现动态规划与路径回溯。

## Hidden Markov Model

设隐藏状态序列为 $X_1,\ldots,X_T$，观察序列为 $E_1,\ldots,E_T$。当前接口需要
具体问题提供三类概率：

$$P(X_1=x)$$

$$P(X_t=x\mid X_{t-1}=x')$$

$$P(E_t=e\mid X_t=x)$$

一阶马尔可夫假设认为当前状态在给定上一状态后与更早状态无关；传感器模型认为
当前观察在给定当前状态后与其他变量无关。

## Viterbi Algorithm

Viterbi 不计算所有隐藏序列的总概率，而是保留“以每个状态结尾的最佳路径”。令
$m_t(x)$ 表示时间 $t$ 以状态 $x$ 结束的最佳路径及当前证据的联合概率。

初始化为：

$$m_1(x)=P(X_1=x)P(E_1=e_1\mid X_1=x)$$

之后递推：

$$m_t(x)=P(E_t=e_t\mid X_t=x)\max_{x'}\left[m_{t-1}(x')P(X_t=x\mid X_{t-1}=x')\right]$$

在计算最大值时，代码同时记录达到当前状态的最佳前驱。最后选择分数最高的终点，
再沿 `backpointers` 逆向恢复完整路径。若状态数为 $S$、序列长度为 $T$，时间复杂度
为 $O(TS^2)$，保存回溯指针需要 $O(TS)$ 空间。

## 天气示例

`WeatherProblem` 使用两个隐藏状态 `Rain` 和 `Sun`，观察值为 `Umbrella` 或
`No Umbrella`。示例观察序列是：

```text
Umbrella -> No Umbrella -> Umbrella
```

初始概率、天气转移概率和雨伞发射概率都直接保存在字典中。它是一个用于验证
Viterbi 流程的小模型，不是从数据中估计概率的训练程序。

## 运行示例

该示例只依赖 Python 标准库。在当前目录执行：

```bash
cd lec2_uncertainty
python viterbi.py
```

输出包括观察序列、最可能的隐藏天气序列，以及该单条最佳路径与全部观察的联合
概率。这个分数不是观察序列的总概率；后者需要对所有隐藏路径求和，可使用 Forward
Algorithm 计算。

## 实现边界

- 概率直接相乘，长序列可能发生浮点下溢；更稳健的实现通常在 log-space 中相加。
- 当前接口针对有限离散状态与离散观察。
- 空观察序列返回 `([], 0.0)`。
- 模型参数由具体问题手工给定，尚未包含学习转移或发射概率的算法。
