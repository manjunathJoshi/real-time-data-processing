from django.contrib import admin
from DataTransformer.models import DataStream,DataStreamPacket


# Register your models here.
admin.site.register(DataStream)
admin.site.register(DataStreamPacket)
