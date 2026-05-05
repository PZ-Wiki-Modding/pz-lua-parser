import json, yaml, lupa
from pathlib import Path
# from lupa import 

from execute_lua import run_files
from find_game_path import get_lua_directory


LUA_DIR = get_lua_directory()
OUT = Path("out/distributions.json")
OUT_ROOMS = Path("out/rooms.json")


# parsing those properties is useless, they do nothing, see the properties file for the details
# PROPERTIES_DATA = Path("data/ItemPickerRoom_properties.yaml")
# with open(PROPERTIES_DATA) as f:
#     PROPERTIES = yaml.safe_load(f)
#     PROPERTIES = [
#         v for v in PROPERTIES if not v.get('isUseless', False)
#     ]

PROPERTIES_DATA = Path("data/ItemPickerContainer_properties.yaml")
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
    LUA_DIR / "server/Items/Distributions.lua",
]
lua = run_files(lua_files)

dist = lua.globals()['Distributions']
distrib_table = dist[1]

rooms = []
rooms_distribution = {}
for room_name, room_data in distrib_table.items():
    # PZ is a bitch so they store fucking procedural distributions alongside room definitions
    # literally in the same table, what the fucking fuck ???
    if "rolls" in room_data:
        continue

    # store room name
    rooms.append(room_name)
    rooms_distribution[room_name] = {}

    for container_name, container_data in room_data.items():
        # if it isn't a table, then it's not a container def
        if not lupa.lua_type(container_data) == 'table':
            continue

        # check that it contains 'procedural'
        if not container_data['procedural']:
            continue

        procList = list(container_data['procList'].values())
        procList = [dict(item) for item in procList]
        for item in procList:
            for prop in PROPERTIES:
                val = item.get(prop['name'])
                if val is None:
                    continue
                t = prop.get('type', {})
                if t.get('main', None) == 'array':
                    item[prop['name']] = val.split(t.get('separator', ';'))
            print(item)

        rooms_distribution[room_name][container_name] = procList

    # parse container name


# export rooms
with open(OUT_ROOMS, "w") as f:
    rooms.sort(key=str.lower)
    json.dump(rooms, f, indent=4)

# export distributions
with open(OUT, "w") as f:
    json.dump(rooms_distribution, f, indent=4)