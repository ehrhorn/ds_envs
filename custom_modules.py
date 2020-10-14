from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf


def read_dataset(file_path: Path) -> pd.DataFrame:
    dataset = pd.read_csv(file_path)
    return dataset


def clean_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset = dataset.dropna()
    return dataset


def one_hot_encode_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset["Origin"] = dataset["Origin"].map({1: "USA", 2: "Europe", 3: "Japan"})
    dataset = pd.get_dummies(dataset, prefix="", prefix_sep="")
    return dataset


def split_dataset(dataset: pd.DataFrame) -> dict:
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)
    return {"train": train_dataset, "test": test_dataset}


def get_features(datasets: dict) -> dict:
    train_features = datasets["train"].copy()
    test_features = datasets["test"].copy()
    train_labels = train_features.pop("MPG")
    test_labels = test_features.pop("MPG")
    return {
        "train_features": train_features,
        "test_features": test_features,
        "train_labels": train_labels,
        "test_labels": test_labels,
    }


def create_normalizer(
    datasets: dict,
) -> tf.python.keras.layers.preprocessing.normalization.Normalization:
    feature = np.array(datasets["train_features"]["Horsepower"])
    normalizer = tf.keras.layers.experimental.preprocessing.Normalization(
        input_shape=[
            1,
        ]
    )
    normalizer.adapt(feature)
    return normalizer


def create_model(
    normalizer: tf.python.keras.layers.preprocessing.normalization.Normalization,
) -> tf.python.keras.engine.sequential.Sequential:
    model = tf.keras.Sequential([normalizer, tf.keras.layers.Dense(units=1)])
    model.compile(
        optimizer=tf.optimizers.Adam(learning_rate=0.1), loss="mean_absolute_error"
    )
    return model