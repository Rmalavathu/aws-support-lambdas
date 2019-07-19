import boto3
region = 'us-east-2'
instances = []

#Need a CloudWatch Role to trigger the lambda
#Cron Expression for ClouldWatch Role 0 8 * * ? *
#If you want to change the time change the second number (Uses 24 hour time)

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
    ec2.start_instances(InstanceIds=instances) 
    
