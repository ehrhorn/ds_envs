from azure.common.client_factory import get_client_from_cli_profile
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.resource import SubscriptionClient
from azure.storage.blob import BlobServiceClient
from azureml.core.authentication import AzureCliAuthentication
from azureml.core import Dataset
from azureml.core import Datastore
from azureml.core import Workspace
import pandas as pd

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

dataset = pd.read_csv(
    url, names=column_names, na_values="?", comment="\t", sep=" ", skipinitialspace=True
)
dataset = dataset.dropna()
dataset["Origin"] = dataset["Origin"].map({1: "USA", 2: "Europe", 3: "Japan"})
dataset = pd.get_dummies(dataset, prefix="", prefix_sep="")

small_dataset = dataset.loc[0:150, :]
small_dataset_csv = small_dataset.to_csv(path_or_buf=None, index=False)
dataset_csv = dataset.to_csv(path_or_buf=None, index=False)

container_name = "dsenvsblob"
key_vault_name = "meh-key-vault"
secret_name = "dsenvsstorage-con-str"
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
credentials = DefaultAzureCredential(exclude_interactive_browser_credential=False)
client = SecretClient(vault_url=key_vault_uri, credential=credentials)
connection_string = client.get_secret(secret_name).value

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

blob_client = blob_service_client.get_blob_client(
    container=container_name, blob="datasets/dataset_1.csv"
)
blob_client.upload_blob(small_dataset_csv)
blob_client = blob_service_client.get_blob_client(
    container=container_name, blob="datasets/dataset_2.csv"
)
blob_client.upload_blob(dataset_csv)

cli_auth = AzureCliAuthentication()
subscription_client = get_client_from_cli_profile(SubscriptionClient)
subscription_id = next(subscription_client.subscriptions.list()).subscription_id
ws = Workspace(
    subscription_id=subscription_id,
    resource_group="ds_envs_RG",
    workspace_name="ds_envs_ws",
    auth=cli_auth,
)
datastore = Datastore.get(ws, datastore_name="ds_envs_datastore")
datastore_paths = [
    (datastore, "datasets/dataset_1.csv"),
]
v1_dataset = Dataset.Tabular.from_delimited_files(path=datastore_paths)
v1_dataset.register(
    workspace=ws,
    name="fuel_efficiency",
    description="fuel efficiency data",
    create_new_version=True,
)
datastore_paths = [
    (datastore, "datasets/dataset_2.csv"),
]
v2_dataset = Dataset.Tabular.from_delimited_files(path=datastore_paths)
v2_dataset.register(
    workspace=ws,
    name="fuel_efficiency",
    description="fuel efficiency data",
    create_new_version=True,
)