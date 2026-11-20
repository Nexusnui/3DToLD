import re
from enum import Enum

import tomlkit
import os
from platformdirs import PlatformDirs
from importlib import resources
import datetime
import requests
__appdirs__ = PlatformDirs("3DToLD", "Nexusnui")
__user_brick_resources_path = __appdirs__.user_data_dir
__user_brick_resources_filename = "brick_resources.toml"
user_brick_resources_filepath = os.path.join(__user_brick_resources_path, __user_brick_resources_filename)

__initialised = False
__ldraw_resources: tomlkit.TOMLDocument
__bl_studio_resources: tomlkit.TOMLDocument

def init():
    global __initialised
    if not __initialised:
        load_resources()
        __initialised = True

def load_resources():
    global __initialised
    if not __initialised:
        global __bl_studio_resources
        bl_studio_resources_reference = resources.files("ThreeDToLD.brick_data") / "bl_studio_brick_resources.toml"
        with bl_studio_resources_reference.open(mode="r", encoding="utf-8") as source:
            __bl_studio_resources = tomlkit.load(source)
    global __ldraw_resources
    ldraw_resources_reference = resources.files("ThreeDToLD.brick_data") / "default_brick_resources.toml"
    with ldraw_resources_reference.open(mode="r", encoding="utf-8") as source:
        __ldraw_resources = tomlkit.load(source)
    if os.path.exists(user_brick_resources_filepath):
        with open(user_brick_resources_filepath, "r", encoding="utf-8") as source:
            user_brick_resources = tomlkit.load(source)
        if user_brick_resources["build_date"] > __ldraw_resources["build_date"]:
            __ldraw_resources = user_brick_resources


class ConfigSection(Enum):
    HEADER = 0
    COLOURS = 1
    AVATARS = 2


def get_brick_resources_from_ldconfig(ldconfig: str | requests.models.Response)-> tuple[str, list[tuple],list[str], list[str]]:
    current_section = ConfigSection.HEADER
    build_date = datetime.date.today()
    brick_resources={
        "build_date": build_date,
        "config_update":"",
        "colours":{},
        "brick_categories":[],
    }
    with ConfigReader(ldconfig) as source:
        additional_info = ""
        current_category = ""
        for line in source:
            if current_section == ConfigSection.HEADER:
                if line.startswith("0 !LDRAW_ORG Configuration UPDATE "):
                    date_str: str = line.split(" ")[-1].strip("\n")
                    brick_resources["config_update"] = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                if line == "0 // Colour definitions\n":
                    current_section = ConfigSection.COLOURS

            elif current_section == ConfigSection.COLOURS:
                if line.startswith("0 !COLOUR "):
                    name, code, value, edge = re.search(r"0 !COLOUR (\S*)\s+CODE\s+(\S*)\s+"
                                                        r"VALUE\s+(\S*)\s+EDGE\s+(\S*)\s+", line).groups()
                    str_match = re.search(r"ALPHA\s*([0-9]*)", line)
                    alpha = "255" if str_match is None else str_match.group(1)
                    str_match = re.search(r"LUMINANCE\s*([0-9]*)", line)
                    luminance = "" if str_match is None else str_match.group(1)
                    str_match = re.search(r"\s+(CHROME|PEARLESCENT|METAL|RUBBER|RUBBER|MATTE_METALLIC|"
                                          r"MATERIAL\s+.+)$", line)
                    material = "" if str_match is None else str_match.group(1)
                    if (str_match := re.search(r"LEGOID\s+(.*)\s+-\s+(.*)", additional_info)) is not None:
                        lego_ids, lego_names = str_match.groups()
                    elif (str_match := re.search(r"(MODULEXID\s+.*)\s+-\s+(.*)", additional_info)) is not None:
                        lego_ids, lego_names = str_match.groups()
                    elif (str_match := re.search(r"LEGO\s+-\s+(.*)", additional_info)) is not None:
                        lego_names = str_match.group(1)
                        lego_ids = ""

                    elif additional_info == "LEGO Gr.Metal / BricksetID 910 - Metallic Green":
                        lego_ids = "BricksetID 910"
                        lego_names = "Gr.Metal / Metallic Green"
                    elif additional_info == "BricksetID 911 - Metallic Pink (Clikits)":
                        lego_ids = "BricksetID 911"
                        lego_names = "Metallic Pink (Clikits)"
                    elif additional_info == "(Mx Very Light Bluish Gray for Printed Plancopy Tiles)":
                        lego_ids = ""
                        lego_names = "Mx Very Light Bluish Gray for Printed Plancopy Tiles"
                    elif additional_info != "":
                        lego_names = additional_info
                        lego_ids = ""
                    else:
                        lego_ids = ""
                        lego_names = ""
                    if not current_category in brick_resources["colours"].keys():
                        brick_resources["colours"][current_category] = []
                    brick_resources["colours"][current_category].append((name, code, value, edge, alpha, luminance, material,
                                          lego_ids, lego_names))
                elif line == "0 // Avatar definitions\n":
                    current_section = ConfigSection.AVATARS
                elif (str_match := re.search(r"0 // (\S.*)", line)) is not None:
                    current_category = str_match.group(1)
                    additional_info = ""
                elif (str_match := re.search(r"0 \s+// (\S.*)", line)) is not None:
                    additional_info = str_match.group(1)

            elif current_section == ConfigSection.AVATARS:
                if (str_match := re.search(r'0 !AVATAR CATEGORY "(.*)" DESCRIPTION', line)) is not None:
                    brick_resources["brick_categories"].append(str_match.group(1))
    return brick_resources

