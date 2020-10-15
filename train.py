import os
import pickle
from pathlib import Path
from azure.common.client_factory import get_client_from_cli_profile
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.resource import SubscriptionClient
from azure.storage.blob import BlobClient
import dvc.api
import git
import tensorflow as tf
import custom_modules as cm

print("Available GPUs: {}".format(tf.config.list_physical_devices("GPU")))

env_type = os.environ["ENV_TYPE"]
key_vault_name = os.environ["KEY_VAULT_NAME"]
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
secret_name = os.environ["SECRET_NAME"]

if env_type == "dev":
    print("This is a dev box")
    subscription_client = get_client_from_cli_profile(SubscriptionClient)

    credentials = DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True,
        exclude_visual_studio_code_credential=True,
        exclude_shared_token_cache_credential=True,
    )
    client = SecretClient(vault_url=key_vault_uri, credential=credentials)
    connection_string = client.get_secret(secret_name).value
else:
    print("This is not a dev box")

os.environ["AZURE_STORAGE_CONNECTION_STRING"] = connection_string

resource_url = dvc.api.get_url("data/dataset.csv", repo="./")
split_url = resource_url.split("/")
container = split_url[2]
blob = split_url[3] + "/" + split_url[4]

blob = BlobClient.from_connection_string(
    conn_str=connection_string, container_name=container, blob_name=blob
)

with open("./data/dataset.csv", "wb") as f:
    blob_data = blob.download_blob()
    blob_data.readinto(f)

repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

dataset_path = Path("./data/dataset.csv")
output_path = Path("./models/{}".format(sha))
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
