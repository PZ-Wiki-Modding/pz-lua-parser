# PZ Lua Parser
Parse the Project Zomboid Lua game files to extract information about various elements.

## Usage
To use the parser, you first need to set an environment variable `PZ_GAME_PATH` that points to the root directory of your Project Zomboid installation. For example:
```bash
PZ_GAME_PATH=/home/simon/.steam/debian-installation/steamapps/common/ProjectZomboid
```

For Linux, this needs to be the path pointing to the `projectzomboid.sh` file (double parent to `media`). For Windows, it should point to the `ProjectZomboid64.exe` file (parent to `media`).
