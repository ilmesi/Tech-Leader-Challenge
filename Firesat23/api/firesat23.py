import random
from datetime import datetime, timedelta

cache: str = ""

def generate_random_coordinates():
  y = random.uniform(-90, 90)
  x = random.uniform(-180, 180)
  return x, y

def generate_random_datetime():
  yesterday = datetime.utcnow() - timedelta(days=1)
  random_seconds = random.randint(0, 86400)
  return yesterday + timedelta(seconds=random_seconds)

def get_wildfires_last_24_hours() -> str:
  global cache

  if (len(cache) > 0): return cache
  wildfires = []

  for _ in range(random.randint(5000, 6000)):
    x, y = generate_random_coordinates()
    date = generate_random_datetime().strftime('%Y-%m-%dT%H:%M:%S+00:00')

    wildfire = {
      "date": date,
      "conf": random.randint(1, 100),
      "x": round(x, 6),
      "y": round(y, 6)
    }
    wildfires.append(wildfire)

  csv_string = ""
  csv_headers = wildfires[0].keys()
  csv_string += ','.join(csv_headers) + '\n'
  for wildfire in wildfires:
    csv_string += ','.join(str(wildfire[key]) for key in csv_headers) + '\n'

  cache = csv_string
  return csv_string