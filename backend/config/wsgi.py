import os
from django.core.wsgi import get_wsgi_application
from decouple import config

# Use production settings by default in WSGI, can be overridden with env var
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_MODULE', default='config.settings.production'))

application = get_wsgi_application()
