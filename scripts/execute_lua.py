from pathlib import Path
from lupa import LuaRuntime

def run_files(lua_files: list[Path]):
    """
    Run multiple Lua files in order.

    Args:
        lua_files (list[Path]): A list of paths to Lua files to be executed.

    Raises:
        FileNotFoundError: If any of the specified Lua files do not exist.

    Returns:
        LuaRuntime: The Lua runtime instance after executing the files.
    """

    # create a Lua runtime
    lua = LuaRuntime(unpack_returned_tuples=True)

    # execute each file in order
    for lua_file in lua_files:
        if lua_file.exists():
            with open(lua_file, 'r', encoding='utf-8') as f:
                lua_code = f.read()
                lua.execute(lua_code)
            print(f"Loaded: {lua_file.name}")
        else:
            raise FileNotFoundError(f"File not found: {lua_file}")

    return lua


