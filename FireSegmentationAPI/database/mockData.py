import boto3
import random
from decimal import Decimal
from datetime import datetime, timedelta


def generate_random_datetime():
  start_date = datetime(2023, 1, 1)
  end_date = datetime(2023, 6, 30)
  random_delta = timedelta(days=random.randint(0, (end_date - start_date).days),
                              hours=random.randint(0, 23),
                              minutes=random.randint(0, 59))
  random_datetime = start_date + random_delta
  return random_datetime.isoformat()


def generate_random_record():
  random_date = generate_random_datetime()
  
  latitude = round(random.uniform(-90.00, 90.00), 6)
  longitude = round(random.uniform(-180.00, 180.00), 6)

  example_item = {
    "date": random_date[:-6], # Fecha con formato ISO 8601 cortada hasta la hora
    "id": f"{random_date}+{latitude:.2f}+{longitude:.2f}", # Es el ISO 8601 + latitud + longitud con aproximación de dos dígitos (con signo - si es negativo)
    "conf": random.randint(1, 100), # Es la confianza de la detección
    "sat": "Firesat23", # Satélite
    "x": Decimal(str(longitude)), # Coordenada x
    "y": Decimal(str(latitude)) # Coordenada y
  }
    
  return example_item


def insert_mock_data() -> None:
  dynamodb = boto3.client('dynamodb')
  table_name = 'WildfiresTable'

  num_records_to_insert = random.randint(2000, 3000)
  for _ in range(num_records_to_insert):
    item = generate_random_record()
    dynamodb.put_item(
      TableName=table_name,
      Item={
          "date": {"S": item["date"]},
          "id": {"S": item["id"]},
          "conf": {"N": str(item["conf"])},
          "sat": {"S": item["sat"]},
          "x": {"N": str(item["x"])},
          "y": {"N": str(item["y"])}
      }
    )