from azure.common.client_factory import get_client_from_cli_profile
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient

subscription_client = get_client_from_cli_profile(SubscriptionClient)

subscription = next(subscription_client.subscriptions.list())
print(dir(subscription))

credential = DefaultAzureCredential()
