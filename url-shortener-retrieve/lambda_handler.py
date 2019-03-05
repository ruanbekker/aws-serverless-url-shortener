import os
import json
import boto3

ddb = boto3.resource('dynamodb', region_name = 'eu-west-1').Table('url-shortener-table')

def lambda_handler(event, context):
    short_id = event.get('short_id')
    
    try:
        item = ddb.get_item(Key={'short_id': short_id})
        long_url = item.get('Item').get('long_url')
        # increase the hit number on the db entry of the url (analytics?)
        ddb.update_item(
            Key={'short_id': short_id},
            UpdateExpression='set hits = hits + :val',
            ExpressionAttributeValues={':val': 1}
        )
    
    except:
        return {
            'statusCode': 301,
            'location': 'https://objects.ruanbekker.com/assets/images/404-blue.jpg'
        }
    
    return {
        "statusCode": 301,
        "location": long_url
    }
