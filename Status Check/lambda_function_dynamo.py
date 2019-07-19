import json
import boto3
import time
region = 'us-east-2'
instances = ['i-009b1021b74fb9f21']

#Work do this to account for both instances
#Needs a CloudWatch Role for trigger
#Cron Expression for CloudWatch Role 0/30 8-20 ? * * *
#The first number is it updates every 30 minutes and 8-20 is the time interval when it updates

def lambda_handler(event, context):
    client = boto3.client('ec2')
    response = client.describe_instance_status(IncludeAllInstances = True)
    dynamodb = boto3.resource('dynamodb')
    dynamodbTable = dynamodb.Table('Daily30Checks')
    for i in response["InstanceStatuses"]:
        dynamodbTable.put_item(
            Item={
                'Time':time.ctime(),
                'InstanceId': i['InstanceId'],
                'InstanceState': i['InstanceState']['Name'],
                'InstanceStatus': i['InstanceStatus']['Status'],
                'System status' : i['SystemStatus']['Status']
            }
        )