def save_brick_resources(brick_resources: tomlkit.TOMLDocument | dict, path, filename) -> bool:
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, filename), "w", encoding="utf-8") as source:
            tomlkit.dump(brick_resources, source)
    except (OSError, PermissionError) as e:
        return False
    return True

def update_brick_resources(path= __user_brick_resources_path, filename = __user_brick_resources_filename, force = False):
    init()
    config_url = "https://library.ldraw.org/library/official/LDConfig.ldr?app=3DToLD"
    global  __ldraw_resources
    update_resources = force
    yield "Start Downloading LDConfig from ldraw.org..."
    response = requests.get(config_url)
    if response.status_code == 200:
        yield "Processing LDConfig Content..."
        new_brick_resources = get_brick_resources_from_ldconfig(response)
        if new_brick_resources["config_update"] > __ldraw_resources["build_date"]:
            update_resources = True
            yield "Build date of current Brick Resources is older than LDConfig..."
        elif new_brick_resources["config_update"] >= __ldraw_resources["config_update"]:
            if len(new_brick_resources["brick_categories"]) != len(__ldraw_resources["brick_categories"]):
                update_resources = True
                yield "Brick Categories changed in LDConfig..."
            if len(new_brick_resources["colours"].keys()) != len(__ldraw_resources["colours"].keys()):
                update_resources = True
                yield "Colour Categories changed in LDConfig..."
            if not update_resources:
                for category in new_brick_resources["colours"].keys():
                    if not category in __ldraw_resources["colours"].keys():
                        update_resources = True
                        yield "New/Renamed colour category in LDConfig..."
                        break
                    new_colour = False
                    if len(new_brick_resources["colours"][category]) != len(__ldraw_resources["colours"][category]):
                        update_resources = True
                        yield "Colours changed in LDConfig..."
                        break
                    else:
                        for colour_index, colour in enumerate(new_brick_resources["colours"][category]):
                            for value_index, value in enumerate(colour):
                                if value != __ldraw_resources["colours"][category][colour_index][value_index]:
                                    update_resources = True
                                    yield "New/Changed colour in LDConfig..."
                                    new_colour = True
                                    break
                    if new_colour:
                        break
    else:
        yield f"LDConfig failed with response code: {response.status_code}..."
        return
    if update_resources:
        yield f"Save Brick Resources..."
        if save_brick_resources(new_brick_resources, path, filename):
            load_resources()
            yield "Brick Resources updated successfully..."
        else:
            yield "Failed to save Brick Resources..."
    else:
        yield "Brick resources are already up to date..."



def get_brick_categories() -> list:
    init()
    return __ldraw_resources["brick_categories"].copy()

def get_brick_colours() -> dict:
    init()
    return __ldraw_resources["colours"] | __bl_studio_resources["colours"]

def get_colour_categories() -> list:
    init()
    colour_categories = []
    colour_categories.extend(__ldraw_resources["colours"].keys())
    colour_categories.extend(__bl_studio_resources["colours"].keys())
    return colour_categories

def get_update_date():
    init()
    return __ldraw_resources["build_date"]


class ConfigReader:
    def __init__(self, config: str | requests.models.Response):
        self.is_request_reader = isinstance(config, requests.models.Response)

        self._config = config

    def __enter__(self):
        if self.is_request_reader:
            self._lines = iter(self._config.text.splitlines(True))
        else:
            self._reader = open(file=self._config, mode="r", encoding="utf-8")
        return self

    def __exit__(self, *args):
        if not self.is_request_reader:
            self._reader.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.is_request_reader:
            return next(iter(self._lines))
        else:
            return next(self._reader)
