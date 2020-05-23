import json
import requests
import boto3
import urllib3
import bz2

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    message = json.loads(event['Records'][0]['Sns']['Message'])
    match_id = message['match_id']

    url = "https://api.opendota.com/api/replays?match_id={}".format(match_id)
    raw_json = requests.get(url)
    replay_info = json.loads(raw_json.text)[0]
    url = "http://replay{}.valve.net/570/{}_{}.dem.bz2".format(replay_info['cluster'], replay_info['match_id'], replay_info['replay_salt'])
    replay = requests.get(url, allow_redirects=True)
    decompressed = bz2.decompress(replay.content)

    with open("/tmp/{}.dem".format(match_id), 'wb') as f:
        f.write(decompressed)

    s3.upload_file("/tmp/{}.dem".format(match_id), "dota-replays-storage", "{}.dem".format(match_id))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello')
    }