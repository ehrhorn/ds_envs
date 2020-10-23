from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf


def split_dataset(dataset: pd.DataFrame):
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)
    return {"train": train_dataset, "test": test_dataset}


def get_features(datasets: dict):
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
):
    feature = np.array(datasets["train_features"]["Horsepower"])
    normalizer = tf.keras.layers.experimental.preprocessing.Normalization(
        input_shape=[
            1,
        ]
    )
    normalizer.adapt(feature)
    return normalizer


def create_model(normalizer):
    model = tf.keras.Sequential([normalizer, tf.keras.layers.Dense(units=1)])
    model.compile(
        optimizer=tf.optimizers.Adam(learning_rate=0.1), loss="mean_absolute_error"
    )
    return model
