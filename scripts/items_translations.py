import shutil
from pathlib import Path

from util.execute_lua import run_files
from util.find_game_path import get_lua_directory


LUA_DIR = get_lua_directory() / "shared/Translate/EN/ItemName.json"

OUT = Path("out/item_names.json")

# copy the file to the output
print(f"Copying {LUA_DIR} to {OUT}")
shutil.copy(LUA_DIR, OUT)