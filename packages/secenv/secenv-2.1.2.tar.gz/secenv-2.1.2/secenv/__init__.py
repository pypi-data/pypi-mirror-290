#!/usr/bin/env python

import argparse
import importlib
import importlib.metadata
import pathlib
import sys
from typing import Dict, List

from . import (
    config as config_lib,
    context as context_lib,
    secrets as secrets_lib,
    store as store_lib,
)
from .stores import StoreInterface, read_secret


VERSION = importlib.metadata.version("secenv")


def load_config():
    """
    Load the configuration file and converts it from YAML to a Python object.
    If it's in a Git repository, look up to root directory, otherwise current directory only.
    """
    return config_lib.load_config()


def dump_config(destination: pathlib.Path = config_lib.config_location):
    """
    Dump the currently loaded configuration into a YAML file.
    """
    return config_lib.dump_config(destination)


def find_stores() -> Dict[str, StoreInterface]:
    """
    Find the stores defined in the configuration object.
    For each found store, instantiate it based on its type.

    Returns:
        Dict[str, StoreInterface]: A dictionary where the keys are the name of the
            stores and the keys are the StoreInterface instantiations

    Raises:
        SystemExit: If the configuration is not valid
    """
    return store_lib.find_stores()


def sync_secrets(stores: Dict[str, StoreInterface]) -> None:
    """
    Sync the secrets defined in the configuration object and the ones already existing in the stores.

    Args:
        stores (Dict[str, StoreInterface]): A dictionary where the keys are the name of
            the stores and the keys are the StoreInterface instantiations
    """
    return secrets_lib.sync_secrets(stores)


def fill_secrets(stores: Dict[str, StoreInterface]) -> None:
    """
    Fill the secrets defined in the configuration object.

    Args:
        stores (Dict[str, StoreInterface]): A dictionary where the keys are the name of
            the stores and the keys are the StoreInterface instantiations
    """
    return secrets_lib.fill_secrets(stores)


def gen_context(name: str, stores: Dict[str, StoreInterface]) -> Dict[str, str]:
    """
    Generate the context specified in the configuration object.

    Args:
        name (str): Name of the context to generate
        stores (Dict[str, StoreInterface]): A dictionary where the keys are the name of
            the stores and the keys are the StoreInterface instantiations

    Returns:
        Dict[str, str]: A dictionary of variables with their associated values

    Raises:
        SystemExit: If the configuration is not valid
    """
    return context_lib.gen_context(name, stores)


def list_stores() -> str:
    """
    List the stores specified in the configuration object.

    Returns:
        str: List of the stores separated by newlines
    """
    return store_lib.list_stores()


def list_contexts() -> str:
    """
    List the contexts specified in the configuration object.

    Returns:
        str: List of contexts separated by newlines
    """
    return context_lib.list_contexts()


def validate_config() -> List[str]:
    """
    Validate a configuration file.

    Returns:
        List[str]: List of found errors
    """
    return config_lib.validate_config()


