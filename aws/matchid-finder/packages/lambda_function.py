import json
import requests
import boto3
import urllib3
from bs4 import BeautifulSoup
import re
import botocore
import time

def lambda_handler(event, context):
    s3 = boto3.resource("s3")
    client = boto3.client("sns")
    #get matchids, iterate through
    r = requests.get("http://dota2protracker.com")
    soup = BeautifulSoup(r.text)
    raw_links = soup.findAll('a', href=re.compile('dotabuff'))
    match_ids = []
    for link in raw_links:
        match_id = re.search(r"\d{10,}", str(link))[0]
        match_ids.append(match_id)

    for match_id in match_ids:
        try:
            s3.Object('dota-replays-storage', '{}.dem'.format(match_id)).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404": #replay doesn't exist
                time.sleep(1)
                print("Match {} not found, trying to grab.".format(match_id))
                message = {"match_id": match_id}
                response = client.publish(
                    TargetArn="arn:aws:sns:us-west-1:575345508156:replays",
                    Message=json.dumps({'default': json.dumps(message)}),
                    MessageStructure='json'
                    )
        else:
            print("Match {} found.".format(match_id))

    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello')
    }