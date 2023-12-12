from shapely.geometry import Point, shape

from .continents import CONTINENTS

continents = CONTINENTS.copy()

for continent in continents:
    continents[continent] = shape(continents[continent])


def get_continent (x: float, y: float) -> str:

    point = Point(x, y)

    for name, continent in continents.items():
        if continent.contains(point):
            return name

    return "UNKNOWN"
