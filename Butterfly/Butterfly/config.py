import os

env = os.environ.get('ENV', 'dev')
SERVER_DATABASES = {
	'default': {
	'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': os.environ.get('POSTGRES_DB_NAME'),
		'USER': os.environ.get('POSTGRES_USERNAME'),
		'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
		'HOST':os.environ.get('POSTGRES_HOST'),
		'PORT': os.environ.get('POSTGRES_PORT'),
	}
}
CELERY_SYNC = True
DOWN_STREAM_QUEUE = os.environ.get('DOWN_STREAM_QUEUE')
S3_BUCKET = os.environ.get('S3_BUCKET')
DOWNSTREAM_API_URL = os.environ.get('DOWNSTREAM_API_URL')