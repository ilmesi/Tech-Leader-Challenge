import boto3
from moto import mock_dynamodb
from decimal import Decimal

def init_db() -> None:
  # Initialize a DynamoDB client
  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

  # Define the table schema
  table_name = 'WildfiresTable'

  table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
      {
        'AttributeName': 'continent_date',
        'KeyType': 'HASH'  # Primary Key
      },
      {
        'AttributeName': 'id',
        'KeyType': 'RANGE'  # Sort Key
      }
    ],
    AttributeDefinitions=[
      {
        'AttributeName': 'continent_date',
        'AttributeType': 'S'  # String
      },
      {
        'AttributeName': 'id',
        'AttributeType': 'S'  # String
      }
    ],
    BillingMode='PAY_PER_REQUEST'  # Serverless mode
  )

  # Wait for the table to be created
  table.meta.client.get_waiter('table_exists').wait(TableName=table_name)


def insert_example_item() -> None:

  # Initialize a DynamoDB client
  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

  # Define the table schema
  table_name = 'WildfiresTable'

  # Insert an example item into the table
  example_item = {
    "continent_date": "SA_2023-10-05T19",
    "id": "2023-10-05T19:00:00+00:00+-10.02+16.71",
    "conf": 15,
    "sat": "noaa-goes16",
    "x": Decimal(-10.0165882110595703125),
    "y": Decimal(16.7101154327392578125)
  }

  table = dynamodb.Table(table_name)
  table.put_item(Item=example_item)

  # Read the entire DynamoDB table
  response = table.scan()
  items = response['Items']

  for item in items:
    print(item)