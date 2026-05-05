import shutil
from pathlib import Path

from execute_lua import run_files
from find_game_path import get_lua_directory


LUA_DIR = get_lua_directory() / "shared/Translate/EN/ItemName.json"

OUT = Path("out/item_names.json")


# copy the file to the output
shutil.copy(LUA_DIR, OUT)