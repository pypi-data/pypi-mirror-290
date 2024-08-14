from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError

from . import StoreInterface, cached, ask_secret, SecretNotFoundError, generate_secret


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name
        key_vault = super().get_from_config(name, "key_vault", infos)

        kv_url = f"https://{key_vault}.vault.azure.net"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=kv_url, credential=credential)

        self.client = client

    def gen_parser(self, parser):
        parser.add_argument("secret")

    @cached
    def read_secret(self, secret):
        try:
            res = self.client.get_secret(secret).value
        except ResourceNotFoundError:
            raise SecretNotFoundError(self.name, secret)
        return res

    def fill_secret(self, secret, generate=None, existing=None):
        if generate:
            secret_value = generate_secret(generate)
        else:
            secret_value = ask_secret(self.name, secret, existing=existing)
        self.client.set_secret(secret, secret_value)

    def list_secrets(self):
        ret = self.client.list_properties_of_secrets()
        return [s.name for s in ret]
