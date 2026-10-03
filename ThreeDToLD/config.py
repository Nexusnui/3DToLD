import os
from platformdirs import PlatformDirs
import tomlkit
import tomlkit.items
from ThreeDToLD.brick_data.colour_categories import colour_categories

__basedir__ = os.path.dirname(__file__)
__appdirs__ = PlatformDirs("3DToLD", "Nexusnui")
config_path = os.path.join(__appdirs__.user_config_dir, "config.toml")


def validate_value(key, value) -> bool:
    if isinstance(value, bool):
        return True
    if isinstance(value, int) or isinstance(value, float):
        if value <= 0:
            return False
    if key == "mode" and value not in ["System", "Dark", "Light"]:
        return False
    elif (key == "unit" and value not in
            ["Auto", "LDraw", "Micrometer", "Millimeter", "Centimeter", "Decimeter", "Meter", "Inch", "Foot"]):
        return False
    elif key == "default_colour_categories":
        for category in value:
            if category not in colour_categories:
                return False
    elif key == "model_path":
        return os.path.isdir(value)
    return True


def loadconfig(reset_config=False) -> (tomlkit.TOMLDocument, dict):
    warning_messages = {}
    config: tomlkit.TOMLDocument
    is_user_config = False
    update_user_config = False

    with open(os.path.join(__basedir__, "default_config.toml"), "r", encoding="utf-8") as source:
        default_config = tomlkit.load(source)
    if not os.path.exists(config_path) or reset_config:
        update_user_config = True
    else:
        try:
            with open(config_path, "r", encoding="utf-8") as source:
                config = tomlkit.load(source)
            is_user_config = True
        except (OSError, PermissionError) as e:
            warning_messages["Config not readable"] = f"Could not read config file at:\n{config_path}"
            config = default_config

    # Checks is config has to be updated/repaired
    if is_user_config:
        for category, values in default_config.items():
            if category not in default_config.keys():
                update_user_config = True
            else:
                for key, value in values.items():
                    if key not in config[category].keys():
                        update_user_config = True
                    else:
                        if type(value) is not type(config[category][key]):
                            update_user_config = True
                        else:
                            if type(value) is not tomlkit.items.Table:
                                if not validate_value(key, config[category][key]):
                                    update_user_config = True
                                elif value != config[category][key]:
                                    default_config[category][key] = config[category][key]
                            else:
                                for subkey, subvalue in value.items():
                                    if type(subvalue) is not type(config[category][key][subkey]):
                                        update_user_config = True
                                    else:
                                        if not validate_value(subvalue, config[category][key][subkey]):
                                            update_user_config = True
                                        elif subvalue != config[category][key][subkey]:
                                            default_config[category][key][subkey] = config[category][key][subkey]
    if update_user_config:
        if not save_config(default_config):
            warning_messages["Config not writable"] = f"Could not save config file at:\n{config_path}"
        config = default_config

    return config, warning_messages


def save_config(config: tomlkit.TOMLDocument) -> bool:
    try:
        if not os.path.exists(__appdirs__.user_config_dir):
            os.makedirs(__appdirs__.user_config_dir, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as source:
            tomlkit.dump(config, source)
    except (OSError, PermissionError) as e:
        return False
    return True


if __name__ == "__main__":
    testconfig, warnings = loadconfig()
    print("Test Config: ", testconfig)
    print("Warnings: ", warnings)
