import boto3
from moto import mock_dynamodb

from database.init import init_db
from api.firesat23 import get_wildfires_last_24_hours

@mock_dynamodb # No remover, es para mockear DynamoDB
def lambda_handler (event: dict, context: dict) -> dict:
  init_db() # No remover, es para inicializar la base de datos

  firesat_csv: str = get_wildfires_last_24_hours()
  return { "statusCode": 200, "body": firesat_csv}