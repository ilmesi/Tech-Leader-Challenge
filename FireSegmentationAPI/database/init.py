import boto3

def init_db() -> None:
  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
  table_name = 'WildfiresTable'

  table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
      {
        'AttributeName': 'date',
        'KeyType': 'HASH'
      },
      {
        'AttributeName': 'id',
        'KeyType': 'RANGE'
      }
    ],
    AttributeDefinitions=[
      {
        'AttributeName': 'date',
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