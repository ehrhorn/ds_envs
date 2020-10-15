import os
import pickle
from pathlib import Path
from azureml.core import Datastore
from azureml.core.run import Run
import dvc.api
import git
import tensorflow as tf
import custom_modules as cm

print("Available GPUs: {}".format(tf.config.list_physical_devices("GPU")))


run = Run.get_context()
ws = run.experiment.workspace

parser = argparse.ArgumentParser()
parser.add_argument("--con_str", type=str, help="Connection string")
args = parser.parse_args()

os.environ["AZURE_STORAGE_CONNECTION_STRING"] = args.con_str

run_id = run.get_details()["runId"]

datastore = Datastore.get(ws, datastore_name="ds_envs_datastore")

resource_url = dvc.api.get_url("data/dataset.csv", repo="./")
split_url = resource_url.split("/")
container = split_url[2]
prefix = split_url[3]
file = split_url[4]

datastore.download(target_path="./data", prefix=prefix)

repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

dataset_path = Path("./data").joinpath(prefix).joinpath(file)
output_path = Path("./outputs").joinpath("runs").joinpath(sha).joinpath(run_id)
output_path.mkdir(exist_ok=True, parents=True)

dataset = cm.read_dataset(dataset_path)
dataset = cm.clean_dataset(dataset)
raw_dataset = cm.one_hot_encode_dataset(dataset)
split_datasets = cm.split_dataset(raw_dataset)
datasets = cm.get_features(split_datasets)

normalizer = cm.create_normalizer(datasets)
model = cm.create_model(normalizer)

history = model.fit(
    datasets["train_features"]["Horsepower"],
    datasets["train_labels"],
    epochs=100,
    verbose=0,
    validation_split=0.2,
)

with open(output_path.joinpath("hist.pkl"), "wb") as f:
    pickle.dump(history.history, f)
with open(output_path.joinpath("datasets.pkl"), "wb") as f:
    pickle.dump(datasets, f)
with open(output_path.joinpath("raw_dataset.pkl"), "wb") as f:
    pickle.dump(raw_dataset, f)

model.save(output_path.joinpath("my_model"))

output_files = [str(f) for f in output_path.rglob("*") if f.is_file()]
print(output_files)
datastore.upload_files(output_files, target_path="runs/{}/{}".format(sha, run_id))
