import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
storage_regular = Celery(
    main='storage_regular',
    include=[
        'apps.storage.tasks.processing',
    ],
)
storage_regular.config_from_object(obj='django.conf:settings', namespace='CELERY')
storage_regular.autodiscover_tasks()
