import os

from azure.common.client_factory import get_client_from_cli_profile
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.keyvault.secrets import SecretClient

import pandas as pd
import tensorflow as tf

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
    retrieved_secret = client.get_secret(secret_name)
    print(retrieved_secret.value)
else:
    print("This is not a dev box")
