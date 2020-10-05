import os

from celery import Celery,platforms
from tasks import config

platforms.C_FORCE_ROOT = True  # 加上这一行
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_tt.settings')

celery_app = Celery('tasks')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()
