import boto3
region = 'us-east-2'
instances = []

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            temp = instance['Tags']
            temp = temp[0]['Key']
            tag = "Time"
            if (temp == tag):
                instances.append(instance["InstanceId"])
    ec2.stop_instances(InstanceIds=instances) 