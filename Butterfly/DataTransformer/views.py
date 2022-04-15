from django.shortcuts import render
from DataTransformer.tasks import *
from Butterfly.responses import *
from Butterfly.utils import logger
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework import views
from django.views import View
from DataTransformer.tasks import *
from DataTransformer.utils import insert_packet_data
# Create your views here.


class TransformData(View):

	def __init__(self):
		self.exception = ""
		self.response = init_response()

	def post(self, request, *args, **kwargs):
		try:
			request_body = request.POST
			primary_resource_id = int(request_body.get('primary_resource_id',''))
			data_packet_index = int(request_body.get('data_packet_index',''))
			last_chunk_flag = True if request_body.get('last_chunk_flag') == 'True' else False
			file = request.FILES.get('file','')
			raw_payload = None
			for i in file:
				raw_payload = i
			result = insert_packet_data(primary_resource_id,data_packet_index,raw_payload,last_chunk_flag)
			return send_200(self.response)
		except Exception as e:
			logger.exception(str(e))
			self.exception = str(e)
		return send_500(self.response)

class HealthCheck(View):
	'''API to heath check for load balancer '''

	def get(self,request):
		return send_200("Welcome to data transform module")