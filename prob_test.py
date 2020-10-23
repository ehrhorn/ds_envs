# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import tensorflow_probability as tfp

# %%
url = "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
column_names = [
    "MPG",
    "Cylinders",
    "Displacement",
    "Horsepower",
    "Weight",
    "Acceleration",
    "Model Year",
    "Origin",
]

raw_dataset = pd.read_csv(
    url, names=column_names, na_values="?", comment="\t", sep=" ", skipinitialspace=True
)
dataset = raw_dataset.copy()
dataset = dataset.dropna()
dataset["Origin"] = dataset["Origin"].map({1: "USA", 2: "Europe", 3: "Japan"})
dataset = pd.get_dummies(dataset, prefix="", prefix_sep="")
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)
train_features = train_dataset.copy()
test_features = test_dataset.copy()
train_labels = train_features.pop("MPG")
test_labels = test_features.pop("MPG")
# %%
negloglik = lambda y, rv_y: -rv_y.log_prob(y)
# %%
horsepower = np.array(train_features["Horsepower"])
horsepower_normalizer = tf.keras.layers.experimental.preprocessing.Normalization(
    input_shape=[
        1,
    ]
)
horsepower_normalizer.adapt(horsepower)
# %%
standard_model = tf.keras.Sequential(
    [
        horsepower_normalizer,
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(units=1),
    ]
)
# %%
standard_model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.1), loss="mae")
history = standard_model.fit(
    train_features["Horsepower"],
    train_labels,
    epochs=100,
    verbose=0,
    validation_split=0.2,
)
# %%
x = tf.linspace(0.0, 250, 251)
y = standard_model.predict(x)
# %%
fig, ax = plt.subplots()
ax.scatter(x=train_features["Horsepower"], y=train_labels, s=1, c="blue", label="Data")
ax.plot(x, y, color="red", marker="", linestyle="dashed", linewidth=1)
plt.show()
# %%
prob_model = tf.keras.Sequential(
    [
        horsepower_normalizer,
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(1),
        tfp.layers.DistributionLambda(
            lambda t: tfp.distributions.Normal(loc=t, scale=1)
        ),
    ]
)
# %%
prob_model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.1), loss=negloglik)
history = prob_model.fit(
    train_features["Horsepower"],
    train_labels,
    epochs=100,
    verbose=0,
    validation_split=0.2,
)
# %%
x = tf.linspace(0.0, 250, 251)
y = prob_model(x)
# %%
fig, ax = plt.subplots()
ax.scatter(x=train_features["Horsepower"], y=train_labels, s=1, c="blue", label="Data")
ax.plot(x, y.mean(), color="red", marker="", linestyle="dashed", linewidth=1)
ax.plot(
    x,
    y.mean() + y.stddev(),
    color="red",
    marker="",
    linestyle="dashed",
    linewidth=1,
)
ax.plot(
    x,
    y.mean() - y.stddev(),
    color="red",
    marker="",
    linestyle="dashed",
    linewidth=1,
)

plt.show()
# %%
