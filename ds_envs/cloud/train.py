import argparse
from azureml.core import Dataset
from azureml.core import Datastore
from azureml.core.run import Run
import matplotlib.pyplot as plt
import mlflow
import tensorflow as tf

import custom_modules as cm

print("Available GPUs: {}".format(tf.config.list_physical_devices("GPU")))

parser = argparse.ArgumentParser()
parser.add_argument("--version", type=int)
args = parser.parse_args()

run = Run.get_context()
ws = run.experiment.workspace

datastore = Datastore.get(ws, datastore_name="ds_envs_datastore")

dataset = Dataset.get_by_name(
    workspace=ws, name="fuel_efficiency", version=args.version
)
df = dataset.to_pandas_dataframe()

split_datasets = cm.split_dataset(df)
datasets = cm.get_features(split_datasets)

normalizer = cm.create_normalizer(datasets)
model = cm.create_model(normalizer)

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="./logs")

history = model.fit(
    datasets["train_features"]["Horsepower"],
    datasets["train_labels"],
    epochs=100,
    verbose=0,
    validation_split=0.2,
    callbacks=[tensorboard_callback],
)

print("Done!")

x = tf.linspace(0.0, 250, 251)
y = model.predict(x)
with mlflow.start_run():
    fig, ax = plt.subplots()
    ax.scatter(
        x=datasets["train_features"]["Horsepower"],
        y=datasets["train_labels"],
        s=1,
        c="blue",
        label="Data",
    )
    ax.plot(x, y, color="red", marker="", linestyle="dashed", linewidth=1)
    fig.savefig("regression.png")
    mlflow.log_artifact("regression.png")
    mlflow.log_metric("Training samples", len(datasets["train_features"]["Horsepower"]))
