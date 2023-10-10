import boto3
import json
from moto import mock_dynamodb

from database.init import init_db
from database.mockData import insert_mock_data

@mock_dynamodb
def lambda_handler (event: dict, context: dict) -> dict:

  init_db()
  insert_mock_data()

  jsonParams = json.loads(event["body"])
  print(jsonParams)
  
  return { "statusCode": 200, "body": jsonParams}