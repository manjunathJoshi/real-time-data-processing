from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from DataTransformer.views import TransformData



urlpatterns = [
	path('v1', csrf_exempt(TransformData.as_view()), name='transform_data'),
]