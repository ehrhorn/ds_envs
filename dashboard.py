import os
from pathlib import Path
import pickle
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import SubscriptionClient
from azureml.core import Datastore
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication
import custom_modules as cm
import streamlit as st
import tensorflow as tf

cli_auth = AzureCliAuthentication()
subscription_client = get_client_from_cli_profile(SubscriptionClient)
subscription_id = next(subscription_client.subscriptions.list()).subscription_id

ws = Workspace(
    subscription_id=subscription_id,
    resource_group=os.environ["ML_RG"],
    workspace_name=os.environ["ML_WS"],
    auth=cli_auth,
)
datastore = Datastore.get(ws, datastore_name="ds_envs_datastore")

versions_path = Path("./outputs")
datastore.download(target_path=str(versions_path), prefix="runs")
runs_path = versions_path.joinpath("runs")

versions = [folder for folder in runs_path.iterdir() if folder.is_dir()]
chosen_version = st.sidebar.selectbox("Version", versions, format_func=lambda x: x.name)

runs = [folder for folder in chosen_version.iterdir() if folder.is_dir()]
chosen_run = st.sidebar.selectbox("Run", runs, format_func=lambda x: x.name)

model = tf.keras.models.load_model(chosen_run.joinpath("my_model"))
with open(chosen_run.joinpath("datasets.pkl"), "rb") as f:
    datasets = pickle.load(f)
with open(chosen_run.joinpath("raw_dataset.pkl"), "rb") as f:
    raw_dataset = pickle.load(f)
with open(chosen_run.joinpath("hist.pkl"), "rb") as f:
    history = pickle.load(f)

x = tf.linspace(0.0, 250, 251)
y = model.predict(x)
test_predictions = model.predict(datasets["test_features"]["Horsepower"]).flatten()

fig = cm.plot_loss(history)
st.pyplot(fig)
fig = cm.plot_distributions(raw_dataset)
st.pyplot(fig)
fig = cm.plot_horsepower(datasets, x, y)
st.pyplot(fig)
fig = cm.plot_errors(datasets, test_predictions)
st.pyplot(fig)
fig = cm.plot_residuals(test_predictions, datasets["test_labels"])
st.pyplot(fig)
