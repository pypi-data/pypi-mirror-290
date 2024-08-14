import sys
import importlib
from . import config as config_lib


def find_stores():
    stores = {}
    if "stores" not in config_lib.config or not config_lib.config["stores"]:
        return stores

    for name in config_lib.config["stores"]:
        infos = config_lib.config["stores"][name]

        if "extends" in infos:
            extended = infos["extends"]
            if extended not in config_lib.config["stores"]:
                print("Config error: extended store does not exist:", extended)
                sys.exit(1)
            extended_infos = config_lib.config["stores"][extended]
            extended_infos.update(infos)
            infos = extended_infos

        try:
            store = importlib.import_module(f".stores.{infos['type']}", package="secenv")
        except ModuleNotFoundError:
            print(f"Config error: no store defined as '{infos['type']}'")
            sys.exit(1)
        stores[name] = store.Store(name, infos)

    return stores


def list_stores():
    return "\n".join(config_lib.config.get("stores", ""))
