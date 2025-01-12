import pytest


def factoryEvent(body='') -> dict:
   return {
      "body": body,
      "headers": {
         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
         "Accept-Encoding":"gzip, deflate, br",
         "Accept-Language":"pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
         "Cache-Control":"max-age=0",
         "Connection":"keep-alive",
         "Host":"127.0.0.1:3000",
         "Sec-Ch-Ua":"\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
         "Sec-Ch-Ua-Mobile":"?0",
         "Sec-Ch-Ua-Platform":"\"Linux\"",
         "Sec-Fetch-Dest":"document",
         "Sec-Fetch-Mode":"navigate",
         "Sec-Fetch-Site":"none",
         "Sec-Fetch-User":"?1",
         "Upgrade-Insecure-Requests":"1",
         "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
         "X-Forwarded-Port":"3000",
         "X-Forwarded-Proto":"http"
      },
      "httpMethod":"GET",
      "isBase64Encoded":False,
      "multiValueHeaders": {
         "Accept":[
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
         ],
         "Accept-Encoding":[
            "gzip, deflate, br"
         ],
         "Accept-Language":[
            "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
         ],
         "Cache-Control":[
            "max-age=0"
         ],
         "Connection":[
            "keep-alive"
         ],
         "Host":[
            "127.0.0.1:3000"
         ],
         "Sec-Ch-Ua":[
            "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\""
         ],
         "Sec-Ch-Ua-Mobile":[
            "?0"
         ],
         "Sec-Ch-Ua-Platform":[
            "\"Linux\""
         ],
         "Sec-Fetch-Dest":[
            "document"
         ],
         "Sec-Fetch-Mode":[
            "navigate"
         ],
         "Sec-Fetch-Site":[
            "none"
         ],
         "Sec-Fetch-User":[
            "?1"
         ],
         "Upgrade-Insecure-Requests":[
            "1"
         ],
         "User-Agent":[
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
         ],
         "X-Forwarded-Port":[
            "3000"
         ],
         "X-Forwarded-Proto":[
            "http"
         ]
      },
      "multiValueQueryStringParameters":"",
      "path":"/hello",
      "pathParameters":"",
      "queryStringParameters":"",
      "requestContext": {
         "accountId":"123456789012",
         "apiId":"1234567890",
         "domainName":"127.0.0.1:3000",
         "extendedRequestId":"",
         "httpMethod":"GET",
         "identity": {
            "accountId":"",
            "apiKey":"",
            "caller":"",
            "cognitoAuthenticationProvider":"",
            "cognitoAuthenticationType":"",
            "cognitoIdentityPoolId":"",
            "sourceIp":"127.0.0.1",
            "user":"",
            "userAgent":"Custom User Agent String",
            "userArn":""
         },
         "path":"/hello",
         "protocol":"HTTP/1.1",
         "requestId":"a3590457-cac2-4f10-8fc9-e47114bf7c62",
         "requestTime":"02/Feb/2023:11:45:26 +0000",
         "requestTimeEpoch":1675338326,
         "resourceId":"123456",
         "resourcePath":"/hello",
         "stage":"Prod"
      },
      "resource":"/hello",
      "stageVariables":"",
      "version":"1.0"
   }



@pytest.fixture
def valid_gw_event_with_good_dates():
   """ Generates an API GW valid Event with a full year timespan"""

   return factoryEvent(body='{"fromDate": "2023-01-01T00:00:00", "toDate": "2024-01-01T00:00:00"}')


@pytest.fixture
def valid_gw_event_with_old_dates():
   """ Generates an API GW valid Event but with really old dates"""

   return factoryEvent(body='{"fromDate": "1970-01-01T00:00:00", "toDate": "1970-01-01T23:59:59"}')


@pytest.fixture
def valid_gw_event():
   """ Generates an API GW valid Event"""

   return factoryEvent(body='{"fromDate": "2023-01-01T00:00:00", "toDate": "2023-01-01T23:59:59"}')


@pytest.fixture
def invalid_gw_event():
   """ Generates an API GW invalid Event without body"""

   return factoryEvent(body='{}')


@pytest.fixture
def lambda_context():
   class LambdaContext:
      def __init__(self):
         self.function_name = "test-func"
         self.memory_limit_in_mb = 128
         self.invoked_function_arn = "arn:aws:lambda:eu-west-1:809313241234:function:test-func"
         self.aws_request_id = "52fdfc07-2182-154f-163f-5f0f9a621d72"

      def get_remaining_time_in_millis(self) -> int:
         return 1000

   return LambdaContext()
