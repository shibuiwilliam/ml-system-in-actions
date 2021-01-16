import logging
from typing import Any, Dict

from fastapi import BackgroundTasks
from PIL import Image
from pydantic import BaseModel
from src.api_composition_proxy.backend.store_data_job import left_push_queue, save_image_redis_job
from src.api_composition_proxy.configurations import CacheConfigurations
from src.api_composition_proxy.constants import CONSTANTS

logger = logging.getLogger(__name__)


class SaveDataJob(BaseModel):
    job_id: str
    data: Any
    queue_name: str = CONSTANTS.REDIS_QUEUE
    is_completed: bool = False

    def __call__(self):
        pass


class SaveDataRedisJob(SaveDataJob):
    enqueue: bool = False

    def __call__(self):
        save_data_jobs[self.job_id] = self
        logger.info(f"registered job: {self.job_id} in {self.__class__.__name__}")
        self.is_completed = save_image_redis_job(job_id=self.job_id, image=self.data)
        if self.enqueue:
            self.is_completed = left_push_queue(self.queue_name, self.job_id)
        logger.info(f"completed save data: {self.job_id}")


def save_data_job(
    data: Image.Image,
    job_id: str,
    background_tasks: BackgroundTasks,
    enqueue: bool = False,
) -> str:
    task = SaveDataRedisJob(
        job_id=job_id,
        data=data,
        queue_name=CacheConfigurations.queue_name,
        enqueue=enqueue,
    )
    background_tasks.add_task(task)
    return job_id


save_data_jobs: Dict[str, SaveDataJob] = {}
