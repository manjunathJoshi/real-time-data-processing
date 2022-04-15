import boto3
from Butterfly.utils import logger
from DataTransformer.utils import insert_packet_data
from botocore.exceptions import NoCredentialsError

def poll_for_kinesis_events():
    try:
        stream = 'prodigal-stream'
        kinesis_client = boto3.client('kinesis', region_name='us-east-1')
        response = kinesis_client.describe_stream(StreamName=stream)
        shard_id = response['StreamDescription']['Shards'][0]['ShardId']
        shard_iterator = kinesis_client.get_shard_iterator(StreamName=stream,ShardId=shard_id,ShardIteratorType='LATEST')
        data_shard_iterator = shard_iterator['ShardIterator'] #The position in the shard from which to start reading data records sequentially

        record_response = kinesis_client.get_records(ShardIterator=data_shard_iterator,Limit=10) 
            #The position in the shard from which you want to start sequentially reading data records.
        while 'NextShardIterator' in record_response:
            record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],Limit=10)
            records = record_response.get('Records')
            for record in records:
                result = insert_packet_data(data_packet_index=record['SequenceNumber'],
                                            primary_resource_id=record['PartitionKey'],
                                            raw_payload=record['Data'],
                                            last_chunk_flag=records['NextShardIterator'])
            logger.info("Polled for kinesis")
            return result
    except Exception as e:
        logger.exception(str(e))
        raise Exception(str(e))

# kinesis_client.get_records response

# {
# 	'Records': [
# 		{
# 			'SequenceNumber': 'string',
# 			'ApproximateArrivalTimestamp': datetime(2015, 1, 1),
# 			'Data': b'bytes',
# 			'PartitionKey': 'string',
# 			'EncryptionType': 'NONE'|'KMS'
# 		},
# 	],
# 	'NextShardIterator': 'string',
# 	'MillisBehindLatest': 123,
# 	'ChildShards': [
# 		{
# 			'ShardId': 'string',
# 			'ParentShards': [
# 				'string',
# 			],
# 			'HashKeyRange': {
# 				'StartingHashKey': 'string',
# 				'EndingHashKey': 'string'
# 			}
# 		},
# 	]
# }

# machine level access to aws s3

def upload_to_aws_s3(local_file, bucket, s3_file):
    s3 = boto3.client('s3')
    try:
        response = s3.upload_file(local_file, bucket, s3_file)
        logger.info("Upload Successful")
        return response
    except Exception as e:
        logger.error("Error uploading")
        return False