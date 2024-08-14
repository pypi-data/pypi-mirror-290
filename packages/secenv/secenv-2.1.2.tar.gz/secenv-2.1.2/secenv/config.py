import pathlib
import shutil
import yaml
import yaml.parser

from . import utils

config = {}
no_config_available = True
config_location = pathlib.Path(".secenv.yaml").resolve()


def load_config():
    global config, no_config_available, config_location
    possible_path = pathlib.Path(".").resolve()
    paths_to_scan = [possible_path]
    if utils.is_git_directory(possible_path):
        while not pathlib.Path(possible_path / ".git").is_dir():
            possible_path = (possible_path / "..").resolve()
            paths_to_scan.append(possible_path)

    for path in paths_to_scan:
        try:
            if pathlib.Path(path / ".secenv.yaml").exists():
                config = yaml.load(open(path / ".secenv.yaml", "r"), Loader=yaml.Loader)
                config_location = pathlib.Path(path / ".secenv.yaml").resolve()
                break
            elif pathlib.Path(path / ".secenv.yml").exists():
                config = yaml.load(open(path / ".secenv.yml", "r"), Loader=yaml.Loader)
                config_location = pathlib.Path(path / ".secenv.yml").resolve()
                break

        except yaml.parser.ParserError as e:
            print("Config error: config is not a valid YAML file:", e)
            return
    else:
        print("Config error: .secenv.yaml not found")

    if config:
        no_config_available = False
    else:
        print("Config error: file is empty")


def dump_config(destination: pathlib.Path = config_location):
    if destination.exists():
        print(f"Copied previous config into '{destination.name+'.bak'}'")
        shutil.copy(destination, destination.name + ".bak")

    with open(destination, "w") as f:
        yaml.dump(config, f)
        print(f"Successfully dumped config into '{f.name}'")


def validate_config():
    load_config()

    logs = []

    if "stores" not in config:
        config["stores"] = {}
    for name, obj in config["stores"].items():
        if "type" in obj and "extends" in obj:
            logs.append(f"Store '{name}' contains both 'type' and 'extends' keys")

        if "type" not in obj and "extends" not in obj:
            logs.append(f"Store '{name}' contains neither 'type' nor 'extends' keys")

        if "extends" in obj and obj["extends"] not in config["stores"]:
            logs.append(f"Store '{name}' extends an inexistent store '{obj['extends']}'")

    if "secrets" not in config:
        config["secrets"] = []
    for idx, obj in enumerate(config["secrets"]):
        if "store" not in obj:
            logs.append(f"Secret {idx} doesn't contain the 'store' key")
        if "secret" not in obj:
            logs.append(f"Secret {idx} doesn't contain the 'secret' key")
        if "store" in obj and obj["store"] not in config["stores"]:
            logs.append(f"Secret {idx} references an inexistent store '{obj['store']}'")
        if "generate" in obj and "type" not in obj["generate"]:
            logs.append(f"Secret {idx} generation doesn't have a type")

    if "contexts" not in config:
        config["contexts"] = {}
    for name, obj in config["contexts"].items():
        for extended in obj.get("extends", []):
            if extended not in config["contexts"]:
                logs.append(f"Context '{name}' extends an inexistent context '{extended}'")

        for var_name, var_obj in obj.get("vars", {}).items():
            if type(var_obj) is str:
                continue
            if "store" not in var_obj:
                logs.append(f"Secret '{name}/{var_name}' doesn't contain the 'store' key")
            if "store" in var_obj and var_obj["store"] not in config["stores"]:
                logs.append(f"Secret '{name}/{var_name}' references an inexistent store '{var_obj['store']}'")
            if "secret" not in var_obj:
                logs.append(f"Secret '{name}/{var_name}' doesn't contain the 'secret' key")
            if "key" in var_obj and type(var_obj["key"]) is not str:
                logs.append(
                    f"Secret '{name}/{var_name}' defines 'key' with wrong type '{type(var_obj['key'])}' (expects 'str')"
                )
            if "sensitive" in var_obj and type(var_obj["sensitive"]) is not bool:
                logs.append(
                    f"Secret '{name}/{var_name}' defines 'sensitive' with wrong type '{type(var_obj['sensitive'])}' (expects 'bool')"
                )

    return logs
