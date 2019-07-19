import json
import boto3
import datetime
import os
import subprocess
instance = ['i-009b1021b74fb9f21']

#Fix the health so that it checks the health of all the instances and can be done easily just look at start and stop lambdas
#Need to do the SES (Email) and most likely format the text file better 
#Other Policies that are needed are AmazonS3FullAccess and AmazonEC2ReadOnlyAccess

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    file = open("/tmp/DailyReport.txt", "w")
    
    #Health checks
    
    health = '';
    for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
        health = (status['InstanceStatus']['Status'])
        print(health)
    
    #Volume Size Delete if not needed
    ''''
    volumes = ec2.meta.client.describe_instance_attribute(InstanceId='i-009b1021b74fb9f21', Attribute='blockDeviceMapping')
    volumeId = (volumes['BlockDeviceMappings'][0]['Ebs']['VolumeId'])
    
    volume = ec2.Volume(volumeId)
    volumeSize = str(volume.size)
    '''
    
    '''
    #This commmand was supposed to give the space usage info but had errors with to see the full problem go to the link below
    #https://stackoverflow.com/questions/57114028/it-is-saying-that-the-dev-xdva1-doesnt-exist
    #The space usage should appear after using the command
    
    os.system('df -hT /')
    '''
    ################################################
    
    #The cost of the last day
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
    
    #Writes to file 
    
    s = ("InstanceId: i-009b1021b74fb9f21 \n" + "Health: " + health + "\n" + "Total Disk Space: " + volumeSize + "\n" + "Daily Cost: " + dailyCost)
    
    file.write(s)
    
    file.close()

    #Upload to s3
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/DailyReport.txt', 'dailyreport123456789', 'DailyReport.txt')
