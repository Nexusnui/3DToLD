# This File is intended for updating the brick resource files:
# ThreeDToLD/brick_data/default_brick_resources.toml
# and
# ThreeDToLD/brick_data/bl_studio_brick_resources.toml
# (Paths are Windows based)
from ThreeDToLD.brick_data.brick_resources import get_brick_resources_from_ldconfig, save_brick_resources


def get_bl_studio_resources(definition_path, buid_date:str) -> dict:
    brick_resources = {
        "build_date": buid_date,
        "colours": {},
    }
    with open(definition_path, "r", encoding="utf-8") as source:
        source.readline()
        for line in source:
            values = line.split("\t")
            if values[0] != "":
                name = values[4].replace(" ", "_")
                code = f"100{values[3]}"
                rgb_values = values[8]
                # edge value for all bricklink colors is the one for black.
                # it would be better if it were generated based on the main color.
                edge_values = "#1B2A34"
                alpha = str(round(float(values[9]) * 255))
                category = f"Bricklink:{values[15].split("\n")[0]}"
                if not category in brick_resources["colours"].keys():
                    brick_resources["colours"][category] = []
                brick_resources["colours"][category].append((name, code, rgb_values, edge_values, alpha, "", "", ""))
        return brick_resources


if __name__ == "__main__":

    # Manually change date
    build_date = "2026-11-13"
    # This file is in your LDraw library folder
    ldraw_config = "Path/To/Your/LDConfig.ldr"
    brick_resources_path = f"{__file__.split("build-resources")[0]}ThreeDToLD\\brick_data"
    default_brick_resources = get_brick_resources_from_ldconfig(ldraw_config, build_date)
    save_brick_resources(default_brick_resources,brick_resources_path, "default_brick_resources.toml")

    bl_studio_custom_color_definition = "C:/Program Files/Studio 2.0/data/CustomColors/CustomColorDefinition.txt"

    bl_studio_resources = get_bl_studio_resources(bl_studio_custom_color_definition, build_date)
    save_brick_resources(bl_studio_resources, brick_resources_path, "bl_studio_brick_resources.toml")

