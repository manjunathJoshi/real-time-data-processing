import boto3
from DataTransformer.models import DataStreamPacket, DataStream
from Butterfly.config import *
from Butterfly.utils import logger

def insert_streams_data(primary_resource_id,last_chunk_flag):
    try:
        data_stream = DataStream.objects.get_stream(primary_resource_id=primary_resource_id)
        if not data_stream:
            data_stream = DataStream.objects.create(primary_resource_id =primary_resource_id,stream_transferd=last_chunk_flag )
        if last_chunk_flag:
            data_stream.stream_transferd = last_chunk_flag
            data_stream.save(update_fields=['stream_transferd'])        
        return data_stream
    except Exception as e:
        logger.exception(str(e))
        raise Exception(str(e))


def insert_packet_data(primary_resource_id,data_packet_index,raw_payload,last_chunk_flag):
    from DataTransformer.tasks import ancillary_process
    try:
        stream = insert_streams_data(primary_resource_id=primary_resource_id,last_chunk_flag=last_chunk_flag)
        data_packet_db_response = DataStreamPacket.objects.create(data_packet_index=data_packet_index,primary_resource_id=stream,raw_payload=raw_payload)
        ancillary_process.apply_async([primary_resource_id, data_packet_index])
    except Exception as e:
        logger.exception(str(e))
        raise Exception(str(e))

# def data_yield():

