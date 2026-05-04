import json
from pathlib import Path
from lupa import LuaRuntime

from execute_lua import run_files


LUA_DIR = Path("/home/simon/.steam/debian-installation/steamapps/common/ProjectZomboid/projectzomboid/media/lua")
OUT = Path("out/procedural_distributions.json")



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

# convert to a regular dict for JSON serialization
def parse_procedural_distributions(lua_table):
    out = {}
    for procedural_distribution, data in lua_table.items():
        out_data = {
            "rolls": data["rolls"],
        }

        out_data["items"] = parse_odd_pair(data["items"])
        
        out_junk = {}
        junk = data["junk"]
        if junk is not None:
            out_junk["items"] = parse_odd_pair(junk["items"])
            out_junk["rolls"] = junk["rolls"]

        out_data["junk"] = out_junk

        out[procedural_distribution] = out_data

    return out


# convert the Lua table to a regular dict
procedural_distributions_dict = parse_procedural_distributions(procedural_distributions)

# save to JSON
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(procedural_distributions_dict, f, indent=4)