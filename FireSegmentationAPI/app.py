import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, date
import json
from moto import mock_dynamodb

from database.init import init_db
from database.mockData import insert_mock_data

from segmentation.segmentation import segmentacion_de_incendios


def filtrar_fuegos(wildfires_table: any, from_date: date, to_date: date):
  response = wildfires_table.query(
    IndexName='date-index',
    KeyConditionExpression=Key('sat').eq('Firesat23') & Key('date').between(from_date.isoformat(), to_date.isoformat()),
  )
  return response['Items']


@mock_dynamodb
def lambda_handler(event: dict, context: dict) -> dict:

  body = event.get('body', {})
  if type(body) == str:
    body = json.loads(body)

  from_date_string = body.get('fromDate', event.get('fromDate'))
  fromDate: date = datetime.strptime(from_date_string, "%Y-%m-%dT%H:%M:%S")
  to_date_string = body.get('toDate', event.get('toDate'))
  toDate: date = datetime.strptime(to_date_string, "%Y-%m-%dT%H:%M:%S")
  distance: float = event.get("distance", 10.0)
  time: float = event.get("time", 100.0)

  init_db()
  insert_mock_data()

  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
  table_name = 'WildfiresTable'
  wildfires_table = dynamodb.Table(table_name)

  fuegos: list[dict] = filtrar_fuegos(wildfires_table, fromDate, toDate)

  incendios = segmentacion_de_incendios(fuegos, distance, time)

  return { "statusCode": 200, "body": incendios }
