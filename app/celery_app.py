from celery import Celery

from app.config import REDIS_URL


celery_app = Celery("distributed_image_processing", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    result_expires=86400,
    timezone="UTC",
)
celery_app.autodiscover_tasks(["app"])

