"""
Some rooms from the RoomNames.txt from the official mapping tools are 
missing from the Distributions.lua which are the source for rooms.json

The RoomNames.txt file source is from the following repository branch:
https://github.com/timbaker/tiled/tree/basements

And its version is of the commit 1d08c3bed750226c2686c92114cc488c29465a60:
https://github.com/timbaker/tiled/commit/1d08c3bed750226c2686c92114cc488c29465a60
"""



import re, json

# find room names from RoomNames.txt
with open("checks/RoomNames.txt", "r") as file:
    content = file.read()

pattern = r"internal = (?P<room>\w+)"

matches = re.findall(pattern, content)

# check whenever a room is missing from rooms.json
with open("out/rooms.json", "r") as file:
    rooms = json.load(file)

for match in matches:
    # print(match)
    if match not in rooms:
        print(f"Room {match} not found in rooms.json")
