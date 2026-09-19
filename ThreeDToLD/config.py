import os
from platformdirs import PlatformDirs
import tomlkit

basedir = os.path.dirname(__file__)
dirs = PlatformDirs("3DToLD", "Nexusnui")
config_path = os.path.join(dirs.user_config_dir, "config.toml")


def loadconfig() -> (tomlkit.TOMLDocument, dict):
    warning_messages = {}
    config: tomlkit.TOMLDocument

    with open(os.path.join(basedir, "default_config.toml"), "r", encoding="utf-8") as source:
        default_config = tomlkit.load(source)
    if not os.path.exists(config_path):
        config = default_config
        try:
            if not os.path.exists(dirs.user_config_dir):
                os.makedirs(dirs.user_config_dir, exist_ok=True)
            with open(config_path, "w", encoding="utf-8") as source:
                tomlkit.dump(default_config, source)
        except (OSError, PermissionError) as e:
            warning_messages["Config not writable"] = f"Could not save config file at:\n{config_path}"
    else:
        try:
            with open(config_path, "r", encoding="utf-8") as source:
                config = tomlkit.load(source)
        except (OSError, PermissionError) as e:
            warning_messages["Config not readable"] = f"Could not read config file at:\n{config_path}"
            config = default_config
    # Todo: Validate Config, Update User Config

    return config, warning_messages
