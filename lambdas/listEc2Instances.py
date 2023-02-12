import boto3
import csv
import jmespath
import itertools

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
    output = list(itertools.chain(*myData))
    with open("ec2-inventory-latest.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['AccountID','InstanceID','Type','State','AZ','PrivateIP','PublicIP','KeyPair','Name'])
        writer.writerows(output)

    s3_client = boto3.client("s3")

    result = s3_client.put_object(Bucket='airbus_bucket', Key='ec2-inventory-latest.csv')

    res = result.get('ResponseMetadata')

    if res.get('HTTPStatusCode') == 200:
        return 'File Uploaded Succesfully'
    else:
        return 'File Not Uploaded'