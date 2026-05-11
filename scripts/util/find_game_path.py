"""
Utility script to find the Project Zomboid game installation path.
Supports Windows, Linux, and macOS with various Steam configurations.
"""

import os
from pathlib import Path

def get_game_directory() -> Path:
    """
    Get the path to the Project Zomboid game root directory.
    
    Returns:
        Path object pointing to the game root directory.
    
    Raises:
        FileNotFoundError: If Project Zomboid installation cannot be found.
    """
    pz_path_env = os.getenv('PZ_GAME_PATH')
    if not pz_path_env:
        raise FileNotFoundError(
            "PZ_GAME_PATH environment variable is not set. "
            "Please set the environment variable to path to the folder which contains the media directory."
        )
    if not Path(pz_path_env).is_dir():
        raise FileNotFoundError(
            f"PZ_GAME_PATH environment variable is set to '{pz_path_env}', but it is not a valid directory."
        )
    if not (Path(pz_path_env) / "media").is_dir():
        raise FileNotFoundError(
            f"PZ_GAME_PATH environment variable is set to '{pz_path_env}', but it does not contain a 'media' directory."
        )
    if not (Path(pz_path_env) / "media" / "lua").is_dir():
        raise FileNotFoundError(
            f"PZ_GAME_PATH environment variable is set to '{pz_path_env}', but it does not contain a 'media/lua' directory."
        )
    return Path(pz_path_env)


def get_lua_directory() -> Path:
    """
    Get the path to the Project Zomboid lua directory.
    
    Returns:
        Path object pointing to the lua directory.
    
    Raises:
        FileNotFoundError: If Project Zomboid installation cannot be found.
    """
    return get_game_directory() / "media" / "lua"


if __name__ == "__main__":
    try:
        lua_dir = get_lua_directory()
        print(f"Found Project Zomboid Lua directory: {lua_dir}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
