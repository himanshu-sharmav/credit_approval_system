# credit_approval_system/celery.py

import os
from celery import Celery

# Set default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval_system.settings')

app = Celery('credit_approval_system')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
