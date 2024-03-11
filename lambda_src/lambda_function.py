import os
import json
import logging

import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        endpoint_name = os.environ['SAGEMAKER_ENDPOINT']
        client = boto3.client('sagemaker-runtime')
        
        logger.info(f'request event: {event}, type: {type(event)}')
        
        payload = json.dumps(event).encode('utf-8')
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            Body=payload,
            ContentType='application/json',
        )

        result = json.loads(response['Body'].read().decode())
        return result
    except Exception as e:
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Internal Server Error: {e}'})
        }
