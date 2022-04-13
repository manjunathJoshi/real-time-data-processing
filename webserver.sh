python3 manage.py collectstatic --no-input && python manage.py migrate && gunicorn Butterfly.wsgi -b 0.0.0.0:8000
