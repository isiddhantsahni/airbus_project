import boto3
import csv
import jmespath
import itertools
import datetime
import json
import os

def handler(event, context):
    region = 'us-east-1'
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
                for region in ec2_client.describe_regions()['Regions']]

    for region in regions:
        print(region)

    # Get list of EC2 attributes from all profiles and regions
    myData = []
    for region in regions:
        current_session = boto3.Session(region_name = region)
        client = current_session.client('ec2')
        response = client.describe_instances()
        output = jmespath.search("Reservations[].Instances[].[NetworkInterfaces[0].OwnerId, InstanceId, InstanceType, \
                    State.Name, Placement.AvailabilityZone, PrivateIpAddress, PublicIpAddress, KeyName, [Tags[?Key=='Name'].Value] [0][0]]", response)
        myData.append(output)

    # Write myData to CSV file with headers
    file_name = 'ec2-inventory-latest_{date:%Y-%m-%d_%H-%M-%S}.csv'.format(date=datetime.datetime.now())
    output = list(itertools.chain(*myData))
    with open('/tmp/'+file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['AccountID','InstanceID','Type','State','AZ','PrivateIP','PublicIP','KeyPair','Name'])
        writer.writerows(output)
        
    with open('/tmp/'+file_name, 'r') as f1:
        content = f1.read()
    print(content)
    
    s3_client = boto3.client("s3")

    result = s3_client.put_object(Bucket='airbus-final-bucket', Key=file_name, Body=content)

    res = result.get('ResponseMetadata')
    
    print(res.get('HTTPStatusCode'))

    if res.get('HTTPStatusCode') == 200:
        print('File Uploaded Succesfully')
        return{   
        'statusCode': 200,
        # 'body': json.dumps({'message':'File Uploaded Succesfully'})
        'body':'File Uploaded Succesfully'
        }
    else:
        print('File Not Uploaded')
        return{   
        'statusCode': 404,
        'body': 'File Not Uploaded'
        }