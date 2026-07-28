from pathlib import Path

from celery.utils.log import get_task_logger

from app.celery_app import celery_app
from app.image_processor import process_image


logger = get_task_logger(__name__)


@celery_app.task(bind=True, autoretry_for=(OSError,), retry_backoff=True, max_retries=3)
def process_image_task(self, input_path: str, output_path: str) -> dict:
    logger.info("Memproses %s pada worker %s", input_path, self.request.hostname)
    result = process_image(Path(input_path), Path(output_path))
    result["worker"] = self.request.hostname
    result["task_id"] = self.request.id
    return result

