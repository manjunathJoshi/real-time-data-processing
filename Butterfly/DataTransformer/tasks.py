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
from DataTransformer.aws_service_executor import poll_for_kinesis_events,upload_to_aws_s3
import requests
from Butterfly.config import S3_BUCKET,DOWNSTREAM_API_URL
from DataTransformer.ancillary_exec import transform_data, file_chunk_generator

# celery task to process ancillary :  (series of bytes) as the input and converts it into an array of integers
@app.task(name="ancillary_process", queue=settings.DEFAULT_CELERY_QUEUE,
		  autoretry_for= (Exception,) ,retry_kwargs={'max_retries': 2}, retry_backoff=True, retry_jitter = False)
def ancillary_process(primary_resource_id, data_packet_index):
	try:
	# Check for maximum retry threshold and raise error in case of max retry.
		current_retry = ancillary_process.request.retries
		if current_retry == 2:
			raise MaxRetriesExceededError("Maximum retries exceeded")
		data_stream = DataStream.objects.get_stream(primary_resource_id=primary_resource_id)
		data_stream_packet = DataStreamPacket.objects.get_packet(primary_resource_id=data_stream,data_packet_index=data_packet_index)
	
	# sync call to ancillary service
		result = transform_data(data_stream_packet.raw_payload)

	# store transformed_data

		data_stream_packet.transformed_data = result
		data_stream_packet.updated_on = datetime.datetime.now()
		data_stream_packet.save(update_fields=['transformed_data','updated_on'])

	# if the steam packet is last trigger dowstream activity.
		if data_stream.stream_transferd:
			array_data = data_stream_packet.order_by('data_packet_index')
			output_array = []
			for data in array_data:
				tranformed_data = []
				tranformed_data = data.transformed_data
				output_array.extend(tranformed_data)

			file_name = str(primary_resource_id)

	# downstream webhook by writing this output data (as plain text, with one
	# integer of the list per line) to a file with the filename referencing the Primary Resource ID
			# import pdb; pdb.set_trace()
			with open(f'{file_name}.txt', 'w') as f:
				for i in range(len(output_array)):
					value_string  = str(output_array[i])
					f.write(value_string)
					f.write('\n')

	# # Approach 1 : ----------------------------------------------------------------
	# 		# Upload file to s3 and return s3 url
	# 		s3_response = None
	# 		with open(f'{file_name}.txt', 'r') as file_to_upload:
	# 			s3_response = upload_to_aws_s3(f'{file_name}.txt',S3_BUCKET,file_to_upload)
	# 			# Api call to downstream services 
	# 		r = requests.post(url = DOWNSTREAM_API_URL, data = s3_response)

	# # Approach 2 :  ----------------------------------------------------------------
	# 		# downstream data with concept of chunked data transfer by http
	# 	with open(f'{file_name}.txt', 'r') as file_:
	# 		requests.post(DOWNSTREAM_API_URL, data=file_chunk_generator(file_,20))

# Approach 3 :  ----------------------------------------------------------------
		# insert into different queue where data transmits further
		# data_down_streamer.apply_async([primary_resource_id])

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
		logger.info("polling for events")
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