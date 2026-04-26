import os
from platformdirs import PlatformDirs

dirs = PlatformDirs("3DToLD", "Nexusnui", version="1.6.1")


def loadconfig() -> {}:
    if not os.path.exists(dirs.user_config_dir):
        print("path does not exists")

    return {}

loadconfig()


