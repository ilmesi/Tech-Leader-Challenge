import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, date
import json
from moto import mock_dynamodb

from .database.init import init_db
from .database.mockData import insert_mock_data

from .segmentation.segmentation import segmentacion_de_incendios


def filtrar_fuegos(wildfires_table: any, from_date: date, to_date: date) -> list[dict]:
  """Devuelve los fuegos filtrados por los parámetros de fechas

  Input
  ------
  wildfires_table : any
    Tabla de DyanmoDB para consultar
  from_date : date
    Fecha mínima para consultar
  to_date : date
    Fecha máxima para consultar

  Output
  ------
  list[dict]
    Fuegos filtrados por el rango de fechas
  """

  # Para evitar realizar un `scan` de la tabla y filtrar a través de un `scan`, realizamos un filtro mediante
  # un campo dummy cómo lo es `sat` y hacemos el filtro sobre el sort index `date`.
  response = wildfires_table.query(
    IndexName='date-index',
    KeyConditionExpression=Key('sat').eq('Firesat23') & Key('date').between(from_date.isoformat(), to_date.isoformat()),
  )
  return response['Items']


@mock_dynamodb
def lambda_handler(event: dict, context: dict) -> dict:

  # En el caso que el campo body venga desde una request será un dict, caso contrario sam lo levanta cómo un str
  # cuando lo va a buscar al archivo "events/fireSegmentationEvent.json"
  body = event.get('body', {})
  if type(body) == str:
    body = json.loads(body)

  # Tomamos los parámetros de fechas y agregamos la posibilidad de enviar distance
  # y time (defaulteados en 10  y 100 respectivamente).
  from_date_string = body.get('fromDate', event.get('fromDate'))
  to_date_string = body.get('toDate', event.get('toDate'))

  if None in [from_date_string, to_date_string]:
    return { "statusCode": 400, "body": {"error": "Missing fields `fromDate` and `toDate`"} }

  fromDate: date = datetime.strptime(from_date_string, "%Y-%m-%dT%H:%M:%S")
  toDate: date = datetime.strptime(to_date_string, "%Y-%m-%dT%H:%M:%S")
  distance: float = event.get("distance", 10.0)
  time: float = event.get("time", 100.0)

  # Inicialización de la BD
  init_db()
  insert_mock_data()

  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
  table_name = 'WildfiresTable'
  wildfires_table = dynamodb.Table(table_name)

  # Fecha y filtrado de fuegos
  fuegos: list[dict] = filtrar_fuegos(wildfires_table, fromDate, toDate)

  # Agrupación de fuegos en incendios
  incendios = segmentacion_de_incendios(fuegos, distance, time)

  return { "statusCode": 200, "body": incendios }
