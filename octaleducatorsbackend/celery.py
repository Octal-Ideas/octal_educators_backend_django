# ! to be deleted if we dont use celery
import os
from celery import Celery

# Set the default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'octaleducatorsbackend.settings')

# Create the Celery app
app = Celery('octaleducatorsbackend')

# Load task modules from all registered Django app configs
app.autodiscover_tasks()
