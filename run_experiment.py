import os
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import SubscriptionClient
from azureml.core import Environment
from azureml.core import Experiment
from azureml.core import ScriptRunConfig
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication

cli_auth = AzureCliAuthentication()
subscription_client = get_client_from_cli_profile(SubscriptionClient)
subscription_id = next(subscription_client.subscriptions.list()).subscription_id

ws = Workspace(
    subscription_id=subscription_id,
    resource_group="ds_envs_RG",
    workspace_name="ds_envs_ws",
    auth=cli_auth,
)
ds_envs_env = Environment("ds_envs")
ds_envs_env.docker.enabled = False
ds_envs_env.python.user_managed_dependencies = True
# ds_envs_env.docker.base_image = None
# ds_envs_env.docker.base_dockerfile = "./Dockerfile"
# ds_envs_env_registered = ds_envs_env.register(workspace=ws)
# build = ds_envs_env_registered.build_local(
#     workspace=ws, useDocker=True, pushImageToWorkspaceAcr=True
# )

src = ScriptRunConfig(
    source_directory="./",
    script="train.py",
    compute_target="local",
    environment=ds_envs_env,
)

# Set compute target
# Skip this if you are running on your local computer
# script_run_config.run_config.target = my_compute_target

experiment_name = "my_experiment"
experiment = Experiment(workspace=ws, name=experiment_name)

run = experiment.submit(config=src)
run.wait_for_completion(show_output=True)