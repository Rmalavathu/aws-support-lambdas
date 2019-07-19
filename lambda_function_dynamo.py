import json
import boto3
from pprint import pprint
import time
region = 'us-east-2'
instances = ['i-009b1021b74fb9f21']

def lambda_handler(event, context):
    client = boto3.client('ec2')
    response = client.describe_instance_status(IncludeAllInstances = True)
    dynamodb = boto3.resource('dynamodb')
    dynamodbTable = dynamodb.Table('Daily30Checks')
    for i in response["InstanceStatuses"]:
        print(time.ctime()[4])
        dynamodbTable.put_item(
            Item={
                'Time':time.ctime(),
                'InstanceId': i['InstanceId'],
                'InstanceState': i['InstanceState']['Name'],
                'InstanceStatus': i['InstanceStatus']['Status'],
                'System status' : i['SystemStatus']['Status']
            }
        )
