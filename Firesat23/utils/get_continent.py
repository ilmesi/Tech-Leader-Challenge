import json
from shapely.geometry import Point, shape

continents = {}

with open("continents.json", "r") as file:
    continentsJson = json.load(file)

for continent in continents:
    continents[continent] = shape(continents[continent])


def get_continent (x: float, y: float) -> str:
    point = Point(x, y)

    for name, continent in continents.items():
        if continent.contains(point):
            return name

    return "UNKNOWN"
