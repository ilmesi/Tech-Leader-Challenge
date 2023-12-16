import boto3


def init_db() -> None:
  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
  table_name = 'WildfiresTable'

  table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
      {
        'AttributeName': 'date',
        'KeyType': 'RANGE'
      },
      {
        'AttributeName': 'id',
        'KeyType': 'HASH'
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
      },
      {
        'AttributeName': 'sat',
        'AttributeType': 'S'
      }
    ],
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'date-index',
            'KeySchema': [
                {
                    'AttributeName': 'sat',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'date',
                    'KeyType': 'RANGE'
                }
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            }
        }
    ],
    BillingMode='PAY_PER_REQUEST'
  )

  table.meta.client.get_waiter('table_exists').wait(TableName=table_name)