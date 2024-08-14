import passpy
from . import StoreInterface, cached, ask_secret, SecretNotFoundError, generate_secret


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name
        directory = super().get_from_config(name, "directory", infos, default="~/.password-store")
        self.store = passpy.Store(store_dir=directory, gpg_bin="gpg")
        # gpg_bin defaults to `gpg2` which is now commonly deployed

    def gen_parser(self, parser):
        parser.add_argument("secret")

    @cached
    def read_secret(self, secret):
        res = self.store.get_key(secret)
        if res:
            return res
        else:
            raise SecretNotFoundError(self.name, secret)

    def fill_secret(self, secret, generate=None, existing=None):
        if generate:
            secret_value = generate_secret(generate)
        else:
            secret_value = ask_secret(self.name, secret, existing=existing)
        self.store.set_key(secret, secret_value, force=True)

    def list_secrets(self):
        return self.store.find("")
