from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

from allergie import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'allergie.settings')

app = Celery("allergie")

app.config_from_object("allergie.settings", namespace="CELERY"),

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
