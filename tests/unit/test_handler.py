import boto3
from moto import mock_dynamodb

from FireSegmentationAPI import app
from FireSegmentationAPI.segmentation.segmentation import segmentacion_de_incendios


def test_handler_sin_parametros_fail(invalid_gw_event, lambda_context):
   response = app.lambda_handler(invalid_gw_event, context=lambda_context)

   assert response["statusCode"] == 400
   assert "body" in response
   assert "error" in response["body"]


def test_handler_con_paramtros_success(valid_gw_event, lambda_context):
   response = app.lambda_handler(valid_gw_event, context=lambda_context)

   assert response["statusCode"] == 200
   assert "body" in response
   assert "error" not in response["body"]
   assert response["body"][0] > 0
   assert len(response["body"][1]) > 0


@mock_dynamodb
def test_handler_con_resultados_vacios(valid_gw_event_with_old_dates, lambda_context):
   dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
   table_name = 'WildfiresTable'
   wildfires_table = dynamodb.Table(table_name)

   response = app.lambda_handler(valid_gw_event_with_old_dates, context=lambda_context)

   assert wildfires_table.item_count > 0

   assert response["statusCode"] == 200
   assert "body" in response
   assert "error" not in response["body"]
   assert response["body"][0] == 0
   assert len(response["body"][1]) == 0


@mock_dynamodb
def test_handler_con_resultados_no_vacios(valid_gw_event_with_good_dates, lambda_context):

   response = app.lambda_handler(valid_gw_event_with_good_dates, context=lambda_context)

   dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
   table_name = 'WildfiresTable'
   wildfires_table = dynamodb.Table(table_name)
   fuegos = wildfires_table.scan()["Items"]
   d = 10
   t = 100
   incendios = segmentacion_de_incendios(fuegos, d, t)

   assert response["statusCode"] == 200
   assert "body" in response
   assert "error" not in response["body"]
   assert response["body"][0] == incendios[0]
