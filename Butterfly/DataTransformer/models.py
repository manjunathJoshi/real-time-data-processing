from django.db import models
from django.db import IntegrityError
from django.contrib.postgres.fields import ArrayField
from Butterfly.utils import logger

class BaseModel(models.Model):
	""" Base abstract model"""
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		abstract = True

class DataStreamManager(models.Manager):
    def get_stream(self, **kwargs):
        try:
            return self.get(**kwargs)
        except IntegrityError as e:
            logger.exception(str(e))
            return None
        except Exception as e:
            logger.exception(str(e))
            return None

class DataStream(BaseModel):
    primary_resource_id = models.IntegerField(db_index=True)
    stream_transferd = models.BooleanField(default=False)
    
    objects = DataStreamManager()

    def __str__(self):
        return f"{self.pk} -- {self.primary_resource_id} -- {self.stream_transferd} "


class DataStreamPacketManager(models.Manager):
    def get_packet(self, **kwargs):
        try:
            return self.get(**kwargs)
        except IntegrityError as e:
            raise IntegrityError(str(e))
        except Exception as e:
            raise Exception(str(e))

class DataStreamPacket(BaseModel):
    data_packet_index  = models.IntegerField(db_index=True)
    primary_resource_id = models.ForeignKey(DataStream,on_delete=models.CASCADE)
    raw_payload = models.BinaryField(default=b"default text")
    transformed_data = ArrayField(models.IntegerField(),null=True,blank=True)

    objects = DataStreamPacketManager()

    class Meta:
        unique_together = ('data_packet_index', 'primary_resource_id')

    def __str__(self):
        return f"{self.pk} -- {self.primary_resource_id} -- {self.data_packet_index} "

