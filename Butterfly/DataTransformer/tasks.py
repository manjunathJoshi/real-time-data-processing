from Butterfly.celery import app
from django.conf import settings
import datetime
from datetime import date
from celery.exceptions import MaxRetriesExceededError
import json
import logging
logger = logging.getLogger('django')
from DataTransformer.models import DataStreamPacket,DataStream
from DataTransformer.sqs_executors import push_data_to_sqs
from DataTransformer.kinesis_executors import poll_for_kinesis_events

# celery task to process ancillary :  (series of bytes) as the input and converts it into an array of integers
@app.task(name="ancillary_process", queue=settings.DEFAULT_CELERY_QUEUE,
		  autoretry_for= (Exception,) ,retry_kwargs={'max_retries': 2}, retry_backoff=True, retry_jitter = False)
def ancillary_process(primary_resource_id, data_packet_index):
	try:
		current_retry = ancillary_process.request.retries
		if current_retry == 2:
			raise MaxRetriesExceededError("Maximum retries exceeded")
		# repayment_notification_to_partner.apply_async(args=[payload])
		data_stream = DataStream.objects.get_stream(primary_resource_id=primary_resource_id)
		data_stream_packet = DataStreamPacket.objects.get_packet(primary_resource_id=data_stream,data_packet_index=data_packet_index)
		raw_payload = data_stream_packet.raw_payload.tobytes()
		result = []
		transformed_data = raw_payload.decode('utf-8')
		data_array = transformed_data.split()
		for i in range(0,len(data_array)):
			result.append(len(data_array[i]))

		data_stream_packet.transformed_data = result
		data_stream_packet.updated_on = datetime.datetime.now()
		data_stream_packet.save(update_fields=['transformed_data','updated_on'])

		if data_stream.stream_transferd:
			data_down_streamer.apply_async([primary_resource_id])

	except MaxRetriesExceededError as e:
		logger.error("MaxRetriesExceededError")
		raise Exception("Maximum retries exceeded")
	except Exception as e:
		logger.error("MaxRetriesExceededError")
		raise Exception(f" Failed due to {e}")

# the output from the ancillary service and collate them into a single array (correctly ordered) for a 
# particular Primary Resource ID

@app.task(name="data_down_streamer", queue=settings.DEFAULT_CELERY_QUEUE,
		  autoretry_for= (Exception,), retry_kwargs={'max_retries': 2}, retry_backoff=True, retry_jitter = False)
def data_down_streamer(primary_resource_id):
	try:
		current_retry = data_down_streamer.request.retries
		if current_retry == 2:
			raise MaxRetriesExceededError("Maximum retries exceeded")
		request_body = json.loads(request_body)
		# repayment_notification_to_partner.apply_async(args=[payload])
		output_array = []
		data_stream = DataStream.objects.get_stream(primary_resource_id=primary_resource_id)
		array_data =  DataStreamPacket.objects.filter(primary_resource_id=data_stream).order_by('data_packet_index')
		for data in array_data:
			tranformed_data = []
			tranformed_data = data.transformed_data
			output_array.extend(tranformed_data)
		push_data_to_sqs(output_array)
	except MaxRetriesExceededError as e:
		logger.error("MaxRetriesExceededError")
		raise Exception("Maximum retries exceeded")
	except Exception as e:
		logger.error("MaxRetriesExceededError")
		raise Exception(f" Failed due to {e}")


@app.task(name="poll_for_events", queue=settings.SCHEDULING_QUEUE)
def poll_for_events():
	try:
		poll_for_kinesis_events()
	except MaxRetriesExceededError as e:
		logger.error("MaxRetriesExceededError")
		raise Exception("Maximum retries exceeded")
	except ValueError as e:
		logger.error("MaxRetriesExceededError")
		raise ValueError("value error occurred while making a request" + str(e))
	except Exception as e:
		logger.error("MaxRetriesExceededError")
		raise Exception(f" Failed due to {e}")