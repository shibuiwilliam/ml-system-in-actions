from typing import Dict, Any
from fastapi import BackgroundTasks
import logging
from pydantic import BaseModel

from src.app.backend.redis_client import redis_client


logger = logging.getLogger(__name__)


def set_data_redis(key: str, value: Any) -> bool:
    redis_client.set(key, value)
    return True


def get_data_redis(key: str) -> Any:
    data = redis_client.get(key)
    if data is None:
        return None
    return data


class SaveDataJob(BaseModel):
    item_id: str
    data: Any

    def __call__(self):
        pass


class SaveDataRedisJob(SaveDataJob):
    def __call__(self):
        save_data_jobs[self.item_id] = self
        logger.info(f"registered cache: {self.item_id} in {self.__class__.__name__}")
        self.is_completed = set_data_redis(key=self.item_id, value=self.data)
        logger.info(f"completed save data: {self.item_id}")


async def save_data_job(data: Any, item_id: str, background_tasks: BackgroundTasks) -> str:
    task = SaveDataRedisJob(item_id=item_id, data=data)
    background_tasks.add_task(task)
    return item_id


save_data_jobs: Dict[str, SaveDataJob] = {}
