from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import SubscriptionClient
from azureml.core import Environment
from azureml.core import Experiment
from azureml.core import ScriptRunConfig
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication
from ds_envs.modules.utils import get_project_root

cli_auth = AzureCliAuthentication()
subscription_client = get_client_from_cli_profile(SubscriptionClient)
subscription_id = next(subscription_client.subscriptions.list()).subscription_id

ws = Workspace(
    subscription_id=subscription_id,
    resource_group="ds_envs_RG",
    workspace_name="ds_envs_ws",
    auth=cli_auth,
)

env = Environment.get(workspace=ws, name="ds_envs")

src = ScriptRunConfig(
    source_directory=get_project_root() / "ds_envs" / "cloud",
    script="train.py",
    arguments=["--version", 1],
    compute_target="cpu",
    environment=env,
)

experiment_name = "my_experiment"
experiment = Experiment(workspace=ws, name=experiment_name)

run = experiment.submit(config=src)

run.wait_for_completion(show_output=True)