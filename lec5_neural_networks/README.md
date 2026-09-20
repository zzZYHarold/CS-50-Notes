# 神经网络（Neural Networks）

这一目录不从零实现反向传播，而是用 TensorFlow/Keras 复现 Lec5 中两个代表性任务：
`banknotes.py` 用全连接网络完成表格数据二分类，`handwriting.py` 用卷积神经网络识别
MNIST 手写数字。两份代码都包含数据准备、模型定义、训练、评估和命令行参数。

## 从神经元到网络

全连接层先计算线性组合，再应用激活函数：

$$z=W^Tx+b$$

$$a=g(z)$$

堆叠多个可训练层后，模型可以表示非线性决策边界。Keras 在 `model.fit` 中完成前向
传播、损失计算、自动微分和参数更新，因此这里关注的是如何为不同数据选择输入表示、
网络结构、输出层和损失函数。

## Banknote 二分类

`banknotes.py` 读取 `banknotes.csv`。前四列转换为 `float32` 特征，原始第五列为 `0`
时映射为 `1`（Authentic），其他值映射为 `0`。

数据使用 `train_test_split` 划分，`stratify=y` 尽量保持训练集与测试集的类别比例一致。
网络结构为：

```text
4 features
  -> Dense(8, ReLU)
  -> Dense(1, Sigmoid)
```

Sigmoid 把输出压缩到 $(0,1)$，可解释为正类概率：

$$\sigma(z)=\frac{1}{1+e^{-z}}$$

二分类使用 Binary Cross-Entropy：

$$L=-\frac{1}{N}\sum_{i=1}^{N}
\left[y_i\log\hat{y}_i+(1-y_i)\log(1-\hat{y}_i)\right]$$

优化器为 Adam，评估指标为 Accuracy。默认数据路径是脚本同目录下的
`banknotes.csv`；数据文件不存在时会给出明确错误，也可以通过 `--csv` 指定路径。

运行示例：

```bash
python lec5_neural_networks/banknotes.py --csv path/to/banknotes.csv --epochs 20
```

## MNIST 手写数字分类

`handwriting.py` 通过 Keras 加载 MNIST。灰度像素从 $[0,255]$ 缩放到 $[0,1]$，并把
输入 shape 从 `(N, 28, 28)` 扩展为 `(N, 28, 28, 1)`。标签转换为长度为 10 的
One-Hot 向量。

模型结构为：

```text
(28, 28, 1)
  -> Conv2D(32, 3x3, ReLU)
  -> MaxPooling2D(2x2)
  -> Flatten
  -> Dense(128, ReLU)
  -> Dropout(0.5)
  -> Dense(10, Softmax)
```

卷积层使用局部连接和权重共享提取空间特征。未指定 padding 时使用 `valid`，因此
$28\times28$ 输入经过 $3\times3$ 卷积后变成 $26\times26\times32$，再经 $2\times2$
最大池化变成 $13\times13\times32$。

Softmax 把十个输出转换为和为 $1$ 的类别分布：

$$P(y=k\mid x)=\frac{e^{z_k}}{\sum_{j=1}^{10}e^{z_j}}$$

由于标签已经 One-Hot 编码，训练使用 Categorical Cross-Entropy。`Dropout(0.5)` 只在
训练时随机屏蔽一部分激活，评估和预测时不会随机丢弃单元。

完整训练：

```bash
python lec5_neural_networks/handwriting.py --epochs 10 --batch-size 64
```

快速 smoke test 可以限制样本数：

```bash
python lec5_neural_networks/handwriting.py --epochs 1 --limit-train 1000 --limit-test 200
```

两个 limit 参数如果提供，必须是正整数；这可以避免空数据集和负数切片造成的歧义。

使用 `--save-model model.keras` 可以保存训练后的模型。第一次运行时，Keras 可能需要
联网下载 MNIST。

## 两个任务的对应关系

| 维度 | Banknotes | Handwriting |
| --- | --- | --- |
| 数据类型 | 4 个表格特征 | $28\times28$ 灰度图像 |
| 任务 | 二分类 | 10 类分类 |
| 特征提取 | Dense 层直接组合特征 | Conv2D 学习局部空间特征 |
| 输出层 | 1 个 Sigmoid | 10 个 Softmax |
| 损失 | Binary Cross-Entropy | Categorical Cross-Entropy |
| 额外依赖 | NumPy、scikit-learn、TensorFlow | TensorFlow |

## 实现边界

- 两份代码是框架使用示例，不展示梯度公式如何转化为手写反向传播。
- `banknotes.py` 依赖外部 CSV，仓库当前未包含该数据文件。
- `handwriting.py` 使用 Keras 自带数据加载器，首次运行可能下载数据。
- 当前示例只报告一次 train/test split 或固定测试集结果，尚未加入验证集、Early
  Stopping、超参数搜索、混淆矩阵或训练曲线。
- 固定随机种子有助于复现，但不同 TensorFlow 版本、硬件和底层算子仍可能产生细微
  数值差异。
