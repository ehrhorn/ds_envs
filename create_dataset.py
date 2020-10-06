from azure.common.client_factory import get_client_from_cli_profile
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient


subscription_client = get_client_from_cli_profile(SubscriptionClient)

subscription = next(subscription_client.subscriptions.list())
credentials = DefaultAzureCredential(
    exclude_environment_credential=True,
    exclude_managed_identity_credential=True,
    exclude_visual_studio_code_credential=True,
    exclude_shared_token_cache_credential=True,
)

resource_client = ResourceManagementClient(credentials, subscription.subscription_id)
storage_client = StorageManagementClient(credentials, subscription.subscription_id)

for item in storage_client.storage_accounts.list():
    print(item.name)
