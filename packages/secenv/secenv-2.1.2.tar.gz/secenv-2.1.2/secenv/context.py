import sys
import concurrent.futures

import boto3

from . import config as config_lib
from .stores import read_secret
from .utils import escape

available_formats = ["dotenv", "shell", "github_actions"]


def gen_aws_assume_role(creds, stores):
    output = {}

    for k, v in creds.items():
        # raw values are passed directly
        if isinstance(v, str):
            continue
        # and values from stores are computed first
        args = {k2: v2 for k2, v2 in v.items() if k2 != "store" and v2}
        creds[k] = read_secret(stores[v["store"]], args)

    try:
        session = boto3.Session(aws_access_key_id=creds["key_id"], aws_secret_access_key=creds["secret_key"])

        sts_client = session.client("sts")
        assumed_role_object = sts_client.assume_role(RoleArn=creds["role"], RoleSessionName="AssumeRoleSession1")

        credentials = assumed_role_object["Credentials"]
        access_key_id = credentials["AccessKeyId"]
        secret_access_key = credentials["SecretAccessKey"]
        session_token = credentials["SessionToken"]

        output["AWS_ACCESS_KEY_ID"] = access_key_id
        output["AWS_SECRET_ACCESS_KEY"] = secret_access_key
        output["AWS_SESSION_TOKEN"] = session_token
    except Exception:
        print(f"AWS error: couldn't assume role '{creds['role']}'")
        sys.exit(1)

    sensitive_output = {}

    for key, value in output.items():
        sensitive_output[key] = {
            "value": value,
            "sensitive": True,
        }

    return sensitive_output


def format_output(context, format):
    output = []
    if format == "dotenv":
        for k, v in context.items():
            output.append(f"{k}={escape(v['value'])}")
        output = "\n".join(output)

    elif format == "shell":
        for k, v in context.items():
            output.append(f"export {k}={escape(v['value'])}")
        output = "\n".join(output)

    elif format == "github_actions":
        for k, v in context.items():
            # Here we have to handle the quotes in yet another way
            # as the 'echo' below add some too
            if isinstance(v, str):
                escaped = escape(v)
            else:
                escaped = escape(v["value"])

            if escaped[0] == "'":
                output.append(f"echo '{k}={escaped[1:-1]}' >> $GITHUB_ENV")
                if not isinstance(v, str) and v["sensitive"]:
                    output.append(f"echo '::add-mask::{escaped[1:-1]}'")
            elif escaped[0] == '"':
                output.append(f'echo "{k}={escaped[1:-1]}" >> $GITHUB_ENV')
                if not isinstance(v, str) and v["sensitive"]:
                    output.append(f'echo "::add-mask::{escaped[1:-1]}"')
        output = "\n".join(output)

    else:
        print(f"User error: format {format} not found, available: {available_formats}")
        sys.exit(1)

    return str(output)


def _handle_var(secret_name, secret_def, stores, output={}):
    if isinstance(secret_def, str):
        # raw value
        output[secret_name] = secret_def

    else:
        # retrieve from store
        store = secret_def["store"]
        if store not in stores:
            print(f"Config error: store '{store}' not found in config")
            sys.exit(1)

        secret_def = {k: v for k, v in secret_def.items() if k != "store" and v}
        res = read_secret(stores[store], secret_def)
        output[secret_name] = res


def is_sensitive(var_config):
    if "sensitive" in var_config:
        return var_config["sensitive"]
    else:
        return True


def gen_vars(vars, stores):
    output = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = [executor.submit(_handle_var, key, value, stores, output) for key, value in vars.items()]
        for future in concurrent.futures.as_completed(results):
            future.result()

    sensitive_output = {}

    for key, var_config in vars.items():
        sensitive_output[key] = {
            "value": output[key],
            "sensitive": is_sensitive(var_config),
        }

    return sensitive_output


def gen_context(name, stores):
    context_config = config_lib.config["contexts"][name]
    output = {}

    if context_config is None:
        print(f"Config error: context '{name}' is empty")
        sys.exit(1)

    if "extends" in context_config:
        for extended in context_config["extends"]:
            if extended not in config_lib.config["contexts"]:
                print(f"Config error: try to extend an unexistent context '{extended}'")
                sys.exit(1)
            if extended == name:
                print("Config error: can't extend a context with itself")
                sys.exit(1)
            extended_context = gen_context(extended, stores)
            output.update(extended_context)

    if "vars" in context_config:
        output.update(gen_vars(context_config["vars"], stores))

    if "aws_assume_role" in context_config:
        creds = {}
        creds["key_id"] = context_config["aws_assume_role"]["aws_access_key_id"]
        creds["secret_key"] = context_config["aws_assume_role"]["aws_secret_access_key"]
        creds["role"] = context_config["aws_assume_role"]["role_arn"]

        output.update(gen_aws_assume_role(creds, stores))

    return output


def list_contexts():
    return "\n".join(config_lib.config.get("contexts", ""))
