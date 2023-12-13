import boto3
from botocore.exceptions import ClientError
from collections.abc import Sequence
from datetime import datetime, date
from decimal import Decimal
from moto import mock_dynamodb

from database.init import init_db
from database.models import Fire
from api.firesat23 import get_wildfires_last_24_hours


def process_csv (csv_data: str, uploadFrom: date):
  firstLine: bool = True

  items = []
  for row in csv_data.splitlines():
    # Extraer la información, detectar continente y subir a la base de datos
    # Se recomienda usar la función "get_continent" del archivo "utils/get_continent.py"
    # Modularizar la solucion para hacerla más clara y entendible
    if not firstLine:
      data: tuple[str, int, Decimal, Decimal] = row.split(",")
      fire_date: date = datetime.strptime(data[0], "%Y-%m-%dT%H:%M:%S+00:00")
      # Antes de procesar cada item verificamos la fecha del mismo para que sea posterior a la fecha de control
      # ingresada en la llamada a la función a través del parámetro "uploadFrom"
      if (fire_date > uploadFrom):
        items.append(
          Fire(
            fire_date=fire_date,
            conf=data[1],
            x=data[2],
            y=data[3],
          )
        )
    firstLine = False

  return items


def save_data(items: Sequence[Fire], wildfires_table: any):
  try:
    with wildfires_table.batch_writer() as writer:
      for item in items:
        writer.put_item(Item=item.__dict__())
  except ClientError as err:
    raise


def fetch_data(wildfires_table: any):
  response = wildfires_table.scan()
  return response['Items']


@mock_dynamodb
def lambda_handler (event: dict, context: dict) -> dict:
  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
  table_name = 'WildfiresTable'
  wildfires_table = dynamodb.Table(table_name)

  init_db()
  # Fetch data from the API
  firesat_csv: str = get_wildfires_last_24_hours()
  uploadFrom: date = datetime.strptime(event["uploadFrom"], "%Y-%m-%dT%H:%M:%S+00:00")

  # Parse the data from last step & filter by date
  items = process_csv(firesat_csv, uploadFrom)

  # Save final list of filtered items
  save_data(items, wildfires_table)

  # Fetch the whole table data to return
  whole_database = fetch_data(wildfires_table)

  return { "statusCode": 200, "body": whole_database }
