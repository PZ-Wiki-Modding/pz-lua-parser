import json, yaml
from pathlib import Path

from execute_lua import run_files


LUA_DIR = Path("/home/simon/.steam/debian-installation/steamapps/common/ProjectZomboid/projectzomboid/media/lua")
OUT = Path("out/procedural_distributions.json")

PROPERTIES_DATA = Path("data/procedural_distributions_properties.yaml")
with open(PROPERTIES_DATA) as f:
    PROPERTIES = yaml.safe_load(f)



# load files in dependency order
lua_files = [
    # requirements
    LUA_DIR / "server/Items/Distribution_BagsAndContainers.lua",
    LUA_DIR / "server/Items/Distribution_BinJunk.lua",
    LUA_DIR / "server/Items/Distribution_ClosetJunk.lua",
    LUA_DIR / "server/Items/Distribution_CounterJunk.lua",
    LUA_DIR / "server/Items/Distribution_DeskJunk.lua",
    LUA_DIR / "server/Items/Distribution_ShelfJunk.lua",
    LUA_DIR / "server/Items/Distribution_SideTableJunk.lua",
    
    LUA_DIR / "server/Vehicles/VehicleDistribution_SeatJunk.lua",
    LUA_DIR / "server/Vehicles/VehicleDistribution_GloveBoxJunk.lua",
    LUA_DIR / "server/Vehicles/VehicleDistribution_TrunkJunk.lua",

    # main distribution file
    LUA_DIR / "server/Items/ProceduralDistributions.lua",
]
lua = run_files(lua_files)

# access ProceduralDistributions
proc_dist = lua.globals()['ProceduralDistributions']
procedural_distributions = proc_dist['list']



def parse_odd_pair_table(items):
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

            # parse odd pair table
            elif property_name == "items":
                o[property_name] = parse_odd_pair_table(data[property_name])

            # otherwise just copy the value
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