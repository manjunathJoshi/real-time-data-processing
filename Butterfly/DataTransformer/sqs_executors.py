import boto3
from Butterfly.config import DOWN_STREAM_QUEUE
import json

# push data into fifo queue to consume by downstream services,Fifo helps in reading data sequentially.{FAN IN}

def push_data_to_sqs(payload):
    try:
        sqs = boto3.client('sqs')

        queue_url = DOWN_STREAM_QUEUE

        # Send message to SQS queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageAttributes={},
            MessageBody=json.dumps(payload)
        )
    except Exception as e:
        raise Exception(str(e))