import json
import sys
from . import (
    config as config_lib,
    utils,
)
from .stores import fill_secret


def handle_fill(stores, store, secret):
    # secenv secrets fill
    if "secrets" not in config_lib.config:
        print("Config error: 'secrets' block is not present")
        sys.exit(1)
    if not store and not secret:
        fill_secrets(stores)
    if store and not secret:
        if store not in stores:
            print(f"Usage error: store '{store}' not found")
            sys.exit(1)
        dict_with_one_store = {store: stores[store]}
        fill_secrets(dict_with_one_store)
    if store and secret:
        if store not in stores:
            print(f"Usage error: store '{store}' not found")
            sys.exit(1)
        for secret_obj in config_lib.config["secrets"]:
            if secret_obj["store"] != store or secret_obj["secret"] != secret:
                continue
            store = stores[secret_obj["store"]]
            secret = {k: v for k, v in secret_obj.items() if k not in ["store"]}
            fill_secret(store, secret)
            break
        else:
            print(f"Config error: secret {store}/{secret} not found")
            sys.exit(1)


def fill_secrets(stores):
    for secret_config in config_lib.config["secrets"]:
        if "secret" not in secret_config:
            print("Config error: a secret has no name")
            continue
        secret_name = secret_config["secret"]

        if "store" not in secret_config:
            print(f"Config error: 'store' not found in secret {secret_name}")
            sys.exit(1)

        if secret_config["store"] not in stores:
            print(f"Config error: store '{secret_config['store']}' not found")
            sys.exit(1)

        store = stores[secret_config["store"]]
        secret = {k: v for k, v in secret_config.items() if k not in ["store"]}
        fill_secret(store, secret)


def sync_secrets(stores):
    if "secrets" not in config_lib.config:
        config_lib.config["secrets"] = []

    for store_name, store_obj in stores.items():
        specified_secrets = {s["secret"]: s for s in config_lib.config["secrets"] if s["store"] == store_name}
        detected_secrets = store_obj.list_secrets()

        # check for secrets' existence
        for secret_name in detected_secrets:
            if secret_name not in specified_secrets:
                # secret is not defined in the config
                print(f"Secret filled but missing from configuration: {store_name}/{secret_name}")
                config_lib.config["secrets"].append({"secret": secret_name, "store": store_name})

        config_secrets_as_map = {s["secret"]: s for s in config_lib.config["secrets"] if s["store"] == store_name}

        # now they are sync-ed, check for the keys
        for secret_name in config_secrets_as_map:
            try:
                secret = store_obj.read_secret(secret_name)
                if not isinstance(secret, dict):
                    secret = json.loads(secret)
            except utils.SecretNotFoundError:
                print(f"Secret specified but not filled: {store_name}/{secret_name}")
                continue
            except json.JSONDecodeError:
                continue

            if not isinstance(secret, dict):
                # JSON will load '1' but it's not a map with actual keys
                continue

            specified_keys = set(config_secrets_as_map[secret_name].get("keys", []))
            detected_keys = set(secret.keys())
            detected_but_not_specified = list(detected_keys - specified_keys)
            specified_but_not_detected = list(specified_keys - detected_keys)

            if detected_but_not_specified:
                print(f"Detected but not specified keys for {store_name}/{secret_name}:", *detected_but_not_specified)
            if specified_but_not_detected:
                print(f"Specified but not detected keys for {store_name}/{secret_name}:", *specified_but_not_detected)

            config_secrets_as_map[secret_name]["keys"] = list(specified_keys | detected_keys)

    if utils.yes_no("Write config down?"):
        config_lib.dump_config()
