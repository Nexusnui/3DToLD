import re
from enum import Enum
import tomlkit
import os


class ConfigSection(Enum):
    HEADER = 0
    COLOURS = 1
    AVATARS = 2


def get_brick_resources_from_ldconfig(ldconfig_path, build_date: str = "")-> tuple[str, list[tuple],list[str], list[str]]:
    current_section = ConfigSection.HEADER
    brick_resources={
        "build_date": build_date,
        "config_update":"",
        "colours":{},
        "brick_categories":[],
    }
    with open(ldconfig_path, "r", encoding="utf-8") as source:
        additional_info = ""
        current_category = ""
        for line in source:
            if current_section == ConfigSection.HEADER:
                if line.startswith("0 !LDRAW_ORG Configuration UPDATE "):
                    brick_resources["config_update"] = line.split(" ")[-1].strip("\n")
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
