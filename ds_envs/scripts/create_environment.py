from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import SubscriptionClient
from azureml.core import Environment
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication
from ds_envs.modules.utils import get_project_root

root_folder = get_project_root()

cli_auth = AzureCliAuthentication()
subscription_client = get_client_from_cli_profile(SubscriptionClient)
subscription_id = next(subscription_client.subscriptions.list()).subscription_id

ws = Workspace(
    subscription_id=subscription_id,
    resource_group="ds_envs_RG",
    workspace_name="ds_envs_ws",
    auth=cli_auth,
)

ds_envs_env = Environment.from_conda_specification(
    name="ds_envs", file_path=root_folder / "azureml_environment.yml"
)
ds_envs_env.docker.enabled = True
ds_envs_env.docker.base_image = (
    "mcr.microsoft.com/azureml/" "base-gpu:openmpi3.1.2-cuda10.1-cudnn7-ubuntu18.04"
)
ds_envs_env.register(workspace=ws)