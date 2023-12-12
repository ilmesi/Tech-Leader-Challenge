from decimal import Decimal
from datetime import date

from utils.get_continent import get_continent

class Fire:

    def __init__(self, fire_date: date, conf: int, x: Decimal, y: Decimal, sat: str = 'noaa-goes16'):
        self.fire_date = fire_date
        self.conf = conf
        self.x = Decimal(x)
        self.y = Decimal(y)
        self.id = f'{self.fire_date}+{self.x:0.2f}+{self.y:0.2f}'
        self.continent = get_continent(self.x, self.y)
        self.sat = sat

    def __dict__(self):
        return {
            'continent_date': f'{self.continent}_{self.fire_date:%Y-%m-%dT%H}',
            'id': self.id,
            'conf': self.conf,
            'sat': self.sat,
            'x': self.x,
            'y': self.y,
        }