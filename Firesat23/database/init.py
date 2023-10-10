import boto3
from decimal import Decimal

def init_db() -> None:
  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
  table_name = 'WildfiresTable'

  table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
      {
        'AttributeName': 'continent_date',
        'KeyType': 'HASH'
      },
      {
        'AttributeName': 'id',
        'KeyType': 'RANGE'
      }
    ],
    AttributeDefinitions=[
      {
        'AttributeName': 'continent_date',
        'AttributeType': 'S'
      },
      {
        'AttributeName': 'id',
        'AttributeType': 'S'
      }
    ],
    BillingMode='PAY_PER_REQUEST'
  )

  table.meta.client.get_waiter('table_exists').wait(TableName=table_name)


def insert_example_item() -> None:

  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
  table_name = 'WildfiresTable'

  example_item = {
    "continent_date": "SA_2023-10-05T19", # Es el continente en dos caracteres + fecha con formato ISO 8601 cortada hasta la hora
    "id": "2023-10-05T19:00:00+00:00+-10.02+16.71", # Es el ISO 8601 + latitud + longitud con aproximación de dos dígitos
    "conf": 15, # Es la confianza de la detección
    "sat": "noaa-goes16",
    "x": Decimal(-10.0165882110595703125),
    "y": Decimal(16.7101154327392578125)
  }

  table = dynamodb.Table(table_name)
  table.put_item(Item=example_item)
  
  response = table.scan()
  items = response['Items']

  for item in items:
    print(item)