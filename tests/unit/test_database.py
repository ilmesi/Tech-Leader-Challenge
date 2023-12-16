import boto3
from moto import mock_dynamodb

from FireSegmentationAPI.database.init import init_db


@mock_dynamodb
def test_init_db_table_creation():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    assert 'WildfiresTable' not in [table.name for table in dynamodb.tables.all()]

    init_db()

    assert 'WildfiresTable' in [table.name for table in dynamodb.tables.all()]


@mock_dynamodb
def test_init_db_table_schema():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    assert 'WildfiresTable' not in [table.name for table in dynamodb.tables.all()]

    init_db()

    table = [table for table in dynamodb.tables.all() if table.name == 'WildfiresTable'][0]
   
    assert table.key_schema == [
        {
            'AttributeName': 'date',
            'KeyType': 'RANGE'
        },
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ]
    assert table.attribute_definitions == [
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
    ]
    assert table.global_secondary_indexes == [
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
            },
            'IndexStatus': 'ACTIVE',
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 0,
                'WriteCapacityUnits': 0
            }
        }
    ]


@mock_dynamodb
def test_init_db_table_empty():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    assert 'WildfiresTable' not in [table.name for table in dynamodb.tables.all()]

    init_db()

    table = [table for table in dynamodb.tables.all() if table.name == 'WildfiresTable'][0]
    assert table.item_count == 0
