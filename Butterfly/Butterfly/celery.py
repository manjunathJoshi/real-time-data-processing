from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
# from django.apps import apps

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Butterfly.settings')

app = Celery('Butterfly',
         broker = os.environ.get("BROKER_URL"),
         include=[])
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# apps.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# app.conf.beat_schedule = {
#     'schedule-tasks': {
#         'task': 'poll_for_events',
#         'schedule': 1,
#         'options': {'queue': os.environ.get('SCHEDULING_QUEUE')}
#     }
# }