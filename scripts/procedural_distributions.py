import json, yaml
from pathlib import Path

from execute_lua import run_files


LUA_DIR = Path("/home/simon/.steam/debian-installation/steamapps/common/ProjectZomboid/projectzomboid/media/lua")
OUT = Path("out/procedural_distributions.json")

PROPERTIES_DATA = Path("data/procedural_distributions/properties.yaml")
with open(PROPERTIES_DATA) as f:
    PROPERTIES = yaml.safe_load(f)



# load files in dependency order
lua_files = [
    # requirements
    LUA_DIR / "server/Items/Distribution_BagsAndContainers.lua",
    LUA_DIR / "server/Vehicles/VehicleDistribution_SeatJunk.lua",

    # main distribution file
    LUA_DIR / "server/Items/ProceduralDistributions.lua",
]

lua = run_files(lua_files)

# access ProceduralDistributions
proc_dist = lua.globals()['ProceduralDistributions']

# for k, v in proc_dist['list'].items():
#     print(f"Distribution: {k}, Items: {len(v['items']) if 'items' in v else 'N/A'}")



procedural_distributions = proc_dist['list']

def parse_odd_pair(items):
    """
    Parse Lua tables with the following structure:
    ```lua
    {
        "val", chance,
        "val2", chance2,
        ...
    }
    ```
    """

    if items is None:
        return []

    d = []
    for i in range(1, len(items), 2):
        item: str = items[i]

        # all items are Base module. Best to use full type since some items use the full type while others don't
        # users of the data can easily chose which one to use by splitting by dot
        if not item.startswith("Base."):
            item = "Base." + item

        # there should always be a chance associated to the item right after it
        chance: float = items[i + 1]# if i + 1 < len(items) else None

        d.append((item, chance))
    return d

def parse_item_picker_container(data):
    o = {}
    for property in PROPERTIES:
        property_name = property["name"]
        if property_name in data:
            # should handle as an ItemPickerContainer ?
            if "ItemPickerContainer" in property and property["ItemPickerContainer"]:
                o[property_name] = parse_item_picker_container(data[property_name])
            elif property_name == "items":
                o[property_name] = parse_odd_pair(data[property_name])
            else:
                o[property_name] = data[property_name]
    return o

# convert to a regular dict for JSON serialization
def parse_procedural_distributions(lua_table):
    out = {}
    for procedural_distribution, data in lua_table.items():
        out[procedural_distribution] = parse_item_picker_container(data)

    return out


# convert the Lua table to a regular dict
procedural_distributions_dict = parse_procedural_distributions(procedural_distributions)

# save to JSON
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(procedural_distributions_dict, f, indent=4)