def gen_parser(stores: Dict[str, StoreInterface]) -> argparse.ArgumentParser:
    """
    Parse the arguments provided to the program.

    Args:
        stores (Dict[str, StoreInterface]): A dictionary where the keys are the name of
            the store and the keys are the StoreInterface instantiations

    Returns:
        argparse.ArgumentParser: A parser ready to being consumed by the application
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # secenv version
    subparsers.add_parser("version", help="get secenv version")

    # secenv validate
    subparsers.add_parser("validate", help="validate secenv config")

    # secenv stores
    subparsers.add_parser("stores", help="list the available stores")

    # secenv secrets {fill, get} STORE SECRET [KEY]
    # subparsers_group.add_parser("secrets", help="fill secrets in the stores")
    secrets_parser = subparsers.add_parser("secrets", help="manage secrets in the stores")
    secrets_subparsers = secrets_parser.add_subparsers(dest="secrets_command")
    secrets_get_parser = secrets_subparsers.add_parser("get", help="get secrets in the stores")
    secrets_get_subparser = secrets_get_parser.add_subparsers(dest="secrets_get_store")

    secrets_fill_parser = secrets_subparsers.add_parser("fill", help="fill secrets in the stores")
    secrets_fill_parser.add_argument("store", help="the store to fill the secret in", nargs="?")
    secrets_fill_parser.add_argument("secret", help="the secret to fill", nargs="?")

    for store in stores:
        if "extends" in config_lib.config["stores"][store]:
            extended = config_lib.config["stores"][store]["extends"]
            type = config_lib.config["stores"][extended]["type"]
        else:
            type = config_lib.config["stores"][store]["type"]
        store_subparser = secrets_get_subparser.add_parser(
            store,
            help=f"query store '{store}' of type '{type}'",
        )
        stores[store].gen_parser(store_subparser)

    # secenv contexts list
    # secenv contexts gen CONTEXT
    contexts_parser = subparsers.add_parser("contexts", help="manage available contexts")
    contexts_subparsers = contexts_parser.add_subparsers(dest="contexts_command")
    contexts_subparsers.add_parser("list", help="list contexts")
    contexts_gen_subparsers = contexts_subparsers.add_parser("gen", help="generate an environment based on a context")
    contexts_gen_subparsers.add_argument("context")
    contexts_gen_subparsers.add_argument(
        "-o",
        "--output-format",
        choices=context_lib.available_formats,
        default="shell",
        dest="format",
        help="output format",
    )

    # secenv sync
    sync_parser = subparsers.add_parser("sync", help="sync the defined and existing secrets")
    sync_parser.add_argument("store", help="the store to sync the secret in", nargs="?")
    sync_parser.add_argument("secret", help="the secret to sync", nargs="?")

    return parser


def main():
    if len(sys.argv) == 2 and "version" == sys.argv[1]:
        # secenv version
        print(f"secenv version {VERSION}")
        sys.exit(0)

    config_lib.load_config()
    stores = {} if config_lib.no_config_available else find_stores()

    # Listing subparsers from an `argparse.ArgumentParser` is not straightforward
    # because the standard library doesn't provide a direct method to retrieve them.
    # However, one can access them indirectly by inspecting the parser's internal structures.
    #
    # The iterator is to cast it from `Iterable[any]` to a more typing-friendly value.
    #
    # It's safe to ignore the type warning as `choices` is actually a `dict`.
    parser = gen_parser(stores)
    subparsers: Dict[str, argparse.ArgumentParser] = {k: v for k, v in parser._actions[1].choices.items()}  # type: ignore

    args = parser.parse_args()

    if len(sys.argv) == 1:
        # secenv
        parser.print_help()
        return

    elif args.command == "stores":
        print(list_stores())
        return

    elif args.command == "secrets":
        if not args.secrets_command:
            # secenv secrets
            subparsers["secrets"].print_help()

        if args.secrets_command == "fill":
            # secenv secrets fill
            secrets_lib.handle_fill(stores, args.store, args.secret)

        if args.secrets_command == "get":
            # secenv secrets get
            try:
                store_obj = stores[args.secrets_get_store]
            except KeyError:
                # Same technique as above with the subparsers
                subparsers["secrets"]._actions[1].choices["get"].print_help()  # type: ignore
                return

            unwanted_args_for_query = ["type", "command", "secrets_get_store", "secrets_command"]
            args = {k: v for k, v in vars(args).items() if k not in unwanted_args_for_query and v}
            result = read_secret(store_obj, args)
            print(result)

        return

    elif args.command == "contexts":
        if not args.contexts_command:
            # secenv contexts
            subparsers["contexts"].print_help()
            return

        if args.contexts_command == "list":
            # secenv contexts list
            if contexts := list_contexts():
                print(contexts)
            else:
                print("No contexts defined")
            return

        if args.contexts_command == "gen":
            # secenv contexts gen
            context_name = args.context
            if "contexts" not in config_lib.config or context_name not in config_lib.config["contexts"]:
                print(f"Config error: context '{context_name}' not found")
                print("Run `secenv contexts list` first")
                sys.exit(1)
            ctx = gen_context(context_name, stores)
            print(context_lib.format_output(ctx, args.format))
            return

    elif args.command == "validate":
        # secenv validate
        errors = validate_config()
        if not errors:
            print("Configuration valid!")
        else:
            print("\n".join(errors))
        return

    elif args.command == "sync":
        # secenv sync
        if not args.store and not args.secret:
            sync_secrets(stores)
        if args.store and not args.secret:
            if args.store not in list_stores():
                print(f"Usage error: store '{args.store}' not found")
                sys.exit(1)
            dict_with_one_store = {args.store: stores[args.store]}
            sync_secrets(dict_with_one_store)
        # TODO: sync just one secret
        # if args.store and args.secret:
        #     if args.store not in list_stores():
        #         print(f"Usage error: store '{args.store}' not found")
        #         sys.exit(1)
        #     for secret_obj in config["secrets"]:
        #         if secret_obj["store"] != args.store or secret_obj["secret"] != args.secret:
        #             continue
        #         generate_obj = utils.SecretType.from_config(secret_obj["generate"])
        #         stores[secret_obj["store"]].sync_secret(secret_obj["secret"], generate_obj)
        #         break
        #     else:
        #         print(f"Config error: secret {args.store}/{args.secret} not found")
        #         sys.exit(1)

        return

    parser.print_help()
    parser.exit()
