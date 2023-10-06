import boto3
from moto import mock_dynamodb

from database.init import init_db, insert_example_item

@mock_dynamodb
def lambda_handler (event: dict, context: dict) -> dict:
  init_db()
  insert_example_item()
  return { "statusCode": 200, "body": "Database initialized"}