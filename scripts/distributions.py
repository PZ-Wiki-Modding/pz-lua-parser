import json, yaml
from pathlib import Path

from execute_lua import run_files


LUA_DIR = Path("/home/simon/.steam/debian-installation/steamapps/common/ProjectZomboid/projectzomboid/media/lua")
OUT = Path("out/distributions.json")
OUT_ROOMS = Path("out/rooms.json")

PROPERTIES_DATA = Path("data/distributions_room_properties.yaml")
with open(PROPERTIES_DATA) as f:
    PROPERTIES = yaml.safe_load(f)
    PROPERTIES = {
        k: v for k, v in PROPERTIES.items() if not v.get('isUseless', False)
    }

print(PROPERTIES)

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
    LUA_DIR / "server/Items/Distributions.lua",
]
lua = run_files(lua_files)

dist = lua.globals()['Distributions']
distrib_table = dist[1]

rooms = []
for room_name, data in distrib_table.items():
    # PZ is a bitch so they store fucking procedural distributions alongside room definitions
    # literally in the same table, what the fucking fuck ???
    if "rolls" in data:
        continue

    rooms.append(room_name)


# export rooms
with open(OUT_ROOMS, "w") as f:
    rooms.sort(key=str.lower)
    json.dump(rooms, f, indent=4)

