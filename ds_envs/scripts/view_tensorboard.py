from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import SubscriptionClient
from azureml.core import Experiment
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication
from azureml.tensorboard import Tensorboard

cli_auth = AzureCliAuthentication()
subscription_client = get_client_from_cli_profile(SubscriptionClient)
subscription_id = next(subscription_client.subscriptions.list()).subscription_id

ws = Workspace(
    subscription_id=subscription_id,
    resource_group="ds_envs_RG",
    workspace_name="ds_envs_ws",
    auth=cli_auth,
)
experiment_name = "my_experiment"
run_id = "my_experiment_1603471452_ed6739ca"
experiment = Experiment(workspace=ws, name=experiment_name)
run = [i for i in experiment.get_runs() if i.id == run_id][0]
tb = Tensorboard([run])
tb.start(start_browser=True)
input("Press Enter to continue...")
tb.stop()
