"""CS50 AI Lec5 代表性示例：用 Dense Neural Network 判断真假钞。

这是基于课程思路重新整理的学习版，不是官方源码的逐字复制。
需要将课程使用的 ``banknotes.csv`` 放在本文件附近，或通过 --csv 指定路径。
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a neural network on banknotes.csv.")
    parser.add_argument("--csv", type=Path, default=Path(__file__).with_name("banknotes.csv"))
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--test-size", type=float, default=0.4)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def load_data(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """读取课程 banknotes.csv：前 4 列是特征，第 5 列是类别。"""
    if not path.exists():
        raise FileNotFoundError(f"Could not find {path}. Place the course banknotes.csv there or pass --csv PATH.")

    evidence: list[list[float]] = []
    labels: list[float] = []

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            if not row:
                continue
            if len(row) < 5:
                raise ValueError("Each CSV row must contain at least 5 columns.")

            evidence.append([float(cell) for cell in row[:4]])

            # 与 Lec5 notes 的 TensorFlow 示例保持同一语义：
            # 原始数据第 5 列为 0 时映射为 1（Authentic），否则映射为 0。
            labels.append(1.0 if row[4] == "0" else 0.0)

    if not evidence:
        raise ValueError("No data rows were found in the CSV file.")

    return np.asarray(evidence, dtype=np.float32), np.asarray(labels, dtype=np.float32)


def main() -> None:
    args = parse_args()

    if args.epochs <= 0:
        raise SystemExit("epochs must be positive.")
    if not 0.0 < args.test_size < 1.0:
        raise SystemExit("test-size must be between 0 and 1.")

    try:
        import tensorflow as tf
        from sklearn.model_selection import train_test_split
    except ImportError as exc:
        raise SystemExit(
            "This example requires TensorFlow and scikit-learn."
        ) from exc

    tf.keras.utils.set_random_seed(args.random_state)
    X, y = load_data(args.csv)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )

    model = tf.keras.Sequential(
        [
            tf.keras.Input(shape=(4,), name="banknote_features"),
            tf.keras.layers.Dense(8, activation="relu", name="hidden"),
            tf.keras.layers.Dense(1, activation="sigmoid", name="output"),
        ],
        name="banknote_classifier",
    )

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()
    model.fit(X_train, y_train, epochs=args.epochs, verbose=2)

    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"test_loss={loss:.6f}")
    print(f"test_accuracy={accuracy:.4f}")


if __name__ == "__main__":
    main()
