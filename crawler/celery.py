from celery import Celery

from config import REDIS_URL

app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)
