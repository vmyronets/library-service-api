import os
import sys
from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "library_service.settings"
)

app = Celery("library_service_api")
app.config_from_object("django.conf:settings", namespace="CELERY")

if sys.platform == "win32":
    app.conf.update(worker_pool="solo")

app.autodiscover_tasks()
