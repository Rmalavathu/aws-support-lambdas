import json
import boto3
import datetime
import os
import subprocess
instance = ['i-009b1021b74fb9f21']

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    file = open("/tmp/DailyReport.txt", "w")
    
    health = '';
    for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
        health = (status['InstanceStatus']['Status'])
        print(health)
    
    volumes = ec2.meta.client.describe_instance_attribute(InstanceId='i-009b1021b74fb9f21', Attribute='blockDeviceMapping')
    volumeId = (volumes['BlockDeviceMappings'][0]['Ebs']['VolumeId'])
    
    volume = ec2.Volume(volumeId)
    volumeSize = str(volume.size)
    os.system('df -hT /')

    
    d = datetime.datetime.today()
    
    lastDate = str(d.year) + "-0" + str(d.month) +  "-" + str(d.day - 1)
    today = str(d.year) + "-0" + str(d.month) +  "-" + str(d.day)
    
    ce = boto3.client('ce')
    cost = ce.get_cost_and_usage(
        TimePeriod={'Start': lastDate, 'End': today},
        Granularity = 'DAILY',
        Metrics=['UnblendedCost'])
    dailyCost = round(float(cost['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']), 2)
    dailyCost = "$" + str(dailyCost)
    
    print(cost)
    s = ("InstanceId: i-009b1021b74fb9f21 \n" + "Health: " + health + "\n" + "Total Disk Space: " + volumeSize + "\n" + "Daily Cost: " + dailyCost)
    
    file.write(s)
    
    file.close()

    
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/DailyReport.txt', 'dailyreport123456789', 'DailyReport.txt')