"""CS50 AI Lec5 代表性示例：使用 CNN 识别 MNIST 手写数字。

这是基于课程 Lec5 模型结构重新整理的学习版，不是官方源码的逐字复制。
"""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the Lec5-style CNN on MNIST.")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--limit-train", type=int, default=None)
    parser.add_argument("--limit-test", type=int, default=None)
    parser.add_argument("--save-model", type=str, default=None)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.epochs <= 0 or args.batch_size <= 0:
        raise SystemExit("epochs and batch-size must be positive.")
    if args.limit_train is not None and args.limit_train <= 0:
        raise SystemExit("limit-train must be positive.")
    if args.limit_test is not None and args.limit_test <= 0:
        raise SystemExit("limit-test must be positive.")

    try:
        import tensorflow as tf
    except ImportError as exc:
        raise SystemExit("This example requires TensorFlow.") from exc

    tf.keras.utils.set_random_seed(args.random_state)
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # 像素从 [0, 255] 缩放到 [0, 1]。
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    # Lec5 示例使用 categorical cross entropy，因此把标签转成 one-hot。
    y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)

    # Conv2D 需要显式 channel 维：28 x 28 -> 28 x 28 x 1。
    x_train = x_train[..., None]
    x_test = x_test[..., None]

    if args.limit_train is not None:
        x_train = x_train[: args.limit_train]
        y_train = y_train[: args.limit_train]
    if args.limit_test is not None:
        x_test = x_test[: args.limit_test]
        y_test = y_test[: args.limit_test]

    model = tf.keras.Sequential(
        [
            tf.keras.Input(shape=(28, 28, 1), name="image"),
            tf.keras.layers.Conv2D(
                32,
                (3, 3),
                activation="relu",
                name="conv",
            ),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2), name="pool"),
            tf.keras.layers.Flatten(name="flatten"),
            tf.keras.layers.Dense(128, activation="relu", name="hidden"),
            tf.keras.layers.Dropout(0.5, name="dropout"),
            tf.keras.layers.Dense(10, activation="softmax", name="output"),
        ],
        name="handwriting_cnn",
    )

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()
    model.fit(
        x_train,
        y_train,
        epochs=args.epochs,
        batch_size=args.batch_size,
        verbose=2,
    )

    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"test_loss={loss:.6f}")
    print(f"test_accuracy={accuracy:.4f}")

    if args.save_model:
        model.save(args.save_model)
        print(f"model saved to {args.save_model}")


if __name__ == "__main__":
    main()
