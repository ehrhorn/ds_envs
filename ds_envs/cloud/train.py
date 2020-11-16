import argparse
import os
import socket
from azureml.core import Dataset
from azureml.core import Datastore
from azureml.core.run import Run
import debugpy
import matplotlib.pyplot as plt
import mlflow
import tensorflow as tf

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import custom_modules as cm

print("Available GPUs: {}".format(tf.config.list_physical_devices("GPU")))

parser = argparse.ArgumentParser()
parser.add_argument("--version", type=int)
parser.add_argument("--remote_debug", action="store_true")
parser.add_argument(
    "--remote_debug_connection_timeout",
    type=int,
    default=300,
    help=f"Defines how much time the AML compute target "
    f"will await a connection from a debugger client (VSCODE).",
)
parser.add_argument(
    "--remote_debug_client_ip", type=str, help=f"Defines IP Address of VS Code client"
)
parser.add_argument(
    "--remote_debug_port",
    type=int,
    default=5678,
    help=f"Defines Port of VS Code client",
)
args = parser.parse_args()

run = Run.get_context()

if args.remote_debug:
    print(f"Timeout for debug connection: {args.remote_debug_connection_timeout}")
    try:
        ip = args.remote_debug_client_ip
    except Exception:
        print("Need to supply IP address for VS Code client")
    ip = socket.gethostbyname(socket.gethostname())
    print(f"ip_address: {ip}")
    debugpy.listen(address=(ip, args.remote_debug_port))
    debugpy.wait_for_client()
    print(f"Debugger attached = {debugpy.is_client_connected()}")


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
